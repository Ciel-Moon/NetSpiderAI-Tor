import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from typing import List, Optional
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)

class ResumableDownloader:
    def __init__(self, download_dir: str = settings.DOWNLOAD_DIR, max_workers: int = 5):
        self.download_dir = download_dir
        self.max_workers = max_workers
        os.makedirs(download_dir, exist_ok=True)

    def download(self, url: str, filename: Optional[str] = None, resume: bool = True) -> Optional[str]:
        """Download a file with resume support."""
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or 'index.html'

        filepath = os.path.join(self.download_dir, filename)
        checkpoint_file = f"{filepath}.ckpt"

        # Get total size
        try:
            head = requests.head(url, timeout=settings.REQUEST_TIMEOUT)
            total_size = int(head.headers.get('content-length', 0))
        except Exception as e:
            logger.error(f"Failed to get file size for {url}: {e}")
            return None

        # Read checkpoint
        downloaded = 0
        if resume and os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                downloaded = checkpoint.get('downloaded', 0)

        if downloaded >= total_size:
            logger.info(f"File already fully downloaded: {filepath}")
            return filepath

        # Download chunks in parallel
        chunk_size = 1024 * 1024  # 1 MB
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for start in range(downloaded, total_size, chunk_size):
                end = min(start + chunk_size - 1, total_size - 1)
                future = executor.submit(self._download_chunk, url, filepath, start, end)
                futures.append(future)

            for future in as_completed(futures):
                future.result()  # propagate exceptions

        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
        return filepath

    def _download_chunk(self, url: str, filepath: str, start: int, end: int):
        """Download a single byte range."""
        headers = {'Range': f'bytes={start}-{end}'}
        try:
            resp = requests.get(url, headers=headers, stream=True, timeout=settings.REQUEST_TIMEOUT)
            resp.raise_for_status()
            mode = 'r+b' if os.path.exists(filepath) else 'wb'
            with open(filepath, mode) as f:
                f.seek(start)
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            # Update checkpoint
            self._update_checkpoint(filepath, end + 1)
        except Exception as e:
            logger.error(f"Chunk download failed {url} bytes {start}-{end}: {e}")
            raise

    def _update_checkpoint(self, filepath: str, downloaded: int):
        checkpoint_file = f"{filepath}.ckpt"
        with open(checkpoint_file, 'w') as f:
            json.dump({'downloaded': downloaded}, f)

    def download_many(self, urls: List[str], file_type: str) -> List[str]:
        """Download multiple files (images, videos)."""
        results = []
        for url in urls:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or f"{file_type}_{len(results)}"
            filepath = self.download(url, filename)
            if filepath:
                results.append(filepath)
        return results
