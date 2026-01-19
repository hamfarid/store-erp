from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# تعيين مسارات الملفات الثابتة والقوالب
template_dir = os.path.abspath('/home/ubuntu/agricultural_ai_system/gaara_erp/src/templates')
static_dir = os.path.abspath('/home/ubuntu/agricultural_ai_system/gaara_erp/src/static')

# إنشاء مجلد للملفات الثابتة إذا لم يكن موجوداً
os.makedirs(static_dir, exist_ok=True)
os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
os.makedirs(os.path.join(static_dir, 'images'), exist_ok=True)

# تكوين Flask لاستخدام مجلد القوالب المخصص
app.template_folder = template_dir

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/nursery')
def nursery_management():
    return render_template('nursery_management.html')

@app.route('/templates/components/<path:filename>')
def serve_component(filename):
    return send_from_directory(os.path.join(template_dir, 'components'), filename)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(static_dir, path)

# إضافة صورة الشعار الافتراضية
@app.route('/create_default_logo')
def create_default_logo():
    logo_path = os.path.join(static_dir, 'images', 'logo.png')
    if not os.path.exists(logo_path):
        # إنشاء صورة شعار بسيطة باستخدام PIL
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGBA', (200, 80), color=(255, 255, 255, 0))
            d = ImageDraw.Draw(img)
            d.rectangle([(0, 0), (200, 80)], outline=(52, 152, 219), width=2)
            d.text((40, 30), "Gaara ERP", fill=(52, 152, 219))
            img.save(logo_path)
            return "تم إنشاء الشعار الافتراضي"
        except ImportError:
            # إذا لم تكن مكتبة PIL متاحة، نستخدم نصاً بسيطاً
            with open(logo_path, 'w') as f:
                f.write("Gaara ERP Logo")
            return "تم إنشاء ملف الشعار الافتراضي (نص)"
    return "الشعار موجود بالفعل"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2050, debug=True)
