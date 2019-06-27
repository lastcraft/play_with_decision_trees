from predicate import (
    NoData, OutOfDomain, FiniteDomain, MissingMiddle,
    IsNone, IsSame, IsEqualOrGreaterThan, is_is_none)
from metrics import calculate_gain, probability_distribution
from math import log, floor
log2 = lambda x: log(x) / log(2)


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


def build(examples):
    predicate = best_predicate(examples)
    if predicate == None:
        return Leaf(probability_distribution(examples))
    yesses, nos = partition(predicate, examples)
    if len(yesses) == len(examples):
        return Leaf(probability_distribution(yesses))
    if len(nos) == len(examples):
        return Leaf(probability_distribution(nos))
    return Tree(predicate, build(yesses), build(nos), weigh(yesses, nos, len(examples)))


def prune(examples, tree, threshold=0.1):
    if is_a_leaf(tree):
        return tree
    yesses, nos = partition(tree.predicate, examples)
    if is_a_branch(tree.yes):
        tree.yes = prune(yesses, tree.yes)
    if is_a_branch(tree.no):
        tree.no = prune(nos, tree.no)
    if is_a_leaf(tree.yes) and is_a_leaf(tree.no):
        if calculate_gain(examples, yesses, nos) < threshold:
            majority = yesses if len(yesses) > len(nos) else nos
            return Leaf(probability_distribution(majority))
    return tree


def best_predicate(examples):
    choice, highest_gain = None, 0.0
    for key in all_keys(examples):
        for predicate in create_predicates(key, examples):
            gain = measure_predicate(predicate, examples)
            if approximately_equal(gain, highest_gain) and is_is_none(predicate):
                choice = predicate
            if gain > highest_gain:
                choice, highest_gain = predicate, gain
    return choice


def measure_predicate(predicate, examples):
    yesses, nos = partition(predicate, examples)
    return calculate_gain(examples, yesses, nos)


def all_keys(examples):
    keys = []
    for example in examples:
        keys += example['data'].keys()
    return set(keys)


def create_predicates(key, examples):
    values = set()
    for example in examples:
        if key in example['data']:
            values.add(example['data'][key])
        else:
            values.add(None)
    return [select_predicate(key, value, values) for value in values]


def select_predicate(key, value, values):
    if value is None:
        return IsNone(key, domain=FiniteDomain(values))
    elif value.__class__.__name__ in ['float', 'int']:
        lower = next_lowest(value, values)
        return IsEqualOrGreaterThan(key, value, domain=MissingMiddle(lower, value))
    else:
        return IsSame(key, value, domain=FiniteDomain(values))


def next_lowest(value, values):
    lower = None
    for candidate in sorted(list(values)):  # inefficient
        if candidate < value:
            lower = candidate
        if candidate == value:
            return lower
    return value


def partition(predicate, examples):
    yesses, nos = [], []
    for example in examples:
        try:
            if predicate(example['data']):
                yesses.append(example)
            else:
                nos.append(example)
        except NoData:
            nos.append(example)
    return [yesses, nos]


def weigh(yesses, nos, size):
    return float(len(yesses)) / size


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


def approximately_equal(float1, float2):
    return floor(float1) * 1000000 == floor(float2) *1000000
