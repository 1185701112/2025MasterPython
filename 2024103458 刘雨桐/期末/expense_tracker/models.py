import datetime
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Entry:
    date: datetime.date
    amount: float
    category: str
    note: str = ""
    id: int = field(default_factory=lambda: Entry._gen_id())

    _id_counter: int = 0

    @classmethod
    def _gen_id(cls)->int:
        cls._id_counter+=1
        return cls._id_counter

    def to_dict(self)->dict:
        return {
            "id":self.id,
            "date":self.date.isoformat(),
            "amount":self.amount,
            "category":self.category,
            "note":self.note
        }

    @classmethod
    def from_dict(cls,d:dict)->"Entry":
        return cls(
            date=datetime.date.fromisoformat(d["date"]),
            amount=d["amount"],
            category=d["category"],
            note=d.get("note",""),
            id=d["id"]
        )

def demo_entries()->List[Entry]:
    today=datetime.date.today()
    return [Entry(today,20,"food","lunch"),Entry(today,50,"transport","bus"),Entry(today,35,"shopping","books")]
