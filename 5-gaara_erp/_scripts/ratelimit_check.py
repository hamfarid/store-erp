import os
import sys
import traceback
from typing import Dict, List, Optional

# Ensure repo root on sys.path to import backend.app reliably
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app import create_app  # noqa: E402

app = create_app()
outfile = os.path.join(os.path.dirname(__file__), 'ratelimit_out.txt')


def hit(c, path: str, method: str = 'GET', count: int = 6, json_body: Optional[dict] = None) -> Dict[str, List[Optional[str]]]:
    codes: List[int] = []
    retry_after: List[Optional[str]] = []
    remaining: List[Optional[str]] = []
    limits: List[Optional[str]] = []
    for _ in range(count):
        if method.upper() == 'POST':
            rv = c.post(path, json=json_body or {})
        else:
            rv = c.get(path)
        codes.append(rv.status_code)
        retry_after.append(rv.headers.get('Retry-After'))
        remaining.append(rv.headers.get('X-RateLimit-Remaining'))
        limits.append(rv.headers.get('X-RateLimit-Limit'))
    return {
        'codes': codes,
        'retry_after': retry_after,
        'remaining': remaining,
        'limit': limits,
    }


try:
    with app.test_client() as c:
        results = {}
        # Detect limiter presence (best-effort)
        limiter_present = bool(getattr(app, 'extensions', {}).get('limiter'))
        results['limiter_present'] = limiter_present

        # Attempt auth endpoints (may be 404 if blueprints not loaded)
        auth_login = hit(c, '/api/auth/login', method='POST', count=6, json_body={'email': 'x@example.com', 'password': 'wrong'})
        auth_refresh = hit(c, '/api/auth/refresh', method='POST', count=11, json_body={'refresh_token': 'invalid'})
        results['auth_login'] = auth_login
        results['auth_refresh'] = auth_refresh

        # If both are 404-only, mark as skipped for auth ratelimit verification
        auth_404 = all(code == 404 for code in auth_login['codes']) and all(code == 404 for code in auth_refresh['codes'])
        results['auth_skipped'] = bool(auth_404)

        # Probe a known healthy endpoint to confirm server responsiveness
        health = hit(c, '/api/health', method='GET', count=5)
        results['health'] = health

        # Also probe status endpoint if it exists
        status = hit(c, '/api/status', method='GET', count=3)
        results['status'] = status

    # Write a compact, parse-friendly report
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('LIMITER_PRESENT ' + repr(results['limiter_present']) + '\n')
        f.write('AUTH_LOGIN_CODES ' + repr(results['auth_login']['codes']) + '\n')
        f.write('AUTH_LOGIN_RETRY_AFTER ' + repr(results['auth_login']['retry_after']) + '\n')
        f.write('AUTH_LOGIN_REMAINING ' + repr(results['auth_login']['remaining']) + '\n')
        f.write('AUTH_REFRESH_CODES ' + repr(results['auth_refresh']['codes']) + '\n')
        f.write('AUTH_REFRESH_RETRY_AFTER ' + repr(results['auth_refresh']['retry_after']) + '\n')
        f.write('AUTH_REFRESH_REMAINING ' + repr(results['auth_refresh']['remaining']) + '\n')
        f.write('AUTH_SKIPPED ' + repr(results['auth_skipped']) + '\n')
        f.write('HEALTH_CODES ' + repr(results['health']['codes']) + '\n')
        f.write('STATUS_CODES ' + repr(results['status']['codes']) + '\n')
except Exception as e:
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('ERR ' + repr(e) + '\n')
        f.write(traceback.format_exc())
