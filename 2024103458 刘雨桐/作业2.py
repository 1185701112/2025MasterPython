#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DataSampler – 通用随机数据生成器（作业二）
================================================
"""

from __future__ import annotations
import argparse
import random
import string
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

# ------------------------------------------------------------
# 基础随机生成函数
# ------------------------------------------------------------
def rand_int(spec: Dict[str, Any]) -> int:
    lo, hi = spec.get("range", (0, 100))
    return random.randint(lo, hi)

def rand_float(spec: Dict[str, Any]) -> float:
    lo, hi = spec.get("range", (0.0, 1.0))
    return random.uniform(lo, hi)

def rand_bool(_: Dict[str, Any]) -> bool:
    return random.choice([True, False])

def rand_str(spec: Dict[str, Any]) -> str:
    length = spec.get("length", 8)
    alphabet = spec.get("alphabet", string.ascii_letters + string.digits)
    return "".join(random.choice(alphabet) for _ in range(length))

def rand_date(spec: Dict[str, Any]) -> str:
    """随机日期，返回 ISO 字符串"""
    start = datetime.fromisoformat(spec.get("start", "2000-01-01"))
    end   = datetime.fromisoformat(spec.get("end",   "2030-01-01"))
    days_range = (end - start).days
    return (start + timedelta(days=random.randrange(days_range + 1))).date().isoformat()

# 映射表：数据类型 -> 生成函数
TYPE_HANDLERS = {
    "int":   rand_int,
    "float": rand_float,
    "bool":  rand_bool,
    "str":   rand_str,
    "date":  rand_date,
}

# ------------------------------------------------------------
# 递归生成核心
# ------------------------------------------------------------
def _generate_from_schema(spec: Any) -> Any:
    """DFS 解析 schema 并返回随机数据"""

    # ---------- 先处理三种『复合类型』 ----------
    if isinstance(spec, dict):
        t = spec.get("type")
        if t == "list":
            length = spec.get("length", random.randint(0, 10))
            return [_generate_from_schema(spec["items"]) for _ in range(length)]
        if t == "tuple":
            return tuple(_generate_from_schema(s) for s in spec["items"])
        if t == "dict":
            return {k: _generate_from_schema(v) for k, v in spec["items"].items()}

    # ---------- 再处理『原子类型』 ----------
    if isinstance(spec, dict) and "type" in spec:
        dtype = spec["type"]
        if dtype not in TYPE_HANDLERS:
            raise ValueError(f"Unsupported type: {dtype}")
        return TYPE_HANDLERS[dtype](spec)

    # ---------- schema 本身写成内置结构 ----------
    if isinstance(spec, list):
        return [_generate_from_schema(s) for s in spec]
    if isinstance(spec, tuple):
        return tuple(_generate_from_schema(s) for s in spec)
    if isinstance(spec, dict):
        return {k: _generate_from_schema(v) for k, v in spec.items()}

    # ---------- 常量原样返回 ----------
    return spec

# ------------------------------------------------------------
# 对外接口
# ------------------------------------------------------------
def data_sampler(*, sample_num: int, schema: Any) -> List[Any]:
    """生成 sample_num 条符合 schema 的随机样本"""
    return [_generate_from_schema(schema) for _ in range(sample_num)]

# ------------------------------------------------------------
# 自带 Demo
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
            {"type": "float", "range": (-90, 90)},   # lat
            {"type": "float", "range": (-180, 180)}  # lon
        ],
    },
}

# ------------------------------------------------------------
# CLI 入口
# ------------------------------------------------------------
def _cli() -> None:
    parser = argparse.ArgumentParser(description="Generic nested random DataSampler")
    parser.add_argument("-n", "--num", type=int, default=5, help="样本数量")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式打印")
    args = parser.parse_args()

    samples = data_sampler(sample_num=args.num, schema=DEMO_SCHEMA)

    if args.json:
        print(json.dumps(samples, indent=2, ensure_ascii=False))
    else:
        for i, s in enumerate(samples, 1):
            print(f"[{i}] {s}")

if __name__ == "__main__":
    _cli()
