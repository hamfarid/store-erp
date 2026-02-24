# CONFIG-scrapy-defaults.py
# Governance: ML/AI Application Framework (Feb 2026)
# Tooling: Scrapy 2.11.1

# 1. Compliance
ROBOTSTXT_OBEY = True
USER_AGENT = 'GlobalSystemBot/1.0 (contact@example.com)'

# 2. Rate Limiting
DOWNLOAD_DELAY = 10  # 1 request per 10 seconds
CONCURRENT_REQUESTS_PER_DOMAIN = 1
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# 3. Retry Middleware
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 4. Caching (Optional)
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 5. Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 6. Item Pipelines
ITEM_PIPELINES = {
    'pipelines.validation.ValidationPipeline': 300,
    'pipelines.storage.StoragePipeline': 800,
}

# 7. Extensions
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}
