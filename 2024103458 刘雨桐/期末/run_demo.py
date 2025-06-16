from expense_tracker.sample_data import random_entries, save_csv
from expense_tracker.storage import Storage
from expense_tracker.commands import stats, charts
from expense_tracker.importer import CSVImporter
from expense_tracker.report import MarkdownReporter
import pathlib, datetime

#手动添加
# === 1) 指定你自己的 CSV 路径 ===
#CSV_FILE = "my_expense.csv"      # ← 换成你的文件名

# === 2) 导入 CSV（覆盖旧数据）===
#store = Storage(pathlib.Path.home() / ".expense_tracker.json")
#store.save_json([])                  # 清空旧数据（可选，确保不混入历史）
#import_csv(store, CSV_FILE)          # 读取 CSV 并写入 JSON

#随机生成
# 1) 生成随机 200 条并导出 CSV
csv_path = save_csv(random_entries(200), "today_entries.csv")

# 2) 用 CSV 覆盖式写入 JSON（不保留历史）
store = Storage(pathlib.Path.home() / ".expense_tracker.json")
store.save_json(CSVImporter(csv_path).import_entries())

# 3) 统计 + 图表
stats(store)
charts(store)

# 4) 当月预算示例（1500 上限）
today = datetime.date.today()
from expense_tracker.budget import BudgetManager
bm = BudgetManager(1500); bm.feed(store.load_json())
print("Budget check:", bm.alert(today.year, today.month))

# 5) 生成本年 Markdown 年报
MarkdownReporter(store.load_json(), "reports").monthly_report(today.year)
