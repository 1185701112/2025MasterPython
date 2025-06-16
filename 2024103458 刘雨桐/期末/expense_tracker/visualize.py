import pathlib, matplotlib.pyplot as plt
from typing import List
from .models import Entry
from .analysis import category_summary, monthly_summary

def plot_category_pie(entries: List[Entry], out_dir='charts'):
    out=pathlib.Path(out_dir);out.mkdir(exist_ok=True)
    data=category_summary(entries)
    plt.figure(figsize=(6,6))
    plt.pie(data.values(),labels=data.keys(),autopct='%1.1f%%')
    plt.title('Spending by Category')
    plt.savefig(out/'category_pie.png');plt.close()

def plot_monthly_bar(entries: List[Entry], out_dir='charts'):
    out=pathlib.Path(out_dir);out.mkdir(exist_ok=True)
    data=monthly_summary(entries)
    plt.figure(figsize=(8,4))
    plt.bar(data.keys(),data.values())
    plt.xticks(rotation=45);plt.tight_layout()
    plt.title('Monthly Spending')
    plt.savefig(out/'monthly_bar.png');plt.close()

def plot_daily_hist(entries: List[Entry], out_dir='charts'):
    out=pathlib.Path(out_dir);out.mkdir(exist_ok=True)
    data={}
    for e in entries:
        data.setdefault(e.date,0)
        data[e.date]+=e.amount
    if not data: return
    xs=list(data.keys());ys=list(data.values())
    plt.figure(figsize=(8,4))
    plt.bar(xs,ys);plt.xticks(rotation=60);plt.tight_layout()
    plt.title('Daily Spend')
    plt.savefig(out/'daily_hist.png');plt.close()

def plot_budget_progress(entries: List[Entry], monthly_limit: float,
                         year: int, month: int, out_dir="charts"):
    """
    绘制本月累计支出 vs 预算上限 折线图。
    """
    from collections import defaultdict
    import matplotlib.pyplot as plt

    # 1. 按日累计支出
    daily = defaultdict(float)
    for e in entries:
        if e.date.year == year and e.date.month == month:
            daily[e.date.day] += e.amount

    if not daily:
        print("No data for budget chart."); return

    days = sorted(daily)
    cum = []
    total = 0
    for d in days:
        total += daily[d]
        cum.append(total)

    # 2. 画图
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    plt.figure(figsize=(7,4))
    plt.plot(days, cum, marker="o", label="Accumulated")
    plt.hlines(monthly_limit, days[0], days[-1], colors="r",
               linestyles="dashed", label=f"Budget {monthly_limit}")
    plt.xlabel("Day"); plt.ylabel("Amount")
    plt.title(f"Budget Progress {year}-{month:02}")
    plt.legend()
    plt.tight_layout()
    fname = pathlib.Path(out_dir) / f"budget_{year}-{month:02}.png"
    plt.savefig(fname); plt.close()
    print(f"Budget chart saved to {fname}")