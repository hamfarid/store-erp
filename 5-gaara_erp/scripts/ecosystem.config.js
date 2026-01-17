// 🏪 نظام إدارة المخزون الكامل - إعدادات PM2
// Complete Inventory Management System - PM2 Ecosystem Configuration

module.exports = {
  apps: [
    {
      // Backend Application
      name: 'inventory-backend',
      cwd: '/var/www/inventory_system/backend',
      script: 'venv/bin/python',
      args: 'src/main.py',
      
      // Environment variables
      env: {
        NODE_ENV: 'production',
        FLASK_ENV: 'production',
        FLASK_DEBUG: 'False',
        PORT: 8000,
        HOST: '127.0.0.1',
        DATABASE_URL: 'sqlite:///instance/inventory.db',
        SECRET_KEY: 'your-production-secret-key-change-this',
        JWT_SECRET_KEY: 'your-jwt-secret-key-change-this',
        CORS_ORIGINS: 'https://your-domain.com',
        MAX_CONTENT_LENGTH: '50MB',
        UPLOAD_FOLDER: '/var/www/inventory_system/uploads',
        LOG_LEVEL: 'INFO',
        TIMEZONE: 'Asia/Riyadh',
        LANGUAGE: 'ar'
      },
      
      // Development environment (for testing)
      env_development: {
        NODE_ENV: 'development',
        FLASK_ENV: 'development',
        FLASK_DEBUG: 'True',
        PORT: 8000,
        HOST: '127.0.0.1',
        LOG_LEVEL: 'DEBUG'
      },
      
      // Staging environment
      env_staging: {
        NODE_ENV: 'staging',
        FLASK_ENV: 'staging',
        FLASK_DEBUG: 'False',
        PORT: 8000,
        HOST: '127.0.0.1',
        LOG_LEVEL: 'INFO'
      },
      
      // Process management
      instances: 1, // Single instance for SQLite
      exec_mode: 'fork', // Fork mode for Python
      autorestart: true,
      watch: false, // Disable watch in production
      max_memory_restart: '1G',
      
      // Restart settings
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      
      // Logging
      log_file: '/var/log/pm2/inventory-backend-combined.log',
      out_file: '/var/log/pm2/inventory-backend-out.log',
      error_file: '/var/log/pm2/inventory-backend-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true,
      
      // Advanced settings
      kill_timeout: 5000,
      listen_timeout: 3000,
      
      // Health monitoring
      health_check_grace_period: 3000,
      
      // Source map support (if needed)
      source_map_support: false,
      
      // Node.js specific (not needed for Python but kept for reference)
      node_args: [],
      
      // Custom settings
      interpreter: '/var/www/inventory_system/backend/venv/bin/python',
      interpreter_args: '-u', // Unbuffered output
      
      // Cron restart (optional - restart daily at 3 AM)
      cron_restart: '0 3 * * *',
      
      // Environment file (optional)
      env_file: '/var/www/inventory_system/backend/.env'
    }
  ],

  // Deployment configuration
  deploy: {
    production: {
      user: 'inventory',
      host: 'your-server-ip',
      ref: 'origin/main',
      repo: 'https://github.com/your-username/inventory-system.git',
      path: '/var/www/inventory_system',
      'pre-deploy-local': '',
      'post-deploy': 'cd backend && source venv/bin/activate && pip install -r requirements.txt && cd ../frontend && npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': '',
      'ssh_options': 'ForwardAgent=yes'
    },
    
    staging: {
      user: 'inventory',
      host: 'staging-server-ip',
      ref: 'origin/develop',
      repo: 'https://github.com/your-username/inventory-system.git',
      path: '/var/www/inventory_system_staging',
      'post-deploy': 'cd backend && source venv/bin/activate && pip install -r requirements.txt && cd ../frontend && npm install && npm run build && pm2 reload ecosystem.config.js --env staging'
    }
  },

  // Global PM2 settings
  pmx: {
    enabled: true,
    network: true,
    ports: true,
    
    // Custom metrics
    custom_probes: [
      {
        name: 'CPU usage',
        probe: function() {
          return process.cpuUsage();
        }
      },
      {
        name: 'Memory usage',
        probe: function() {
          return process.memoryUsage();
        }
      }
    ],
    
    // Network monitoring
    network_timeout: 5000,
    
    // Port monitoring
    ports_timeout: 5000
  }
};

// Additional configuration for monitoring
const monitoringConfig = {
  // Log rotation settings
  logRotate: {
    max_size: '10M',
    retain: 30,
    compress: true,
    dateFormat: 'YYYY-MM-DD_HH-mm-ss'
  },
  
  // Performance monitoring
  monitoring: {
    cpu_threshold: 80,
    memory_threshold: 80,
    disk_threshold: 85,
    response_time_threshold: 5000
  },
  
  // Alerts configuration
  alerts: {
    email: {
      enabled: false,
      smtp_host: 'smtp.gmail.com',
      smtp_port: 587,
      username: 'your-email@gmail.com',
      password: 'your-app-password',
      to: ['admin@your-domain.com']
    },
    
    webhook: {
      enabled: false,
      url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
    }
  }
};

// Export monitoring config for external use
module.exports.monitoring = monitoringConfig;
