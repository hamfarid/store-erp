/**
 * خادم WebSocket المتقدم لنظام Gaara Scan AI
 * يوفر اتصال فوري ثنائي الاتجاه للتطبيق
 * 
 * الملف: /home/ubuntu/clean_project/docker/websocket/src/websocket_server.js
 */

const WebSocket = require('ws');
const express = require('express');
const http = require('http');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const redis = require('redis');
const amqp = require('amqplib');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');
const { RateLimiterRedis } = require('rate-limiter-flexible');

// إعداد السجلات
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: '/app/logs/error.log', level: 'error' }),
        new winston.transports.File({ filename: '/app/logs/combined.log' }),
        new winston.transports.Console({
            format: winston.format.simple()
        })
    ]
});

// إعداد التطبيق
const app = express();
const server = http.createServer(app);

// إعداد الأمان والضغط
app.use(helmet());
app.use(compression());
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || ['*'],
    credentials: true
}));

app.use(express.json({ limit: '10mb' }));

// متغيرات البيئة
const PORT = process.env.PORT || 8007;
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const RABBITMQ_URL = process.env.RABBITMQ_URL || 'amqp://localhost:5672';
const JWT_SECRET = process.env.JWT_SECRET || 'gaara_websocket_secret_2024';
const MAX_CONNECTIONS = parseInt(process.env.MAX_CONNECTIONS) || 1000;
const HEARTBEAT_INTERVAL = parseInt(process.env.HEARTBEAT_INTERVAL) || 30000;

// إعداد Redis
const redisClient = redis.createClient({ url: REDIS_URL });
redisClient.on('error', (err) => logger.error('Redis Client Error', err));

// إعداد Rate Limiting
const rateLimiter = new RateLimiterRedis({
    storeClient: redisClient,
    keyPrefix: 'ws_rate_limit',
    points: 100, // عدد الرسائل
    duration: 60, // في الثانية
});

// إعداد WebSocket
const wss = new WebSocket.Server({
    server,
    verifyClient: async (info) => {
        try {
            const token = new URL(info.req.url, 'http://localhost').searchParams.get('token');
            if (!token) return false;
            
            jwt.verify(token, JWT_SECRET);
            return true;
        } catch (error) {
            logger.error('WebSocket verification failed:', error);
            return false;
        }
    }
});

// تخزين الاتصالات النشطة
const activeConnections = new Map();
const userConnections = new Map();
const roomConnections = new Map();

// فئة إدارة الاتصالات
class ConnectionManager {
    constructor() {
        this.connections = activeConnections;
        this.userConnections = userConnections;
        this.roomConnections = roomConnections;
        this.rabbitChannel = null;
    }

    async initialize() {
        try {
            // الاتصال بـ Redis
            await redisClient.connect();
            logger.info('Connected to Redis');

            // الاتصال بـ RabbitMQ
            const connection = await amqp.connect(RABBITMQ_URL);
            this.rabbitChannel = await connection.createChannel();
            
            // إعداد Exchange للإشعارات
            await this.rabbitChannel.assertExchange('gaara_notifications', 'topic', { durable: true });
            
            // إعداد Queue للاستماع للإشعارات
            const queue = await this.rabbitChannel.assertQueue('websocket_notifications', { durable: true });
            await this.rabbitChannel.bindQueue(queue.queue, 'gaara_notifications', 'notification.*');
            
            // الاستماع للرسائل من RabbitMQ
            this.rabbitChannel.consume(queue.queue, (msg) => {
                if (msg) {
                    this.handleRabbitMessage(msg);
                    this.rabbitChannel.ack(msg);
                }
            });

            logger.info('Connected to RabbitMQ and listening for notifications');
        } catch (error) {
            logger.error('Failed to initialize connections:', error);
            throw error;
        }
    }

    addConnection(ws, userId, connectionId) {
        const connectionInfo = {
            id: connectionId,
            userId: userId,
            ws: ws,
            lastPing: Date.now(),
            rooms: new Set(),
            metadata: {}
        };

        this.connections.set(connectionId, connectionInfo);
        
        if (!this.userConnections.has(userId)) {
            this.userConnections.set(userId, new Set());
        }
        this.userConnections.get(userId).add(connectionId);

        logger.info(`New connection added: ${connectionId} for user: ${userId}`);
        return connectionInfo;
    }

