
from flask import request, abort

class ScannerBlocker:
    """
    Middleware to block automated scanners and malicious access patterns
    """
    
    BLOCKED_USER_AGENTS = [
        'nikto', 'sqlmap', 'nmap', 'nessus', 'arachni', 'acunetix',
        'netsparker', 'burp', 'metasploit', 'w3af', 'zaproxy'
    ]
    
    BLOCKED_PATHS = [
        '/.env', '/.git', '/.svn', '/wp-admin', '/wp-login',
        '/phpmyadmin', '/admin.php', '/config.php', '/.ds_store'
    ]

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def check_scanner():
            # Check User-Agent
            user_agent = request.headers.get('User-Agent', '').lower()
            for agent in self.BLOCKED_USER_AGENTS:
                if agent in user_agent:
                    # Log attempt (in production use real logger)
                    print(f"🚫 Blocked scanner User-Agent: {agent} from {request.remote_addr}")
                    abort(403)
            
            # Check Path
            path = request.path.lower()
            for blocked in self.BLOCKED_PATHS:
                if path.startswith(blocked):
                    print(f"🚫 Blocked sensitive path access: {path} from {request.remote_addr}")
                    abort(403)
