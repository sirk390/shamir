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