    removeConnection(connectionId) {
        const connection = this.connections.get(connectionId);
        if (connection) {
            const { userId, rooms } = connection;
            
            // إزالة من الغرف
            rooms.forEach(room => this.leaveRoom(connectionId, room));
            
            // إزالة من قائمة المستخدم
            if (this.userConnections.has(userId)) {
                this.userConnections.get(userId).delete(connectionId);
                if (this.userConnections.get(userId).size === 0) {
                    this.userConnections.delete(userId);
                }
            }
            
            this.connections.delete(connectionId);
            logger.info(`Connection removed: ${connectionId}`);
        }
    }

    joinRoom(connectionId, roomId) {
        const connection = this.connections.get(connectionId);
        if (connection) {
            connection.rooms.add(roomId);
            
            if (!this.roomConnections.has(roomId)) {
                this.roomConnections.set(roomId, new Set());
            }
            this.roomConnections.get(roomId).add(connectionId);
            
            logger.info(`Connection ${connectionId} joined room: ${roomId}`);
        }
    }

    leaveRoom(connectionId, roomId) {
        const connection = this.connections.get(connectionId);
        if (connection) {
            connection.rooms.delete(roomId);
            
            if (this.roomConnections.has(roomId)) {
                this.roomConnections.get(roomId).delete(connectionId);
                if (this.roomConnections.get(roomId).size === 0) {
                    this.roomConnections.delete(roomId);
                }
            }
            
            logger.info(`Connection ${connectionId} left room: ${roomId}`);
        }
    }

    sendToUser(userId, message) {
        const userConnections = this.userConnections.get(userId);
        if (userConnections) {
            userConnections.forEach(connectionId => {
                this.sendToConnection(connectionId, message);
            });
        }
    }

    sendToRoom(roomId, message, excludeConnectionId = null) {
        const roomConnections = this.roomConnections.get(roomId);
        if (roomConnections) {
            roomConnections.forEach(connectionId => {
                if (connectionId !== excludeConnectionId) {
                    this.sendToConnection(connectionId, message);
                }
            });
        }
    }

    sendToConnection(connectionId, message) {
        const connection = this.connections.get(connectionId);
        if (connection && connection.ws.readyState === WebSocket.OPEN) {
            try {
                connection.ws.send(JSON.stringify(message));
            } catch (error) {
                logger.error(`Failed to send message to connection ${connectionId}:`, error);
                this.removeConnection(connectionId);
            }
        }
    }

    broadcast(message, excludeConnectionId = null) {
        this.connections.forEach((connection, connectionId) => {
            if (connectionId !== excludeConnectionId) {
                this.sendToConnection(connectionId, message);
            }
        });
    }

    handleRabbitMessage(msg) {
        try {
            const notification = JSON.parse(msg.content.toString());
            const { type, target, data } = notification;

            switch (type) {
                case 'user_notification':
                    this.sendToUser(target, {
                        type: 'notification',
                        data: data
                    });
                    break;
                case 'room_notification':
                    this.sendToRoom(target, {
                        type: 'notification',
                        data: data
                    });
                    break;
                case 'broadcast':
                    this.broadcast({
                        type: 'notification',
                        data: data
                    });
                    break;
                default:
                    logger.warn(`Unknown notification type: ${type}`);
            }
        } catch (error) {
            logger.error('Failed to handle RabbitMQ message:', error);
        }
    }

    getStats() {
        return {
            totalConnections: this.connections.size,
            totalUsers: this.userConnections.size,
            totalRooms: this.roomConnections.size,
            connectionsByRoom: Array.from(this.roomConnections.entries()).map(([room, connections]) => ({
                room,
                count: connections.size
            }))
        };
    }
}

// إنشاء مدير الاتصالات
const connectionManager = new ConnectionManager();

