from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import requests
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)

class RobotsChecker:
    def __init__(self):
        self.cache = {}

    def _get_parser(self, base_url: str) -> RobotFileParser:
        """Retrieve or create a RobotFileParser for the domain."""
        if base_url in self.cache:
            return self.cache[base_url]

        parser = RobotFileParser()
        robots_url = f"{base_url}/robots.txt"
        parser.set_url(robots_url)
        try:
            resp = requests.get(robots_url, timeout=settings.REQUEST_TIMEOUT)
            if resp.status_code in (200, 404):
                parser.parse(resp.text.splitlines())
            else:
                parser = None
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt from {robots_url}: {e}")
            parser = None

        self.cache[base_url] = parser
        return parser

    def check(self, url: str, user_agent: str = '*') -> bool:
        """Return True if allowed, False if disallowed or no parser."""
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        parser = self._get_parser(base)
        if parser is None:
            return True  # allow if we can't get robots.txt
        return parser.can_fetch(user_agent, url)
