

def iterslices(iterable, n, pad_last=False, pad_value=None):
    """ Iterates over non-overlapping list of 'n' consecutive elements (python equivalent of each_slices).
        The last element might be smaller.
    """
    current = []
    for a in iterable:
        current.append(a)
        if len(current) == n:
            yield current
            current = []
    if current:
        if pad_last:
            current += [pad_value] * (n-len(current))
        yield current

def joinbase(iterable, base=32):
    it = iter(iterable)
    result = next(it)
    for v in it:
        result = result * base + v
    return result

def splitbase(value, base=257):
    result = []
    mod = value
    while value != 0:
        div, mod = divmod(value, base)
        result.append(mod)
        value = div
    return list(reversed(result))


if __name__ == "__main__":
    print list(iterslices(range(10), 3, True))
    print joinbase([1, 0, 1], 2)
    #print splitbase(joinbase([255, 255, 255, 255, 255, 255, 255, 255], 257), 256)
    
    #print list(iterslices(range(18), 9))
