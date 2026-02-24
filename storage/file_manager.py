import os
import shutil
from config import settings

class FileManager:
    @staticmethod
    def ensure_dir(path: str):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def save_text(content: str, filename: str, subdir: str = 'text') -> str:
        path = os.path.join(settings.DOWNLOAD_DIR, subdir)
        FileManager.ensure_dir(path)
        filepath = os.path.join(path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    @staticmethod
    def move_file(src: str, dest_dir: str) -> str:
        FileManager.ensure_dir(dest_dir)
        dest = os.path.join(dest_dir, os.path.basename(src))
        shutil.move(src, dest)
        return dest
