"""Algorithm to decompose numbers into a sum of pyramidal numbers 

A pyramidal number is defined as:
    pyramidal = (m^3 - m)/6, for m = 0, 1, 2, 3, ... 
    Eg. 0, 1, 4, 10, 20, ....
    
"""

import numpy as np
import logging as log

log.basicConfig(level=log.INFO, format="%(asctime)s: %(message)s")

def main():
    max_n = 1000000
    pyramidals = Pyramidals(max_n)
    found = [0] * (max_n+1)
    max_pyramidals = 5
    bad_numbers = []

    for n in range(1, max_n+1):
        decomposed = decompose_into_pyramidals(n, pyramidals, max_pyramidals, found)
        found[n] = decomposed

        msg = f"{n} = {' + '.join((str(a) for a in decomposed))}"
        log.info(msg)
        if len(decomposed) > max_pyramidals:
            bad_numbers.append(msg)

    log.info("==== FINISHED ====")
    log.warning(f"The following numbers could't be decomposed into a sum of {max_pyramidals} pyramidals:\n\t- " + '\n\t- '.join(bad_numbers))


class Pyramidals:
    def __init__(self, n: int):
        self.array, self.set = pyramidals_until(n)
        
    def __contains__(self, n):
        return n in self.set

    def closest(self, n, offset=1):
        return self.array[np.searchsorted(self.array, n) - offset]

    def until(self, n):
        return self.array[1:np.searchsorted(self.array, n)]

def calc_pyramidal(m: int):
    return (m**3 - m) / 6

def pyramidals_until(n: int):
    pyramidals = []    
    for m in range(1, n+1):
        p = int(calc_pyramidal(m))
        if p <= n:
            pyramidals.append(p)
        else:
            break
    return np.array(pyramidals), set(pyramidals)

def decompose_into_pyramidals_light(n: int, pyramidals: Pyramidals):
    if n in pyramidals:
        return [n]

    p = pyramidals.closest(n)
    result = [p]
    rest = decompose_into_pyramidals_light(n - p, pyramidals)

    return result + rest

def decompose_into_pyramidals_brute(n: int, pyramidals: Pyramidals, n_max: int):
    if n in pyramidals:
        return [n]

    if n_max == 1:
        return [n, 0]

    best = [n] + [0] * (n_max)
    
    for pyramidal in pyramidals.until(n)[::-1]:
        r = n - pyramidal        
        p = decompose_into_pyramidals_brute(r, pyramidals, n_max-1)

        if len(p) < len(best):
            best = [pyramidal] + p

    return best


def decompose_into_pyramidals(n: int, pyramidals: Pyramidals, n_max: int, found: list[list[int]]):
    """Decompose a number into pyramidals, given a list of already found pyramidals"""
    if n in pyramidals:
        return [n]

    for pyramidal in pyramidals.until(n)[::-1]:     
        r = n-pyramidal        
        f = found[r]

        if len(f) < n_max:
            return f + [pyramidal]
        
        p1 = decompose_into_pyramidals_light(r, pyramidals)            
        if len(p1) < n_max:
            found[r] = p1
            return p1 + [pyramidal]    

    p = decompose_into_pyramidals_brute(n, pyramidals, n_max)
    return p 

if __name__ == "__main__":
    main()