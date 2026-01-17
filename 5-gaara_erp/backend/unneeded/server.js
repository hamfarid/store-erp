#!/usr/bin/env node
/**
 * خادم Node.js بسيط لنظام إدارة المخزون
 */

const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const PORT = 8000;
const HOST = '0.0.0.0';

// بيانات تجريبية
const sampleData = {
    products: [
        { id: 1, name: 'بذور طماطم', category: 'بذور', stock: 100, price: 25.50, supplier: 'شركة البذور المصرية' },
        { id: 2, name: 'سماد NPK', category: 'أسمدة', stock: 75, price: 45.00, supplier: 'شركة الأسمدة الحديثة' },
        { id: 3, name: 'مبيد حشري', category: 'مبيدات', stock: 50, price: 85.00, supplier: 'شركة المبيدات المتقدمة' },
        { id: 4, name: 'بذور خيار', category: 'بذور', stock: 120, price: 30.00, supplier: 'شركة البذور المصرية' },
        { id: 5, name: 'سماد عضوي', category: 'أسمدة', stock: 200, price: 20.00, supplier: 'المزارع العضوية' }
    ],
    
    inventory: {
        totalProducts: 5,
        totalStock: 545,
        totalValue: 23275.0,
        lowStockItems: 1,
        categories: ['بذور', 'أسمدة', 'مبيدات']
    },
    
    reports: {
        dailySales: 1250.0,
        weeklySales: 8750.0,
        monthlySales: 35000.0,
        topProducts: [
            { name: 'بذور طماطم', sales: 2550.0, quantity: 100 },
            { name: 'سماد NPK', sales: 2250.0, quantity: 50 },
            { name: 'مبيد حشري', sales: 1700.0, quantity: 20 }
        ],
        lowStockAlerts: [
            { name: 'مبيد حشري', currentStock: 50, minStock: 75, status: 'تحذير' }
        ]
    }
};

// دالة إرسال استجابة JSON
function sendJSON(res, data, statusCode = 200) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end(JSON.stringify(data, null, 2));
}

// دالة إرسال HTML
function sendHTML(res, html) {
    res.writeHead(200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
    });
    res.end(html);
}

// الصفحة الرئيسية
function getHomePage() {
    return `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>نظام إدارة المخزون الزراعي</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
            .header h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
            .header p { color: #7f8c8d; font-size: 1.2em; }
            .status { background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(39,174,96,0.3); }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); transition: transform 0.3s ease; }
            .card:hover { transform: translateY(-5px); }
            .card h3 { color: #2c3e50; margin-bottom: 15px; font-size: 1.3em; }
            .api-item { margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db; }
            .method { background: #3498db; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .endpoint { font-family: 'Courier New', monospace; color: #2c3e50; margin: 0 10px; }
            .description { color: #7f8c8d; font-size: 0.9em; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
            .stat { background: linear-gradient(45deg, #3498db, #2980b9); color: white; padding: 20px; border-radius: 10px; text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; display: block; }
            .stat-label { font-size: 0.9em; opacity: 0.9; }
            .footer { text-align: center; color: rgba(255,255,255,0.8); margin-top: 30px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 نظام إدارة المخزون الزراعي</h1>
                <p>نظام متكامل لإدارة المخزون والمنتجات الزراعية</p>
            </div>
            
            <div class="status">
                <h2>✅ النظام يعمل بنجاح!</h2>
                <p>تم تشغيل الخادم في ${new Date().toLocaleString('ar-EG')}</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>📊 إحصائيات سريعة</h3>
                    <div class="stats">
                        <div class="stat">
                            <span class="stat-number">${sampleData.inventory.totalProducts}</span>
                            <span class="stat-label">منتجات</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">${sampleData.inventory.totalStock}</span>
                            <span class="stat-label">إجمالي المخزون</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">${sampleData.inventory.totalValue.toLocaleString()}</span>
                            <span class="stat-label">القيمة (جنيه)</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🔗 APIs المتاحة</h3>
                    <div class="api-item">
                        <span class="method">GET</span>
                        <span class="endpoint">/health</span>
                        <div class="description">فحص حالة النظام</div>
                    </div>
                    <div class="api-item">
                        <span class="method">GET</span>
                        <span class="endpoint">/api/products</span>
                        <div class="description">قائمة المنتجات</div>
                    </div>
                    <div class="api-item">
                        <span class="method">GET</span>
                        <span class="endpoint">/api/inventory</span>
                        <div class="description">حالة المخزون</div>
                    </div>
                    <div class="api-item">
                        <span class="method">GET</span>
                        <span class="endpoint">/api/reports</span>
                        <div class="description">التقارير والإحصائيات</div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>نظام إدارة المخزون الزراعي - تم التطوير بنجاح ✨</p>
            </div>
        </div>
    </body>
    </html>
    `;
}

// معالج الطلبات
function handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    const method = req.method;
    
    console.log(`[${new Date().toISOString()}] ${method} ${pathname}`);
    
    // معالجة CORS
    if (method === 'OPTIONS') {
        res.writeHead(200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        });
        res.end();
        return;
    }
    
    // المسارات
    switch (pathname) {
        case '/':
            sendHTML(res, getHomePage());
            break;
            
        case '/health':
            sendJSON(res, {
                status: 'healthy',
                message: 'نظام إدارة المخزون يعمل بنجاح',
                timestamp: new Date().toISOString(),
                version: '1.0.0',
                uptime: process.uptime()
            });
            break;
            
        case '/api/products':
            sendJSON(res, {
                success: true,
                data: sampleData.products,
                total: sampleData.products.length,
                message: 'تم جلب المنتجات بنجاح'
            });
            break;
            
        case '/api/inventory':
            sendJSON(res, {
                success: true,
                data: sampleData.inventory,
                message: 'تم جلب حالة المخزون بنجاح'
            });
            break;
            
        case '/api/reports':
            sendJSON(res, {
                success: true,
                data: sampleData.reports,
                message: 'تم جلب التقارير بنجاح'
            });
            break;
            
        default:
            sendJSON(res, {
                success: false,
                error: 'المسار غير موجود',
                message: 'الرجاء التحقق من المسار المطلوب'
            }, 404);
    }
}

// إنشاء وتشغيل الخادم
const server = http.createServer(handleRequest);

server.listen(PORT, HOST, () => {
    console.log('🚀 تم تشغيل نظام إدارة المخزون بنجاح!');
    console.log('=' * 50);
    console.log(`🔗 رابط النظام: http://localhost:${PORT}`);
    console.log(`📋 فحص الحالة: http://localhost:${PORT}/health`);
    console.log(`📦 المنتجات: http://localhost:${PORT}/api/products`);
    console.log(`📊 المخزون: http://localhost:${PORT}/api/inventory`);
    console.log(`📈 التقارير: http://localhost:${PORT}/api/reports`);
    console.log(`⏰ وقت التشغيل: ${new Date().toLocaleString('ar-EG')}`);
    console.log('=' * 50);
    console.log('اضغط Ctrl+C لإيقاف الخادم');
    console.log('=' * 50);
});

server.on('error', (err) => {
    console.error('❌ خطأ في تشغيل الخادم:', err.message);
});

process.on('SIGINT', () => {
    console.log('\n🛑 تم إيقاف الخادم بواسطة المستخدم');
    server.close(() => {
        console.log('✅ تم إغلاق الخادم بنجاح');
        process.exit(0);
    });
});
