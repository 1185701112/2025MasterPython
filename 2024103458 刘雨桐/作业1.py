import random
import time
import argparse
import sys
from typing import List, Tuple

def build_list_matrix(n: int) -> List[List[int]]:

    return [[0] * n for _ in range(n)]

def build_tuple_matrix(n: int) -> Tuple[Tuple[int, ...], ...]:

    row = tuple(0 for _ in range(n))
    return tuple(row for _ in range(n)) 

def mutate_list_matrix(mat: List[List[int]], rounds: int) -> None:
    n = len(mat)
    for _ in range(rounds):
        i = random.randrange(n)
        j = random.randrange(n)
        mat[i][j] += 1

def mutate_tuple_matrix(mat: Tuple[Tuple[int, ...], ...], rounds: int) -> Tuple[Tuple[int, ...], ...]:
    n = len(mat)
    mat_list = list(mat)
    for _ in range(rounds):
        i = random.randrange(n)
        j = random.randrange(n)
        row_as_list = list(mat_list[i])
        row_as_list[j] += 1
        mat_list[i] = tuple(row_as_list)
    return tuple(mat_list)

def benchmark(n: int, rounds: int) -> None:
    print(f"\n=== 基准测试：{n}×{n} 矩阵，随机修改 {rounds} 次 ===")


    t0 = time.perf_counter()
    list_mat = build_list_matrix(n)
    t1 = time.perf_counter()
    print(f"构造 list 矩阵耗时: {t1 - t0:.3f} s")


    t2 = time.perf_counter()
    tuple_mat = build_tuple_matrix(n)
    t3 = time.perf_counter()
    print(f"构造 tuple 矩阵耗时: {t3 - t2:.3f} s")


    t4 = time.perf_counter()
    mutate_list_matrix(list_mat, rounds)
    t5 = time.perf_counter()
    print(f"list 修改耗时: {t5 - t4:.3f} s")


    t6 = time.perf_counter()
    tuple_mat = mutate_tuple_matrix(tuple_mat, rounds)
    t7 = time.perf_counter()
    print(f"tuple 修改耗时: {t7 - t6:.3f} s")

    print("\n=== 结果对比 ===")
    print(f"修改阶段加速比（tuple / list）: {(t7 - t6) / (t5 - t4):.1f} ×")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List vs Tuple mutability benchmark")
    parser.add_argument("--safe", action="store_true", help="使用较小矩阵(2000×2000)防止 OOM")
    args = parser.parse_args()

    N = 10000
    SAFE_N = 2000
    ROUNDS = 10000

    try:
        benchmark(N if not args.safe else SAFE_N, ROUNDS)
    except MemoryError:
        print("内存不足！请加 --safe 或进一步减小 N", file=sys.stderr)
