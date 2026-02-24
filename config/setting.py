import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOWNLOAD_DIR = os.path.join(DATA_DIR, 'downloads')
LOG_DIR = os.path.join(DATA_DIR, 'logs')
DB_DIR = os.path.join(DATA_DIR, 'db')

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# Tor settings
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = None  # Set if using hashed password

# Crawler settings
DEFAULT_RENDERING_ENGINE = 'playwright'  # 'playwright', 'selenium', 'requests'
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
CRAWL_DELAY = 1  # seconds between requests to same domain

# Proxy pool
PROXY_TEST_URL = 'http://httpbin.org/ip'
PROXY_TEST_TIMEOUT = 5
PROXY_REFRESH_INTERVAL = 300  # seconds

# Database
DATABASE_URL = f'sqlite:///{os.path.join(DB_DIR, "spider.db")}'

# RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'crawl_tasks'

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(LOG_DIR, 'spider.log')
