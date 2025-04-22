from functools import lru_cache
import sys
sys.setrecursionlimit(1000000)

def count_vertices_faster(v, y):
    if y == 2:
        return 2
    if v == 2:
        return y

    delta = count_vertices(v - 1, y)
    lambd = count_vertices(delta, y - 1)
    return delta * lambd


def count_vertices(v, y, memo=None):
    if memo is None:
        memo = {}

    if (v, y) in memo:
        return memo[(v, y)]

    if y == 2:
        memo[(v, y)] = 2
        return 2

    if v == 2:
        memo[(v, y)] = y
        return y

    vertices_in_delta = count_vertices(v - 1, y, memo)
    vertices_in_lambda = count_vertices(vertices_in_delta, y - 1, memo)

    result = vertices_in_delta * vertices_in_lambda
    memo[(v, y)] = result
    return result


def count_vertices_dp(v_max, y_max):
    dp = [[0] * (y_max + 1) for _ in range(v_max + 1)]

    for y in range(2, y_max + 1):
        dp[2][y] = y
    for v in range(3, v_max + 1):
        dp[v][2] = 2

    for v in range(3, v_max + 1):
        for y in range(3, y_max + 1):
            dp[v][y] = dp[v - 1][y] * dp[v][y - 1]

    return dp[v_max][y_max]


if __name__ == "__main__":
    k = int(input("Enter k: "))
    g = int(input("Enter g: "))

    result = count_vertices(k, g)
    # result_dp = N(k, g)
    print(f"N({k}, {g}) = {result}, DP = {0}")
