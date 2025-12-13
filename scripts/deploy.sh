#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت النشر لخادم Contabo
# Complete Inventory Management System - Contabo Server Deployment Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="your-domain.com"  # Replace with your domain
APP_NAME="inventory_system"
APP_USER="inventory"
APP_DIR="/var/www/$APP_NAME"
NGINX_CONF="/etc/nginx/sites-available/$APP_NAME"
SSL_EMAIL="admin@$DOMAIN"  # Replace with your email

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "يرجى تشغيل هذا السكريبت كمستخدم root"
        print_error "Please run this script as root"
        exit 1
    fi
}

# Function to update system packages
update_system() {
    print_status "تحديث حزم النظام..."
    print_status "Updating system packages..."
    
    apt update && apt upgrade -y
    apt install -y curl wget git unzip software-properties-common
    
    print_success "تم تحديث النظام بنجاح"
    print_success "System updated successfully"
}

# Function to install Node.js
install_nodejs() {
    print_status "تثبيت Node.js..."
    print_status "Installing Node.js..."
    
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt install -y nodejs
    
    # Install PM2 globally
    npm install -g pm2
    
    print_success "تم تثبيت Node.js و PM2 بنجاح"
    print_success "Node.js and PM2 installed successfully"
}

# Function to install Python
install_python() {
    print_status "تثبيت Python..."
    print_status "Installing Python..."
    
    apt install -y python3 python3-pip python3-venv python3-dev
    
    print_success "تم تثبيت Python بنجاح"
    print_success "Python installed successfully"
}

# Function to install Nginx
install_nginx() {
    print_status "تثبيت Nginx..."
    print_status "Installing Nginx..."
    
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    
    print_success "تم تثبيت Nginx بنجاح"
    print_success "Nginx installed successfully"
}

# Function to install SSL certificate
install_ssl() {
    print_status "تثبيت شهادة SSL..."
    print_status "Installing SSL certificate..."
    
    # Install Certbot
    apt install -y certbot python3-certbot-nginx
    
    # Get SSL certificate
    certbot --nginx -d $DOMAIN --email $SSL_EMAIL --agree-tos --non-interactive
    
    print_success "تم تثبيت شهادة SSL بنجاح"
    print_success "SSL certificate installed successfully"
}

# Function to create application user
create_app_user() {
    print_status "إنشاء مستخدم التطبيق..."
    print_status "Creating application user..."
    
    if ! id "$APP_USER" &>/dev/null; then
        useradd -m -s /bin/bash $APP_USER
        usermod -aG sudo $APP_USER
        print_success "تم إنشاء المستخدم $APP_USER"
        print_success "User $APP_USER created"
    else
        print_warning "المستخدم $APP_USER موجود بالفعل"
        print_warning "User $APP_USER already exists"
    fi
}

# Function to setup application directory
setup_app_directory() {
    print_status "إعداد مجلد التطبيق..."
    print_status "Setting up application directory..."
    
    mkdir -p $APP_DIR
    chown -R $APP_USER:$APP_USER $APP_DIR
    chmod 755 $APP_DIR
    
    print_success "تم إعداد مجلد التطبيق"
    print_success "Application directory setup complete"
}

# Function to deploy application
deploy_application() {
    print_status "نشر التطبيق..."
    print_status "Deploying application..."
    
    # Copy application files
    cp -r . $APP_DIR/
    chown -R $APP_USER:$APP_USER $APP_DIR
    
    # Setup backend
    cd $APP_DIR/backend
    sudo -u $APP_USER python3 -m venv venv
    sudo -u $APP_USER ./venv/bin/pip install -r requirements.txt
    
    # Setup frontend
    cd $APP_DIR/frontend
    sudo -u $APP_USER npm install
    sudo -u $APP_USER npm run build
    
    print_success "تم نشر التطبيق بنجاح"
    print_success "Application deployed successfully"
}

# Function to configure Nginx
configure_nginx() {
    print_status "تكوين Nginx..."
    print_status "Configuring Nginx..."
    
    cat > $NGINX_CONF << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend (React build)
    location / {
        root $APP_DIR/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Logs
    access_log /var/log/nginx/${APP_NAME}_access.log;
    error_log /var/log/nginx/${APP_NAME}_error.log;
}
EOF

    # Enable site
    ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
    
    # Test configuration
    nginx -t
    
    # Reload Nginx
    systemctl reload nginx
    
    print_success "تم تكوين Nginx بنجاح"
    print_success "Nginx configured successfully"
}

