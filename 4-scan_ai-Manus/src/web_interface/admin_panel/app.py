from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, SystemSettings
import os
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///admin_panel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            user.last_login = datetime.utcnow()
            user.failed_login_attempts = 0
            db.session.commit()
            return redirect(url_for('dashboard'))

        flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'error')

    return render_template('login.html')


@app.route('/ai')
@login_required
def ai():
    return render_template('ai.html')


@app.route('/resources')
@login_required
def resources():
    return render_template('resources.html')


@app.route('/usage')
@login_required
def usage():
    return render_template('usage.html')


@app.route('/diagnosis')
@login_required
def diagnosis():
    return render_template('diagnosis.html')


@app.route('/alerts')
@login_required
def alerts():
    return render_template('alerts.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    # Check if setup is already completed
    if current_app.config.get('SETUP_COMPLETED', False):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            # Get form data
            system_name = request.form.get('system_name')
            admin_email = request.form.get('admin_email')
            admin_password = request.form.get('admin_password')
            language = request.form.get('language')
            timezone = request.form.get('timezone')
            date_format = request.form.get('date_format')
            session_timeout = int(request.form.get('session_timeout'))
            max_login_attempts = int(request.form.get('max_login_attempts'))
            password_expiry = int(request.form.get('password_expiry'))
            enable_2fa = request.form.get('enable_2fa') == 'on'

            # Create admin user
            admin_user = User(
                email=admin_email,
                password=generate_password_hash(admin_password),
                role='admin',
                is_active=True
            )
            db.session.add(admin_user)

            # Save system settings
            settings = SystemSettings(
                system_name=system_name,
                language=language,
                timezone=timezone,
                date_format=date_format,
                session_timeout=session_timeout,
                max_login_attempts=max_login_attempts,
                password_expiry=password_expiry,
                enable_2fa=enable_2fa
            )
            db.session.add(settings)

            # Mark setup as completed
            current_app.config['SETUP_COMPLETED'] = True

            # Commit changes
            db.session.commit()

            flash('تم إكمال إعداد النظام بنجاح', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء إعداد النظام: {str(e)}', 'error')
            return redirect(url_for('setup'))

    return render_template('setup.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
