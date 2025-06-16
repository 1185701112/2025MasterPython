import datetime
from typing import List

from .models import Entry
from .storage import Storage
from .analysis import category_summary, monthly_summary
from .visualize import (
    plot_category_pie,
    plot_monthly_bar,
    plot_daily_hist,
    plot_budget_progress,
)


# ---------- 基础 CRUD ----------
def add_entry(
    storage: Storage,
    date: str,
    amount: float,
    category: str,
    note: str = "",
) -> None:
    d = datetime.date.fromisoformat(date)
    entry = Entry(d, amount, category, note)
    entries = storage.load_json()
    entries.append(entry)
    storage.save_json(entries)
    print(f"Added entry id={entry.id}")


def list_entries(storage: Storage) -> None:
    entries = storage.load_json()
    if not entries:
        print("No records")
        return
    for e in entries:
        print(f"{e.id:3}|{e.date}|{e.amount:8.2f}|{e.category:10}|{e.note}")


def delete_entry(storage: Storage, entry_id: int) -> None:
    entries = storage.load_json()
    new_entries = [e for e in entries if e.id != entry_id]
    storage.save_json(new_entries)
    print("Deleted" if len(new_entries) != len(entries) else "Not found")


# ---------- 统计 ----------
def stats(storage: Storage) -> None:
    entries = storage.load_json()
    print("Category summary:")
    for cat, amt in category_summary(entries).items():
        print(f"{cat:12}: {amt:8.2f}")

    print("\nMonthly summary:")
    for ym, amt in monthly_summary(entries).items():
        print(f"{ym}: {amt:8.2f}")


# ---------- 图表 ----------
def charts(storage: Storage, out_dir: str = "charts") -> None:
    entries = storage.load_json()
    plot_category_pie(entries, out_dir)
    plot_monthly_bar(entries, out_dir)
    plot_daily_hist(entries, out_dir)

    # 预算进度折线：默认月预算 1000
    today = datetime.date.today()
    plot_budget_progress(
        entries,
        monthly_limit=1500,
        year=today.year,
        month=today.month,
        out_dir=out_dir,
    )
    print(f"Charts saved to {out_dir}")


# ---------- CSV 批量导入 ----------
def import_csv(storage: Storage, csv_file: str) -> None:
    from .importer import CSVImporter

    imp = CSVImporter(csv_file)
    new_entries = imp.import_entries()
    entries = storage.load_json()
    entries.extend(new_entries)
    storage.save_json(entries)
    print(f"Imported {len(new_entries)} entries")


# ---------- 预算提醒 ----------
def budget_check(storage: Storage, limit: float, year: int, month: int) -> None:
    from .budget import BudgetManager

    bm = BudgetManager(limit)
    bm.feed(storage.load_json())
    print(bm.alert(year, month))
