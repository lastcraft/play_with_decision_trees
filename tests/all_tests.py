from decision_tree_builder import build, prune
from tests.logical_deduction_tests import test_logical_deductions
from tests.many_choices_tests import test_option_with_many_choices
from tests.metrics_tests import test_statistics, test_gain
from tests.label_predicate_tests import test_text_label_predicates
from math import floor

from tests.missing_data_tests import test_deciding_with_missing_data, test_coping_with_unseen_options
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


def test_choosing_from_numerical_data():
    test_decide_based_on_two_examples_separated_numerically()
    test_can_decide_with_mixed_finite_and_numerical_data()
    test_treat_gap_between_numerical_values_as_undecidable()
    test_treat_gap_between_same_values_as_decidable()
    test_can_decide_on_single_numerical_value()
    test_can_handle_a_fuzzy_numerical_boundary()


def test_numerical_evaluations():
    test_produce_a_numerical_result_from_a_single_example()
    test_choose_a_value_from_numerical_outcomes()
    test_can_approximately_add_up()


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


def test_decide_based_on_two_examples_separated_numerically():
    examples = [{'data': {'rainfall': 0.1}, 'conclusion': 'happy'},
                {'data': {'rainfall': 2.7}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 0.0}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 2.9}) == {'sad': 1.0})


def test_can_decide_with_mixed_finite_and_numerical_data():
    examples = [{'data': {'rainfall': 0.1, 'sky': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.1, 'sky': 'cloudy'}, 'conclusion': 'cheerful'},
                {'data': {'rainfall': 2.0, 'sky': 'sunny'}, 'conclusion': 'cheerful'},
                {'data': {'rainfall': 2.0, 'sky': 'cloudy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert (tree.decide({'rainfall': 0.0, 'sky': 'sunny'}) == {'happy': 1.0})
    assert (tree.decide({'rainfall': 2.1, 'sky': 'sunny'}) == {'cheerful': 1.0})
    assert (tree.decide({'rainfall': 0.0, 'sky': 'cloudy'}) == {'cheerful': 1.0})
    assert (tree.decide({'rainfall': 2.1, 'sky': 'cloudy'}) == {'sad': 1.0})


def test_treat_gap_between_numerical_values_as_undecidable():
    examples = [{'data': {'rainfall': 0.1}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.3}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 0.0}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.2}) == {'happy': 0.5, 'sad': 0.5})
    assert(tree.decide({'rainfall': 0.4}) == {'sad': 1.0})


def test_treat_gap_between_same_values_as_decidable():
    examples = [{'data': {'rainfall': 0.1}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.3}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.5}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 0.2}) == {'happy': 1.0})
    assert(approximately(tree.decide({'rainfall': 0.4})) == {'happy': 0.66, 'sad': 0.33})


def test_can_decide_on_single_numerical_value():
    examples = [{'data': {'rainfall': 0.1}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 0.0}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.1}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.2}) == {'happy': 1.0})


def test_can_handle_a_fuzzy_numerical_boundary():
    examples = [{'data': {'rainfall': 0.1}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.2}, 'conclusion': 'sad'},
                {'data': {'rainfall': 0.3}, 'conclusion': 'happy'},
                {'data': {'rainfall': 0.4}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 0.05}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.1}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.15}) == {'happy': 0.5, 'sad': 0.5})
    assert(tree.decide({'rainfall': 0.2}) == {'sad': 1.0})
    assert(approximately(tree.decide({'rainfall': 0.25})) == {'happy': 0.33, 'sad': 0.66})
    assert(tree.decide({'rainfall': 0.3}) == {'happy': 1.0})
    assert(tree.decide({'rainfall': 0.35}) == {'happy': 0.75, 'sad': 0.25})
    assert(tree.decide({'rainfall': 0.4}) == {'sad': 1.0})
    assert(tree.decide({'rainfall': 0.45}) == {'sad': 1.0})


def test_produce_a_numerical_result_from_a_single_example():
    examples = [{'data': {'rainfall': 'high'}, 'conclusion': 2.0}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 'high'}) == {2.0: 1.0})


def test_choose_a_value_from_numerical_outcomes():
    examples = [{'data': {'rainfall': 'high'}, 'conclusion': 2.0},
                {'data': {'rainfall': 'low'}, 'conclusion': 0.0}]
    tree = build(examples)
    assert(tree.decide({'rainfall': 'high'}) == {2.0: 1.0})
    assert(tree.decide({'rainfall': 'low'}) == {0.0: 1.0})


def test_can_approximately_add_up():
    examples = [{'data': {'a': 2.0, 'b': 3.0}, 'conclusion': 5.0},
                {'data': {'a': 0.0, 'b': 2.0}, 'conclusion': 2.0},
                {'data': {'a': 2.0, 'b': 2.0}, 'conclusion': 4.0},
                {'data': {'a': 1.0, 'b': 3.0}, 'conclusion': 4.0}]
    tree = build(examples)
    assert(tree.decide({'a': 0.0, 'b': 2.0}) == {2.0: 1.0})
    assert(tree.decide({'a': 0.0, 'b': 0.0}) == {2.0: 1.0})
    assert(tree.decide({'a': 4.0, 'b': 4.0}) == {5.0: 1.0})


all_tests()