# Function to setup PM2
setup_pm2() {
    print_status "إعداد PM2..."
    print_status "Setting up PM2..."
    
    # Create PM2 ecosystem file
    cat > $APP_DIR/ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: '$APP_NAME-backend',
    cwd: '$APP_DIR/backend',
    script: 'venv/bin/python',
    args: 'src/main.py',
    env: {
      FLASK_ENV: 'production',
      PORT: 8000
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: '/var/log/pm2/${APP_NAME}-error.log',
    out_file: '/var/log/pm2/${APP_NAME}-out.log',
    log_file: '/var/log/pm2/${APP_NAME}-combined.log',
    time: true
  }]
};
EOF

    # Create log directory
    mkdir -p /var/log/pm2
    chown -R $APP_USER:$APP_USER /var/log/pm2

    # Start application with PM2
    sudo -u $APP_USER pm2 start $APP_DIR/ecosystem.config.js
    sudo -u $APP_USER pm2 save
    
    # Setup PM2 startup
    pm2 startup systemd -u $APP_USER --hp /home/$APP_USER
    
    print_success "تم إعداد PM2 بنجاح"
    print_success "PM2 setup complete"
}

# Function to setup firewall
setup_firewall() {
    print_status "إعداد جدار الحماية..."
    print_status "Setting up firewall..."
    
    ufw --force enable
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 'Nginx Full'
    
    print_success "تم إعداد جدار الحماية بنجاح"
    print_success "Firewall setup complete"
}

# Function to setup monitoring
setup_monitoring() {
    print_status "إعداد المراقبة..."
    print_status "Setting up monitoring..."
    
    # Install htop and other monitoring tools
    apt install -y htop iotop nethogs
    
    # Setup log rotation
    cat > /etc/logrotate.d/$APP_NAME << EOF
/var/log/nginx/${APP_NAME}_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload nginx
    endscript
}

/var/log/pm2/${APP_NAME}-*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $APP_USER $APP_USER
    postrotate
        sudo -u $APP_USER pm2 reloadLogs
    endscript
}
EOF

    print_success "تم إعداد المراقبة بنجاح"
    print_success "Monitoring setup complete"
}

# Main deployment function
main() {
    print_status "🚀 بدء نشر نظام إدارة المخزون على خادم Contabo..."
    print_status "🚀 Starting inventory system deployment on Contabo server..."
    
    # Check if running as root
    check_root
    
    # Update system
    update_system
    
    # Install dependencies
    install_nodejs
    install_python
    install_nginx
    
    # Create application user
    create_app_user
    
    # Setup application
    setup_app_directory
    deploy_application
    
    # Configure services
    configure_nginx
    setup_pm2
    
    # Security and monitoring
    setup_firewall
    setup_monitoring
    
    # Install SSL (optional, requires domain)
    if [ "$DOMAIN" != "your-domain.com" ]; then
        install_ssl
    else
        print_warning "تم تخطي تثبيت SSL - يرجى تحديث DOMAIN في السكريبت"
        print_warning "SSL installation skipped - please update DOMAIN in script"
    fi
    
    print_success "🎉 تم نشر النظام بنجاح!"
    print_success "🎉 System deployed successfully!"
    
    echo ""
    print_status "معلومات النشر:"
    print_status "Deployment information:"
    echo ""
    print_status "  التطبيق: $APP_DIR"
    print_status "  Application: $APP_DIR"
    print_status "  المستخدم: $APP_USER"
    print_status "  User: $APP_USER"
    print_status "  الدومين: $DOMAIN"
    print_status "  Domain: $DOMAIN"
    echo ""
    print_status "أوامر مفيدة:"
    print_status "Useful commands:"
    print_status "  sudo -u $APP_USER pm2 status"
    print_status "  sudo -u $APP_USER pm2 logs"
    print_status "  sudo -u $APP_USER pm2 restart $APP_NAME-backend"
    print_status "  systemctl status nginx"
    print_status "  certbot renew --dry-run"
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "update")
        print_status "تحديث التطبيق..."
        print_status "Updating application..."
        
        # Stop PM2
        sudo -u $APP_USER pm2 stop $APP_NAME-backend
        
        # Update code
        deploy_application
        
        # Restart PM2
        sudo -u $APP_USER pm2 start $APP_NAME-backend
        
        print_success "تم تحديث التطبيق بنجاح"
        print_success "Application updated successfully"
        ;;
    "status")
        print_status "حالة الخدمات:"
        print_status "Service status:"
        
        echo "PM2:"
        sudo -u $APP_USER pm2 status
        
        echo ""
        echo "Nginx:"
        systemctl status nginx --no-pager
        
        echo ""
        echo "Firewall:"
        ufw status
        ;;
    *)
        echo "Usage: $0 {deploy|update|status}"
        echo "الاستخدام: $0 {deploy|update|status}"
        exit 1
        ;;
esac
