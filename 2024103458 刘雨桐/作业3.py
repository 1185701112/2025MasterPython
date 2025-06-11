#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stats_sampler.py  ——  作业三：在作业二的 DataSampler 基础上，
                     通过参数化修饰器自动统计数值型叶节点的
                     SUM / AVG / VAR / RMSE
"""

from __future__ import annotations
import argparse
import functools
import math
import random
import string
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

# ------------------------------------------------------------
#   Part 1.  DataSampler（取自作业二，已含修正）
# ------------------------------------------------------------
def _rand_int(spec: Dict[str, Any]) -> int:
    lo, hi = spec.get("range", (0, 100))
    return random.randint(lo, hi)

def _rand_float(spec: Dict[str, Any]) -> float:
    lo, hi = spec.get("range", (0.0, 1.0))
    return random.uniform(lo, hi)

def _rand_bool(_: Dict[str, Any]) -> bool:
    return random.choice([True, False])

def _rand_str(spec: Dict[str, Any]) -> str:
    length = spec.get("length", 8)
    alphabet = spec.get("alphabet", string.ascii_letters + string.digits)
    return "".join(random.choice(alphabet) for _ in range(length))

def _rand_date(spec: Dict[str, Any]) -> str:
    start = datetime.fromisoformat(spec.get("start", "2000-01-01"))
    end   = datetime.fromisoformat(spec.get("end",   "2030-01-01"))
    days  = (end - start).days
    return (start + timedelta(days=random.randrange(days + 1))).date().isoformat()

_TYPE_HANDLERS = {
    "int":   _rand_int,
    "float": _rand_float,
    "bool":  _rand_bool,
    "str":   _rand_str,
    "date":  _rand_date,
}

def _generate_from_schema(spec: Any) -> Any:
    """递归解析 schema"""
    if isinstance(spec, dict):
        t = spec.get("type")
        # ---- 复合类型优先 ----
        if t == "list":
            length = spec.get("length", random.randint(0, 10))
            return [_generate_from_schema(spec["items"]) for _ in range(length)]
        if t == "tuple":
            return tuple(_generate_from_schema(s) for s in spec["items"])
        if t == "dict":
            return {k: _generate_from_schema(v) for k, v in spec["items"].items()}
        # ---- 原子类型 ----
        if "type" in spec:
            if t not in _TYPE_HANDLERS:
                raise ValueError(f"Unsupported type: {t}")
            return _TYPE_HANDLERS[t](spec)
    # ---- schema 直接写成内置结构 ----
    if isinstance(spec, list):
        return [_generate_from_schema(s) for s in spec]
    if isinstance(spec, tuple):
        return tuple(_generate_from_schema(s) for s in spec)
    if isinstance(spec, dict):
        return {k: _generate_from_schema(v) for k, v in spec.items()}
    # ---- 常量 ----
    return spec

def data_sampler(*, sample_num: int, schema: Any) -> List[Any]:
    """对外主接口"""
    return [_generate_from_schema(schema) for _ in range(sample_num)]

# ------------------------------------------------------------
#   Part 2.  统计修饰器
# ------------------------------------------------------------
_ALLOWED = {"SUM", "AVG", "VAR", "RMSE"}

def _collect_numeric_leaves(obj: Any, acc: List[float]) -> None:
    """DFS 收集所有 int / float（排除 bool）"""
    if isinstance(obj, bool):           # bool 是 int 子类，要过滤
        return
    if isinstance(obj, (int, float)):
        acc.append(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_numeric_leaves(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect_numeric_leaves(v, acc)

def _compute_stats(values: List[float], kinds: Tuple[str, ...]) -> Dict[str, float]:
    n = len(values)
    total = sum(values)
    mean  = total / n if n else 0.0
    var   = sum((x - mean) ** 2 for x in values) / n if n else 0.0
    rmse  = math.sqrt(sum(x ** 2 for x in values) / n) if n else 0.0
    lookup = {"SUM": total, "AVG": mean, "VAR": var, "RMSE": rmse}
    return {k: lookup[k] for k in kinds}

def stats_decorator(*stats_kind: str):
    """
    用法:
        @stats_decorator("SUM", "AVG")   # 只算求和、均值
        def func(...): ...
    """
    kinds = tuple(k.upper() for k in stats_kind) or ("SUM", "AVG", "VAR", "RMSE")
    if invalid := set(kinds) - _ALLOWED:
        raise ValueError(f"Unsupported stat(s): {invalid}")

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            data = fn(*args, **kwargs)
            numeric: List[float] = []
            _collect_numeric_leaves(data, numeric)
            stats = _compute_stats(numeric, kinds)
            print(f"[stats] {stats}")
            return data, stats         # 原样本 & 统计结果一起返回
        return wrapper
    return decorator

# ------------------------------------------------------------
#   Part 3.  Demo & CLI
# ------------------------------------------------------------
DEMO_SCHEMA = {
    "user_id": {"type": "int", "range": (1000, 9999)},
    "profile": {
        "type": "dict",
        "items": {
            "name":  {"type": "str",  "length": 6},
            "vip":   {"type": "bool"},
            "score": {"type": "float", "range": (0, 100)},
            "tags":  {"type": "list", "length": 3,
                      "items": {"type": "str", "length": 4}},
            "birthday": {"type": "date",
                         "start": "1990-01-01", "end": "2005-12-31"}
        },
    },
    "recent_locations": {
        "type": "tuple",
        "items": [
            {"type": "float", "range": (-90, 90)},
            {"type": "float", "range": (-180, 180)}
        ],
    },
}

@stats_decorator()                   # 不写参数 = 4 项全算
def generate_demo(n: int):
    """返回 n 条随机用户数据"""
    return data_sampler(sample_num=n, schema=DEMO_SCHEMA)

def main():
    parser = argparse.ArgumentParser(description="DataSampler + 统计修饰器 Demo")
    parser.add_argument("-n", "--num", type=int, default=5, help="样本数")
    parser.add_argument("--stats", nargs="*", default=[], help="统计项子集 eg: SUM AVG")
    args = parser.parse_args()

    # 若 CLI 指定了 stats 子集 → 动态替换装饰器
    if args.stats:
        global generate_demo
        generate_demo = stats_decorator(*args.stats)(lambda m=args.num: data_sampler(sample_num=m, schema=DEMO_SCHEMA))

    samples, stats = generate_demo(args.num)
    print("\n=== 样本示例 ===")
    print(json.dumps(samples[:2], indent=2, ensure_ascii=False))   # 仅展示前两条
    print("\n=== 统计结果 ===")
    print(stats)

if __name__ == "__main__":
    main()
