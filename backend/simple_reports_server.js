#!/usr/bin/env node

/**
 * خادم بسيط للتقارير باستخدام Node.js
 */

const http = require('http');
const url = require('url');

const PORT = 8005;

// بيانات تجريبية للتقارير
const reportsData = {
    sales: {
        success: true,
        sales_report: {
            total_sales: 125000.0,
            total_profit: 35000.0,
            profit_margin: 28.0,
            monthly_data: [
                {
                    month: 'يناير 2025',
                    sales: 45000.0,
                    profit: 12000.0,
                    transactions: 85
                },
                {
                    month: 'فبراير 2025',
                    sales: 52000.0,
                    profit: 15000.0,
                    transactions: 92
                },
                {
                    month: 'مارس 2025',
                    sales: 28000.0,
                    profit: 8000.0,
                    transactions: 67
                }
            ],
            top_products: [
                {
                    name: 'بذور طماطم هجين سوبر',
                    sales: 25000.0,
                    quantity: 714,
                    profit: 7000.0
                },
                {
                    name: 'سماد NPK متوازن',
                    sales: 18000.0,
                    quantity: 300,
                    profit: 4500.0
                },
                {
                    name: 'مبيد حشري عام',
                    sales: 15000.0,
                    quantity: 100,
                    profit: 3000.0
                }
            ]
        }
    },
    profitLoss: {
        success: true,
        profit_loss: {
            period: 'الربع الأول 2025',
            total_revenue: 125000.0,
            total_costs: 90000.0,
            gross_profit: 35000.0,
            operating_expenses: 15000.0,
            net_profit: 20000.0,
            profit_margin: 16.0,
            breakdown: {
                sales_revenue: 125000.0,
                cost_of_goods: 90000.0,
                marketing_expenses: 5000.0,
                administrative_expenses: 7000.0,
                other_expenses: 3000.0
            },
            monthly_breakdown: [
                {
                    month: 'يناير',
                    revenue: 45000.0,
                    costs: 32000.0,
                    profit: 13000.0
                },
                {
                    month: 'فبراير',
                    revenue: 52000.0,
                    costs: 37000.0,
                    profit: 15000.0
                },
                {
                    month: 'مارس',
                    revenue: 28000.0,
                    costs: 21000.0,
                    profit: 7000.0
                }
            ]
        }
    }
};

// إعداد CORS headers
function setCorsHeaders(res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
}

// إنشاء الخادم
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const method = req.method;

    // معالجة طلبات OPTIONS للـ CORS
    if (method === 'OPTIONS') {
        res.writeHead(200);
        setCorsHeaders(res);
        res.end();
        return;
    }

    // إعداد CORS headers لجميع الطلبات
    setCorsHeaders(res);

    // معالجة الطلبات
    if (method === 'GET') {
        if (path === '/api/health') {
            res.writeHead(200);
            res.end(JSON.stringify({
                status: 'healthy',
                message: 'خادم التقارير يعمل بنجاح',
                timestamp: new Date().toISOString(),
                version: '1.0.0'
            }));
        } else if (path === '/api/reports/sales') {
            res.writeHead(200);
            res.end(JSON.stringify(reportsData.sales));
        } else if (path === '/api/reports/profit-loss') {
            res.writeHead(200);
            res.end(JSON.stringify(reportsData.profitLoss));
        } else if (path === '/api/products') {
            res.writeHead(200);
            res.end(JSON.stringify({
                success: true,
                products: [
                    {
                        id: 1,
                        name: 'بذور طماطم هجين سوبر',
                        sku: 'TOM-HYB-001',
                        category: 'بذور',
                        sale_price: 35.0,
                        current_stock: 150.0,
                        unit: 'كيس'
                    },
                    {
                        id: 2,
                        name: 'سماد NPK متوازن',
                        sku: 'NPK-BAL-001',
                        category: 'أسمدة',
                        sale_price: 60.0,
                        current_stock: 75.0,
                        unit: 'كيس 25 كيلو'
                    }
                ],
                count: 2
            }));
        } else {
            res.writeHead(404);
            res.end(JSON.stringify({
                success: false,
                error: 'API غير موجود'
            }));
        }
    } else if (method === 'POST') {
        if (path === '/api/auth/login') {
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            req.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    if (data.username === 'admin' && data.password=os.getenv('ADMIN_PASSWORD', 'change_me')) {
                        res.writeHead(200);
                        res.end(JSON.stringify({
                            success: true,
                            message: 'تم تسجيل الدخول بنجاح',
                            token: `token_${data.username}_${Date.now()}`,
                            user: {
                                id: 1,
                                username: data.username,
                                name: 'مدير النظام',
                                role: 'admin'
                            }
                        }));
                    } else {
                        res.writeHead(401);
                        res.end(JSON.stringify({
                            success: false,
                            error: 'اسم المستخدم أو كلمة المرور غير صحيحة'
                        }));
                    }
                } catch (error) {
                    res.writeHead(400);
                    res.end(JSON.stringify({
                        success: false,
                        error: 'خطأ في البيانات المرسلة'
                    }));
                }
            });
        } else {
            res.writeHead(404);
            res.end(JSON.stringify({
                success: false,
                error: 'API غير موجود'
            }));
        }
    } else {
        res.writeHead(405);
        res.end(JSON.stringify({
            success: false,
            error: 'طريقة غير مدعومة'
        }));
    }
});

// تشغيل الخادم
server.listen(PORT, () => {
    console.log('🚀 بدء تشغيل خادم التقارير...');
    console.log(`🔗 الخادم متاح على: http://localhost:${PORT}`);
    console.log('=' * 50);
    console.log('📋 APIs المتاحة:');
    console.log('   • فحص الحالة: GET /api/health');
    console.log('   • تسجيل الدخول: POST /api/auth/login');
    console.log('   • المنتجات: GET /api/products');
    console.log('   • تقارير المبيعات: GET /api/reports/sales');
    console.log('   • تقارير الأرباح والخسائر: GET /api/reports/profit-loss');
    console.log('=' * 50);
    console.log('🔐 بيانات الدخول: admin / admin123');
    console.log('=' * 50);
});

// معالجة إيقاف الخادم
process.on('SIGINT', () => {
    console.log('\n🛑 تم إيقاف خادم التقارير');
    server.close();
    process.exit(0);
});
