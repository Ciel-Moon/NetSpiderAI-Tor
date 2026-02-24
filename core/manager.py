import stem.process
from stem.control import Controller
from stem import Signal
import requests
import socks
import socket
import time
from utils.logger import get_logger

logger = get_logger(__name__)

class TorManager:
    def __init__(self, socks_port=9050, control_port=9051, password=None):
        self.socks_port = socks_port
        self.control_port = control_port
        self.password = password
        self.tor_process = None
        self.session = None

    def start_tor(self):
        """Launch a Tor process."""
        logger.info("Starting Tor...")
        self.tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.control_port),
                'CookieAuthentication': '1' if not self.password else '0',
                'HashedControlPassword': self._hash_password(self.password) if self.password else None
            },
            init_msg_handler=self._print_bootstrap_lines
        )
        logger.info("Tor started successfully.")

    def _print_bootstrap_lines(self, line):
        if "Bootstrapped" in line:
            logger.debug(line.strip())

    def _hash_password(self, password):
        from stem.util import conf
        return conf.get_config().get('HashedControlPassword', None)  # Simplified; real hashing omitted

    def renew_identity(self):
        """Request a new Tor circuit (new IP)."""
        with Controller.from_port(port=self.control_port) as controller:
            if self.password:
                controller.authenticate(password=self.password)
            else:
                controller.authenticate()
            controller.signal(Signal.NEWNYM)
            logger.info("Tor identity renewed.")
            time.sleep(5)  # Allow circuit to establish

    def get_tor_session(self):
        """Return a requests Session configured to use Tor."""
        if not self.session:
            self.session = requests.Session()
            self.session.proxies = {
                'http': f'socks5h://127.0.0.1:{self.socks_port}',
                'https': f'socks5h://127.0.0.1:{self.socks_port}'
            }
            # Also set socket default for other libraries if needed
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.socks_port)
            socket.socket = socks.socksocket
        return self.session

    def stop_tor(self):
        """Terminate the Tor process."""
        if self.tor_process:
            self.tor_process.kill()
            self.tor_process = None
            logger.info("Tor stopped.")
