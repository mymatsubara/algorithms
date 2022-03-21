"""The problem is specified in: https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=29&page=show_problem&problem=36"""
import sys

def problem_3n_1(lines):
    """The input should be a list of strings countaining a pair of i,j numbers on each line. E.g:
    1 10
    100 200
    201 210
    """
    # Parse input
    i_js = [l.strip().split(" ") for l in lines]
    i_js = [[int(e[0]), int(e[1])] for e in i_js if len(e) == 2]

    cache = {}

    for i_j in i_js:
        [i, j] = sorted(i_j)
        line_max = 0
        for n in range(i, j+1):
            if n == 0:
                continue     

            max_cycle, offsets = find_max_cycle(n, cache)
            cache[n] = max_cycle
            for other_n, offset in offsets:
                cache[other_n] = max_cycle - offset
            line_max = max(max_cycle, line_max)

        i_j.append(line_max)

    lines = (" ".join(str(e) for e in pair) for pair in i_js)
    return "\n".join(lines)
        

def find_max_cycle(n, cache):
    count = 1
    offsets = []
    while n != 1:
        if n % 2 != 0:
            n = 3*n + 1
        else:
            n //= 2

        max_cycle_cached = cache.get(n)
        if max_cycle_cached is not None:
            return count + max_cycle_cached, offsets
        else:
            offsets.append((n, count))

        count += 1
    return count, offsets

input_ = sys.stdin.readlines()
print(problem_3n_1(input_))
