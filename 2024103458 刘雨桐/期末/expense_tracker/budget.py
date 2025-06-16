
import datetime
from typing import List
from collections import defaultdict
from .models import Entry

class BudgetManager:
    """Simple monthly budget tracker."""

    def __init__(self, monthly_limit: float):
        self.limit = monthly_limit
        self.spent: dict[str, float] = defaultdict(float)

    def feed(self, entries: List[Entry]):
        self.spent.clear()
        for e in entries:
            ym = f"{e.date.year}-{e.date.month:02}"
            self.spent[ym] += e.amount

    def remaining(self, year: int, month: int) -> float:
        ym = f"{year}-{month:02}"
        return self.limit - self.spent.get(ym, 0.0)

    def alert(self, year: int, month: int) -> str:
        rem = self.remaining(year, month)
        if rem < 0:
            return f"Over budget by {abs(rem):.2f}"
        if rem < self.limit * 0.1:
            return f"Warning: only {rem:.2f} left"
        return f"Balance OK: {rem:.2f} remaining"
