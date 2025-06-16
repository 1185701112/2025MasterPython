import datetime, random, itertools, pathlib, json
import csv, pathlib
from .models import Entry

def random_entries(n=100):
    cats=['food','transport','shopping','rent','salary','entertainment']
    today=datetime.date.today()
    out=[]
    for i in range(n):
        day = today - datetime.timedelta(days=random.randint(0,365))
        amt = round(random.uniform(5,200),2)
        cat = random.choice(cats)
        note = f'auto_{i}'
        out.append(Entry(day, amt, cat, note))
    return out

def gen_set_0(count=10):
    return random_entries(count)

def gen_set_1(count=10):
    return random_entries(count)

def gen_set_2(count=10):
    return random_entries(count)

def gen_set_3(count=10):
    return random_entries(count)

def gen_set_4(count=10):
    return random_entries(count)

def gen_set_5(count=10):
    return random_entries(count)

def gen_set_6(count=10):
    return random_entries(count)

def gen_set_7(count=10):
    return random_entries(count)

def gen_set_8(count=10):
    return random_entries(count)

def gen_set_9(count=10):
    return random_entries(count)

def gen_set_10(count=10):
    return random_entries(count)

def gen_set_11(count=10):
    return random_entries(count)

def gen_set_12(count=10):
    return random_entries(count)

def gen_set_13(count=10):
    return random_entries(count)

def gen_set_14(count=10):
    return random_entries(count)

def gen_set_15(count=10):
    return random_entries(count)

def gen_set_16(count=10):
    return random_entries(count)

def gen_set_17(count=10):
    return random_entries(count)

def gen_set_18(count=10):
    return random_entries(count)

def gen_set_19(count=10):
    return random_entries(count)

def save_entries(entries, path='random_entries.json'):
    import json
    with open(path,'w',encoding='utf-8') as f:
        json.dump([e.to_dict() for e in entries],f,indent=2,ensure_ascii=False)

def variation_0(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_1(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_2(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_3(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_4(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_5(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_6(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_7(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_8(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_9(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_10(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_11(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_12(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_13(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_14(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_15(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_16(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_17(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_18(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_19(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_20(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_21(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_22(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_23(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_24(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_25(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_26(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_27(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_28(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def variation_29(n=5):
    return [e for e in random_entries(n) if e.amount>50]

def high_spend_var_0(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_1(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_2(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_3(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_4(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_5(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_6(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_7(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_8(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_9(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_10(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_11(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_12(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_13(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_14(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_15(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_16(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_17(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_18(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_19(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_20(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_21(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_22(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_23(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def high_spend_var_24(days=30):
    entries=random_entries(200)
    cutoff=datetime.date.today()-datetime.timedelta(days=days)
    return [e for e in entries if e.amount>100 and e.date>cutoff]

def save_csv(entries, path="random_entries.csv"):
    """
    把随机生成的 Entry 列表写入 CSV，列头与 CSVImporter 兼容。
    """
    path = pathlib.Path(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "amount", "category", "note"])
        for e in entries:
            w.writerow([e.date.isoformat(), e.amount, e.category, e.note])
    return path