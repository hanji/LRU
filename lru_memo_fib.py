#!/usr/bin/env python
# -*- coding: utf-8 -*-

class LRU(object):
    """
    Least-recently-used cache with amortized O(1) element access.
    (c) copyright 2011 Ji Han.
    freely distributable under the BSD license.
    """
    def __init__(self, size=128):
        self._bufsiz = size
        self._down, self._up = {}, {}
        self._default = None

    def __contains__(self, key):
        return key in self._down or key in self._up

    def __setitem__(self, key, value):
        if len(self._down) >= self._bufsiz:
            self._up, self._down = self._down, self._up
            self._down.clear()
        self._down[key] = value

    def __getitem__(self, key):
        value = self._default
        try:
            value = self._down[key]
        except KeyError:
            value = self._up[key]
            del self._up[key]
            self[key] = value
        finally:
            return value

    def __delitem__(self, key):
        try:
            del self._down[key]
        except KeyError:
            del self._up[key]
        finally:
            pass

    def items(self):
        return self._down.items() + self._up.items()

    def clear(self):
        self._down.clear()
        self._up.clear()

def memoize(f):
    """
    memoization with LRU cache.
    (c) copyright 2011 Ji Han.
    freely distributable under the BSD license.
    """
    cache = LRU()
    def g(*args):
        if not args in cache:
            cache[args] = f(*args)
        return cache[args]
    return g

@memoize
def fib(n):
    """
    fib = lambda n: return 0 if n == 0 else 1 if n == 1 else fib(n - 1) + fib(n - 2)
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

if __name__ == '__main__':
    import sys, timeit
    sys.setrecursionlimit(1048576)
    try:
        n = int(sys.argv[1])
    except IndexError:
        n = 1000
    stmt = 'fib(%d)' % n
    print timeit.Timer(stmt, 'from __main__ import fib').timeit(number=1), 'secs'
    print stmt, '=>', eval(stmt)
