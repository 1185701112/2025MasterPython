
import csv, datetime, pathlib
from typing import List
from .models import Entry

class CSVImporter:
    """Import bank CSV: columns date,amount,category,note"""

    def __init__(self, path: str | pathlib.Path):
        self.path = pathlib.Path(path)

    def parse_row(self, row: dict) -> Entry | None:
        try:
            date = datetime.date.fromisoformat(row['date'])
            amount = float(row['amount'])
            category = row.get('category') or 'misc'
            note = row.get('note','')
            return Entry(date, amount, category, note)
        except Exception as e:
            print(f"Skip row due to error: {e}")
            return None

    def import_entries(self) -> List[Entry]:
        entries: List[Entry] = []
        with self.path.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                e = self.parse_row(row)
                if e:
                    entries.append(e)
        print(f"Imported {len(entries)} entries from {self.path}")
        return entries
