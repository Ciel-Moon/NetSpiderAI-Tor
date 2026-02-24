import json
import csv
from typing import List, Dict

class Exporter:
    @staticmethod
    def to_json(data: Dict, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def to_csv(data: List[Dict], filepath: str, fieldnames: List[str] = None):
        if not data:
            return
        if not fieldnames:
            fieldnames = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
