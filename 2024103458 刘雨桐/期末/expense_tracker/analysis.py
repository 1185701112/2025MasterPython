from collections import defaultdict
from typing import List, Dict
from .models import Entry

def category_summary(entries: List[Entry])->Dict[str,float]:
    d=defaultdict(float)
    for e in entries:
        d[e.category]+=e.amount
    return dict(sorted(d.items(), key=lambda kv:-kv[1]))

def monthly_summary(entries: List[Entry])->Dict[str,float]:
    d=defaultdict(float)
    for e in entries:
        ym=f"{e.date.year}-{e.date.month:02}"
        d[ym]+=e.amount
    return dict(sorted(d.items()))
