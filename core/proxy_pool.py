import requests
import threading
import time
from queue import Queue
from datetime import datetime
from typing import Optional, List, Dict
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)

class ProxyPool:
    def __init__(self):
        self.proxies: List[Dict] = []  # active proxies
        self.pending = Queue()         # proxies to validate
        self.lock = threading.Lock()
        self.running = True
        self._start_fetchers()
        self._start_validators()

    def _fetch_from_free_proxy_list(self) -> List[str]:
        """Fetch from https://free-proxy-list.net/"""
        try:
            resp = requests.get('https://free-proxy-list.net/', timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            table = soup.find('table')
            proxies = []
            for row in table.tbody.find_all('tr'):
                cells = row.find_all('td')
                if cells and cells[6].text == 'yes':  # HTTPS support
                    ip = cells[0].text
                    port = cells[1].text
                    proxies.append(f"{ip}:{port}")
            return proxies
        except Exception as e:
            logger.error(f"Error fetching from free-proxy-list: {e}")
            return []

    def _fetch_from_geonode(self) -> List[str]:
        # Placeholder for another source
        return []

    def _fetch_from_proxyscrape(self) -> List[str]:
        # Placeholder
        return []

    def _start_fetchers(self):
        def fetcher():
            sources = [
                self._fetch_from_free_proxy_list,
                self._fetch_from_geonode,
                self._fetch_from_proxyscrape
            ]
            while self.running:
                for source in sources:
                    try:
                        proxies = source()
                        for proxy in proxies:
                            self.pending.put(proxy)
                    except Exception as e:
                        logger.error(f"Proxy fetcher error: {e}")
                time.sleep(settings.PROXY_REFRESH_INTERVAL)
        threading.Thread(target=fetcher, daemon=True).start()

    def _start_validators(self):
        def validator():
            while self.running:
                if not self.pending.empty():
                    proxy = self.pending.get()
                    if self._validate_proxy(proxy):
                        with self.lock:
                            self.proxies.append({
                                'proxy': proxy,
                                'last_verified': datetime.now(),
                                'success_count': 0,
                                'fail_count': 0
                            })
                time.sleep(1)
        for _ in range(5):
            threading.Thread(target=validator, daemon=True).start()

    def _validate_proxy(self, proxy: str) -> bool:
        try:
            resp = requests.get(
                settings.PROXY_TEST_URL,
                proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                timeout=settings.PROXY_TEST_TIMEOUT
            )
            return resp.status_code == 200
        except:
            return False

    def get_proxy(self) -> Optional[str]:
        with self.lock:
            if not self.proxies:
                return None
            # Simple round-robin
            proxy = self.proxies.pop(0)
            self.proxies.append(proxy)
            return proxy['proxy']