// معالج اتصالات WebSocket
wss.on('connection', async (ws, req) => {
    try {
        // التحقق من Rate Limiting
        const clientIP = req.socket.remoteAddress;
        await rateLimiter.consume(clientIP);

        // استخراج معلومات المستخدم من الرمز المميز
        const url = new URL(req.url, 'http://localhost');
        const token = url.searchParams.get('token');
        const decoded = jwt.verify(token, JWT_SECRET);
        
        const userId = decoded.userId;
        const connectionId = uuidv4();

        // إضافة الاتصال
        const connectionInfo = connectionManager.addConnection(ws, userId, connectionId);

        // إرسال رسالة ترحيب
        ws.send(JSON.stringify({
            type: 'welcome',
            connectionId: connectionId,
            timestamp: new Date().toISOString()
        }));

        // معالج الرسائل الواردة
        ws.on('message', async (data) => {
            try {
                await rateLimiter.consume(clientIP);
                
                const message = JSON.parse(data);
                await handleMessage(connectionId, message);
            } catch (error) {
                if (error.remainingHits !== undefined) {
                    // Rate limit exceeded
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: 'Rate limit exceeded'
                    }));
                } else {
                    logger.error('Message handling error:', error);
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: 'Invalid message format'
                    }));
                }
            }
        });

        // معالج إغلاق الاتصال
        ws.on('close', () => {
            connectionManager.removeConnection(connectionId);
        });

        // معالج الأخطاء
        ws.on('error', (error) => {
            logger.error(`WebSocket error for connection ${connectionId}:`, error);
            connectionManager.removeConnection(connectionId);
        });

        // تحديث آخر ping
        connectionInfo.lastPing = Date.now();

    } catch (error) {
        logger.error('Connection setup error:', error);
        ws.close(1008, 'Authentication failed');
    }
});

// معالج الرسائل
async function handleMessage(connectionId, message) {
    const { type, data } = message;

    switch (type) {
        case 'ping':
            connectionManager.sendToConnection(connectionId, {
                type: 'pong',
                timestamp: new Date().toISOString()
            });
            break;

        case 'join_room':
            connectionManager.joinRoom(connectionId, data.roomId);
            connectionManager.sendToConnection(connectionId, {
                type: 'room_joined',
                roomId: data.roomId
            });
            break;

        case 'leave_room':
            connectionManager.leaveRoom(connectionId, data.roomId);
            connectionManager.sendToConnection(connectionId, {
                type: 'room_left',
                roomId: data.roomId
            });
            break;

        case 'room_message':
            connectionManager.sendToRoom(data.roomId, {
                type: 'room_message',
                roomId: data.roomId,
                message: data.message,
                sender: connectionId,
                timestamp: new Date().toISOString()
            }, connectionId);
            break;

        case 'private_message':
            connectionManager.sendToUser(data.targetUserId, {
                type: 'private_message',
                message: data.message,
                sender: connectionId,
                timestamp: new Date().toISOString()
            });
            break;

        default:
            logger.warn(`Unknown message type: ${type}`);
    }
}

// مراقبة الاتصالات وإزالة المنقطعة
setInterval(() => {
    const now = Date.now();
    const timeout = HEARTBEAT_INTERVAL * 2;

    connectionManager.connections.forEach((connection, connectionId) => {
        if (now - connection.lastPing > timeout) {
            logger.info(`Removing inactive connection: ${connectionId}`);
            connection.ws.close();
            connectionManager.removeConnection(connectionId);
        }
    });
}, HEARTBEAT_INTERVAL);

// نقاط النهاية HTTP
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'websocket',
        timestamp: new Date().toISOString(),
        connections: connectionManager.getStats()
    });
});

app.get('/stats', (req, res) => {
    res.json(connectionManager.getStats());
});

// بدء الخادم
async function startServer() {
    try {
        await connectionManager.initialize();
        
        server.listen(PORT, '0.0.0.0', () => {
            logger.info(`WebSocket server running on port ${PORT}`);
            logger.info(`Max connections: ${MAX_CONNECTIONS}`);
            logger.info(`Heartbeat interval: ${HEARTBEAT_INTERVAL}ms`);
        });
    } catch (error) {
        logger.error('Failed to start server:', error);
        process.exit(1);
    }
}

// معالجة إشارات النظام
process.on('SIGTERM', () => {
    logger.info('SIGTERM received, shutting down gracefully');
    server.close(() => {
        redisClient.quit();
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    logger.info('SIGINT received, shutting down gracefully');
    server.close(() => {
        redisClient.quit();
        process.exit(0);
    });
});

// بدء الخادم
startServer();

