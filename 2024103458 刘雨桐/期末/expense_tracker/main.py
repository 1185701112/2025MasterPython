from expense_tracker import commands
from expense_tracker.storage import Storage
from expense_tracker.models import demo_entries
import argparse, pathlib

DATA_FILE = pathlib.Path.home() / ".expense_tracker.json"
storage = Storage(DATA_FILE)

def build_parser():
    p = argparse.ArgumentParser(prog="expense", description="Expense tracker CLI")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("init-demo")

    add_p = sub.add_parser("add")
    add_p.add_argument("date")
    add_p.add_argument("amount", type=float)
    add_p.add_argument("category")
    add_p.add_argument("--note", default="")

    sub.add_parser("list")
    del_p = sub.add_parser("delete"); del_p.add_argument("entry_id", type=int)
    sub.add_parser("stats")
    sub.add_parser("charts")

    imp = sub.add_parser("import")
    imp.add_argument("csv_file")

    bud = sub.add_parser("budget")
    bud.add_argument("limit", type=float)
    bud.add_argument("year", type=int)
    bud.add_argument("month", type=int)

    return p

def main():
    p = build_parser(); args = p.parse_args()
    if args.cmd == "init-demo":
        storage.save_json(demo_entries());print("Demo data saved")
    elif args.cmd == "add":
        commands.add_entry(storage,args.date,args.amount,args.category,args.note)
    elif args.cmd == "list":
        commands.list_entries(storage)
    elif args.cmd == "delete":
        commands.delete_entry(storage,args.entry_id)
    elif args.cmd == "stats":
        commands.stats(storage)
    elif args.cmd == "charts":
        commands.charts(storage)
    elif args.cmd == "import":
        commands.import_csv(storage,args.csv_file)
    elif args.cmd == "budget":
        commands.budget_check(storage,args.limit,args.year,args.month)
    else:
        p.print_help()

if __name__=='__main__':
    main()
