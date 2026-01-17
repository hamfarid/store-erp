#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 إضافة نقطة نهاية لوحة التحكم
Add Dashboard Endpoint

هذا السكريبت يقوم بإضافة نقطة نهاية لوحة التحكم المفقودة
"""

import os

def add_dashboard_endpoint():
    """إضافة نقطة نهاية لوحة التحكم إلى الخادم الخلفي"""
    print("📊 إضافة نقطة نهاية لوحة التحكم...")
    
    backend_file = "backend/enhanced_simple_app.py"
    
    try:
        # قراءة محتوى الملف
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن نقطة إدراج مناسبة (قبل نهاية الملف)
        dashboard_endpoint = '''
# نقطة نهاية لوحة التحكم
@app.route('/api/reports/dashboard', methods=['GET'])
def get_dashboard():
    """الحصول على بيانات لوحة التحكم"""
    try:
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()
        
        # إحصائيات أساسية
        stats = {}
        
        # عدد المنتجات
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
        stats['total_products'] = cursor.fetchone()[0]
        
        # عدد الفئات
        cursor.execute("SELECT COUNT(*) FROM categories")
        stats['total_categories'] = cursor.fetchone()[0]
        
        # عدد المستودعات
        cursor.execute("SELECT COUNT(*) FROM warehouses")
        stats['total_warehouses'] = cursor.fetchone()[0]
        
        # عدد المستخدمين النشطين
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        stats['active_users'] = cursor.fetchone()[0]
        
        # المنتجات منخفضة المخزون
        cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= min_quantity AND is_active = 1")
        stats['low_stock_products'] = cursor.fetchone()[0]
        
        # إجمالي قيمة المخزون
        cursor.execute("SELECT SUM(quantity * cost) FROM products WHERE is_active = 1")
        total_value = cursor.fetchone()[0]
        stats['total_inventory_value'] = total_value if total_value else 0
        
        # أحدث المنتجات المضافة
        cursor.execute("""
            SELECT name, sku, quantity, created_at 
            FROM products 
            WHERE is_active = 1 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_products = []
        for row in cursor.fetchall():
            recent_products.append({
                'name': row[0],
                'sku': row[1],
                'quantity': row[2],
                'created_at': row[3]
            })
        
        # المنتجات منخفضة المخزون (تفصيلي)
        cursor.execute("""
            SELECT name, sku, quantity, min_quantity 
            FROM products 
            WHERE quantity <= min_quantity AND is_active = 1 
            ORDER BY quantity ASC 
            LIMIT 10
        """)
        low_stock_details = []
        for row in cursor.fetchall():
            low_stock_details.append({
                'name': row[0],
                'sku': row[1],
                'current_quantity': row[2],
                'min_quantity': row[3]
            })
        
        conn.close()
        
        dashboard_data = {
            'success': True,
            'data': {
                'statistics': stats,
                'recent_products': recent_products,
                'low_stock_products': low_stock_details,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'خطأ في الحصول على بيانات لوحة التحكم: {str(e)}'
        }), 500
'''
        
        # البحث عن نقطة الإدراج (قبل if __name__ == '__main__':)
        if "if __name__ == '__main__':" in content:
            # إدراج نقطة النهاية قبل الجزء الرئيسي
            content = content.replace("if __name__ == '__main__':", 
                                    dashboard_endpoint + "\n\nif __name__ == '__main__':")
        else:
            # إضافة في نهاية الملف
            content += dashboard_endpoint
        
        # كتابة المحتوى المحدث
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ تم إضافة نقطة نهاية لوحة التحكم بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة نقطة نهاية لوحة التحكم: {e}")
        return False

def test_dashboard_endpoint():
    """اختبار نقطة نهاية لوحة التحكم"""
    print("\n🧪 اختبار نقطة نهاية لوحة التحكم...")
    
    import requests
    
    try:
        response = requests.get('http://localhost:5002/api/reports/dashboard', timeout=10)
        
        print(f"   رمز الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ نقطة نهاية لوحة التحكم تعمل بنجاح!")
            
            if 'data' in data and 'statistics' in data['data']:
                stats = data['data']['statistics']
                print(f"   إجمالي المنتجات: {stats.get('total_products', 0)}")
                print(f"   إجمالي الفئات: {stats.get('total_categories', 0)}")
                print(f"   المستخدمين النشطين: {stats.get('active_users', 0)}")
            
            return True
        else:
            print(f"❌ فشل في الوصول لنقطة نهاية لوحة التحكم: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار نقطة نهاية لوحة التحكم: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("📊 بدء إضافة نقطة نهاية لوحة التحكم")
    print("=" * 50)
    
    if add_dashboard_endpoint():
        print("\n🔄 إعادة تشغيل الخادم الخلفي مطلوبة لتطبيق التغييرات...")
        print("   يرجى إعادة تشغيل الخادم الخلفي ثم اختبار نقطة النهاية")
    else:
        print("\n❌ فشل في إضافة نقطة نهاية لوحة التحكم")

if __name__ == "__main__":
    main()
