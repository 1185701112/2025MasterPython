
import pathlib
import datetime
from typing import List, Dict
from collections import defaultdict
from .models import Entry
from .analysis import category_summary, monthly_summary

class MarkdownReporter:
    """Generate markdown expense reports."""

    def __init__(self, entries: List[Entry], out_dir: str | pathlib.Path = "reports"):
        self.entries = entries
        self.out_dir = pathlib.Path(out_dir)
        self.out_dir.mkdir(exist_ok=True)

    # ---------------- util -----------------
    def _write(self, name: str, content: str):
        path = self.out_dir / name
        with path.open("w", encoding="utf-8") as f:
            f.write(content)
        print(f"Report saved -> {path}")

    # ---------------- public ---------------

    def monthly_report(self, year: int):
        """Generate a report for every month of a given year."""
        months: Dict[int, List[Entry]] = defaultdict(list)
        for e in self.entries:
            if e.date.year == year:
                months[e.date.month].append(e)

        parts: list[str] = [f"# Expense Report {year}\n"]
        total_year = 0.0

        for m in range(1, 13):
            ms = months.get(m, [])
            if not ms:
                continue
            parts.append(f"## {year}-{m:02}\n")
            cat_sum = category_summary(ms)
            mon_sum = sum(cat_sum.values())
            total_year += mon_sum
            parts.append("| Category | Amount |\n|---|---|\n")
            for cat, amt in cat_sum.items():
                parts.append(f"| {cat} | {amt:.2f} |\n")
            parts.append(f"**Subtotal:** {mon_sum:.2f}\n\n")

        parts.append(f"\n## Year Total: {total_year:.2f}\n")
        self._write(f"report_{year}.md", "".join(parts))

    def category_report(self):
        """One‑off report ranking categories across all entries."""
        cats = category_summary(self.entries)
        lines = ["# Category Ranking\n", "| Category | Amount |\n|---|---|\n"]
        for cat, amt in cats.items():
            lines.append(f"| {cat} | {amt:.2f} |\n")
        self._write("categories.md", "".join(lines))
