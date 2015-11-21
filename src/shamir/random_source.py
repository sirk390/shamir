from random import SystemRandom

class SecureRandomSource(object):
    def __init__(self):
        self.rand = SystemRandom()
    def randrange(self, start, end):
        return self.rand.randrange(start, end)

class UnitTestRandomSource(object):
    def __init__(self, results):
        self.iter = iter(results)
    def randrange(self, start, end):
        return next(self.iter)

if __name__ == "__main__":
    r = UnitTestRandomSource(range(100))
    print r.randint(0, 2)
    print r.randint(0, 2)
    print r.randint(0, 2)
    print r.randint(0, 2)
    