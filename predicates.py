
class NoData(Exception):
    pass


class OutOfDomain(Exception):
    pass


class FiniteDomain(object):
    def __init__(self, values):
        self.values = values

    def is_in(self, value):
        return value in self.values


class MissingMiddle(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def is_in(self, value):
        return value <= self.lower or value >= self.upper


class IsSame(object):
    def __init__(self, key, value, domain=None):
        self.key = key
        self.value = value
        self.domain = domain

    def __call__(self, data):
        if self.key not in data:
            raise NoData()
        if not self.domain.is_in(data[self.key]):
            raise OutOfDomain()
        return data[self.key] == self.value

    def __str__(self):
        return "%s is same as %s" % (self.key, self.value)


class IsEqualOrGreaterThan(object):
    def __init__(self, key, value, domain=None):
        self.key = key
        self.value = value
        self.domain = domain

    def __call__(self, data):
        if self.key not in data:
            raise NoData()
        if not self.domain.is_in(data[self.key]):
            raise OutOfDomain()
        return data[self.key] >= self.value

    def __str__(self):
        return "%s is greater than %s" % (self.key, self.value)


class IsNone(object):
    def __init__(self, key, domain=None):
        self.key = key
        self.domain = domain

    def __call__(self, data):
        if self.key not in data:
            return True
        if not self.domain.is_in(data[self.key]):
            raise OutOfDomain()
        return data[self.key] is None

    def __str__(self):
        return "%s is missing" % self.key


def is_is_none(predicate):
    return predicate.__class__.__name__ == 'IsNone'
