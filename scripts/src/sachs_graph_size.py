def primitive_order(k, g, memo=None):
    if memo is None:
        memo = {}
    if(k, g) in memo:
        return memo[(k, g)]

    if k == 2:
        return g
    if g == 2:
        return 2 * k - 2
    inner = primitive_order(k - 1, g, memo)
    result = primitive_order(inner, g - 1, memo)
    memo[(k, g)] = result
    return result


if __name__ == "__main__":
    k = int(input("Enter k: "))
    g = int(input("Enter g: "))

    result = primitive_order(k, g)
    print(f"N({k}, {g}) = {result}")
