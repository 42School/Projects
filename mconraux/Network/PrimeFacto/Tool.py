class WorkClass(object):
    def __init__(self, itemId, data):
        self.itemId = itemId
        self.data = data
        self.result = None
        self.Handler = None

    def __str__(self):
        return "<Order #%s>" % str(self.itemId)

    def factorize(n):
        ret = []
        nn = n
        while nn % 2 == 0:
            nn //= 2
            ret += [2]
        maxFactor = int(nn ** 0.5)
        maxI = (maxFactor - 3) // 2
        maxP = int(maxFactor ** 0.5)
        sieve = [True for j in xrange(maxI + 1)]
        i = 0
        for p in xrange(3, maxP + 1, 2):
            if p > maxP:
                break
            i = (p - 3) // 2
            if sieve[i]:
                while nn % p == 0:
                    nn //= p
                    ret += [p]
                    maxFactor = int(nn ** 0.5)
                    maxI = (maxFactor - 3) // 2
                    maxP = int(maxFactor ** 0.5)
                if nn == 1:
                    break
                else:
                    i2 = (p * p - 3) // 2
                    for k in xrange(i2, maxI + 1, p):
                        sieve[k] = False
        index = i
        for i in xrange(index, maxI + 1):
            if i > maxI:
                break
            if sieve[i]:
                p = 2 * i + 3
                while nn % p == 0:
                    nn //= p
                    ret += [p]
                    maxFactor = int(nn ** 0.5)
                    maxI = (maxFactor - 3) // 2
                if nn == 1:
                    break
        if nn != 1:
            ret += [nn]
        return ret

    def use(self):
        self.factorize(int(self.data))
    @staticmethod
    def from_dict(classname, serialized):
        assert classname == "workitem.WorkClass"
        w = WorkClass(serialized["itemId"], serialized["data"])
        w.result = serialized["result"]
        w.Handler = serialized["Handler"]
        return w
