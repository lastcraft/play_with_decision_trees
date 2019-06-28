from predicate import NoData, OutOfDomain
from math import log


class Tree(object):
    def __init__(self, predicate, yes, no, weight):
        self.predicate = predicate
        self.yes = yes
        self.no = no
        self.weight = weight

    def decide(self, data):
        try:
            return (self.yes if self.predicate(data) else self.no).decide(data)
        except NoData:
            return apportion(self.yes.decide(data), self.no.decide(data), self.weight)
        except OutOfDomain:
            return apportion(self.yes.decide(data), self.no.decide(data), self.weight)

    def __str__(self, indent=''):
        output = ''
        output += "\n" + indent + '+--- ' + str(self.predicate)
        output += str(self.yes.__str__(indent=indent + '|   '))
        output += "\n" + indent + '\\--- not ' + str(self.predicate)
        output += str(self.no.__str__(indent=indent + '    '))
        return output


class Leaf(object):
    def __init__(self, conclusion):
        self.conclusion = conclusion

    def decide(self, _):
        return self.conclusion

    def __str__(self, indent=''):
        return "\n" + indent + '\\---' + str(self.conclusion)


def apportion(distribution_1, distribution_2, weight):
    return merge_as_sums(
        value_map(lambda probability: weight * probability, distribution_1),
        value_map(lambda probability: (1 - weight) * probability, distribution_2))


def merge_as_sums(distribution_1, distribution_2):
    return {key: distribution_1.get(key, 0.0) + distribution_2.get(key, 0.0)
            for key in set(distribution_1.keys() + distribution_2.keys())}


def value_map(fn, distribution):
    return {key: fn(distribution[key]) for key in distribution.keys()}


def is_a_branch(tree):
    return hasattr(tree, 'predicate')


def is_a_leaf(tree):
    return not is_a_branch(tree)


def log2(x):
    return log(x) / log(2)
