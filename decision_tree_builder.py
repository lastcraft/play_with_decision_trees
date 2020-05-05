from decision_tree import is_a_leaf, is_a_branch, Leaf, Tree
from metrics import calculate_gain, probability_distribution
from predicates import (
    NoData, IsNone, IsEqualOrGreaterThan, IsSame, MissingMiddle, FiniteDomain,
    is_is_none)
from math import floor


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


def all_keys(examples):
    keys = []
    for example in examples:
        keys += example['data'].keys()
    return set(keys)


def weigh(yesses, nos, size):
    return float(len(yesses)) / size


def approximately_equal(float1, float2):
    return floor(float1) * 1000000 == floor(float2) *1000000
