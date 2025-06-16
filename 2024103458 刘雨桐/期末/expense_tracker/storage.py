import json, pathlib, csv
from typing import List
from .models import Entry

class Storage:
    def __init__(self, path:pathlib.Path|str):
        self.path=pathlib.Path(path)
        self.path.parent.mkdir(exist_ok=True)

    def load_json(self)->List[Entry]:
        if not self.path.exists():
            return []
        with self.path.open(encoding='utf-8') as f:
            data=json.load(f)
        return [Entry.from_dict(d) for d in data]

    def save_json(self, entries:List[Entry]):
        with self.path.open("w",encoding='utf-8') as f:
            json.dump([e.to_dict() for e in entries],f,ensure_ascii=False,indent=2)

    def export_csv(self, entries:List[Entry], csv_path:str|pathlib.Path):
        csv_path=pathlib.Path(csv_path)
        with csv_path.open("w",newline="",encoding='utf-8') as f:
            w=csv.writer(f)
            w.writerow(["id","date","amount","category","note"])
            for e in entries:
                w.writerow([e.id,e.date.isoformat(),e.amount,e.category,e.note])
