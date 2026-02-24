import time
import random
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright

from config import settings
from utils.user_agent import get_random_ua
from utils.fingerprint import randomize_fingerprint
from utils.logger import get_logger
from core.proxy_pool import ProxyPool
from core.robots_checker import RobotsChecker

logger = get_logger(__name__)

class DynamicCrawler:
    def __init__(self, engine: str = None, proxy_pool: ProxyPool = None, tor_manager=None):
        self.engine = engine or settings.DEFAULT_RENDERING_ENGINE
        self.proxy_pool = proxy_pool
        self.tor_manager = tor_manager
        self.robots_checker = RobotsChecker()
        self.session = requests.Session()

    def _get_proxy_dict(self):
        """Return a proxy dict for requests or Selenium."""
        if self.tor_manager:
            # Tor already configured via session
            return None
        if self.proxy_pool:
            proxy = self.proxy_pool.get_proxy()
            if proxy:
                return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        return None

    def crawl(self, url: str, force: bool = False, dynamic: bool = None) -> Optional[Dict[str, Any]]:
        """
        Main crawl method.
        Returns a dict with 'text', 'images', 'videos' or None on failure.
        If robots.txt blocks and force=False, returns a string like 'robots_blocked'.
        """
        if not force:
            allowed = self.robots_checker.check(url, user_agent='*')
            if not allowed:
                logger.info(f"robots.txt blocks {url}")
                return 'robots_blocked'

        use_dynamic = dynamic if dynamic is not None else (self.engine != 'requests')

        if use_dynamic:
            if self.engine == 'selenium':
                html = self._crawl_selenium(url)
            elif self.engine == 'playwright':
                html = self._crawl_playwright(url)
            else:
                html = self._crawl_requests(url)
        else:
            html = self._crawl_requests(url)

        if html is None:
            return None

        return self._parse_html(html, url)

    def _crawl_requests(self, url: str) -> Optional[str]:
        """Simple requests-based crawl."""
        try:
            headers = {'User-Agent': get_random_ua()}
            proxies = self._get_proxy_dict()
            if self.tor_manager:
                resp = self.tor_manager.get_tor_session().get(
                    url, headers=headers, timeout=settings.REQUEST_TIMEOUT
                )
            else:
                resp = self.session.get(
                    url, headers=headers, proxies=proxies, timeout=settings.REQUEST_TIMEOUT
                )
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

    def _crawl_selenium(self, url: str) -> Optional[str]:
        """Selenium with headless Chrome."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={get_random_ua()}')
        # Anti-detection
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # Proxy
        proxy_dict = self._get_proxy_dict()
        if proxy_dict:
            proxy = proxy_dict['http'].replace('http://', '')
            options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        try:
            driver.get(url)
            time.sleep(2)  # basic wait
            html = driver.page_source
            return html
        except Exception as e:
            logger.error(f"Selenium crawl failed for {url}: {e}")
            return None
        finally:
            driver.quit()

    def _crawl_playwright(self, url: str) -> Optional[str]:
        """Playwright with anti-detection."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=get_random_ua(),
                viewport=randomize_fingerprint()['viewport'],
                device_scale_factor=1,
                has_touch=False,
                is_mobile=False
            )
            page = context.new_page()
            try:
                page.goto(url, wait_until='networkidle')
                html = page.content()
                return html
            except Exception as e:
                logger.error(f"Playwright crawl failed for {url}: {e}")
                return None
            finally:
                browser.close()

    def _parse_html(self, html: str, base_url: str) -> Dict[str, Any]:
        """Extract text, image URLs, video URLs."""
        soup = BeautifulSoup(html, 'lxml')
        for script in soup(['script', 'style']):
            script.decompose()
        text = soup.get_text(separator='\n', strip=True)

        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                images.append(urljoin(base_url, src))

        videos = []
        for video in soup.find_all('video'):
            src = video.get('src')
            if src:
                videos.append(urljoin(base_url, src))
            for source in video.find_all('source'):
                src = source.get('src')
                if src:
                    videos.append(urljoin(base_url, src))
        for source in soup.find_all('source'):
            src = source.get('src')
            if src and source.parent.name != 'video':
                videos.append(urljoin(base_url, src))

        return {
            'text': text,
            'images': list(set(images)),
            'videos': list(set(videos))
        }
