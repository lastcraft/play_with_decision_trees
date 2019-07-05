from decision_tree_builder import build, prune
from tests.logical_deduction_tests import test_logical_deductions
from tests.many_choices_tests import test_option_with_many_choices
from tests.metrics_tests import test_statistics, test_gain
from tests.label_predicate_tests import test_text_label_predicates
from math import floor

from tests.missing_data_tests import test_deciding_with_missing_data, test_coping_with_unseen_options
from tests.numeric_tests import test_choosing_from_numerical_data, test_numerical_evaluations
from tests.pruning_tests import test_pruning


def one_dp(number):
    return floor(100 * number)/100.0


def approximately(a_dict):
    return {key: one_dp(value) for key, value in a_dict.iteritems()}


def all_tests():
    test_statistics()
    test_gain()
    test_text_label_predicates()
    test_logical_deductions()
    test_option_with_many_choices()
    test_pruning()
    test_deciding_with_missing_data()
    test_coping_with_unseen_options()
    test_choosing_from_numerical_data()
    test_numerical_evaluations()


def test_can_prune_tree_with_missing_example_data():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'cheerful'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree, threshold=0.1)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    # assert(tree.decide({}) == {'cheerful': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})


def test_prune_can_remove_missing_data_outliers():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'}] * 99
    examples += [{'data': {}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree, threshold=0.1)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({}) == {'happy': 1.0})


def test_prune_can_remove_outliers_leaving_missing_example_data():
    examples = [{'data': {}, 'conclusion': 'happy'}] * 99
    examples += [{'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree, threshold=0.1)
    assert(tree.decide({}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'happy': 1.0})


def test_unseen_option_treated_as_missing_data():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'cloudy'}) == {'happy': 0.5, 'sad': 0.5})


all_tests()
