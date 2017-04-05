def count_stair_ways(n, k):
    if n == 0:
        return 1
    elif n < 0:
        return 0
    else:
        total, i = 0, 1
        while i <= k:
            total += count_stair_ways(n-i, k)
            i += 1
    return total