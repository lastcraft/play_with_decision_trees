from decision_tree_builder import build, prune
from metrics_tests import test_statistics
from metrics_tests import test_gain
from math import floor


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


def test_text_label_predicates():
    test_decide_with_just_one_example()
    test_decide_between_two_examples()
    test_conclusion_labels_do_not_affect_the_decision()
    test_datum_labels_do_not_affect_the_decision()
    test_field_names_do_not_affect_the_decision()


def test_logical_deductions():
    test_only_one_conclusion()
    test_two_fields_with_second_one_redundant()
    test_two_fields_with_first_one_redundant()
    test_decide_on_two_union_fields()
    test_decide_on_two_xor_fields()


def test_option_with_many_choices():
    test_can_choose_from_a_three_choice_option()


def test_pruning():
    test_prune_does_nothing_on_decisive_tree()
    test_prune_removes_outliers()
    test_no_pruning_unless_gain_is_less_than_threshold()
    test_can_prune_tree_with_missing_example_data()


def test_deciding_with_missing_data():
    test_with_no_data_result_is_divided()
    test_with_no_data_falls_back_training_weights()
    test_probablity_is_apportioned_down_the_tree()
    test_missing_data_in_examples_is_treated_as_an_option()
    test_missing_example_determines_decision_emphatically_when_test_data_is_missing()


def test_coping_with_unseen_options():
    test_unseen_option_treated_as_missing_data()


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


def test_decide_with_just_one_example():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})


def test_decide_between_two_examples():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rain'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rain'}) == {'sad': 1.0})


def test_conclusion_labels_do_not_affect_the_decision():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'overjoyed'},
                {'data': {'weather': 'rain'}, 'conclusion': 'depressed'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'overjoyed': 1.0})
    assert(tree.decide({'weather': 'rain'}) == {'depressed': 1.0})


def test_datum_labels_do_not_affect_the_decision():
    examples = [{'data': {'weather': 'clear'}, 'conclusion': 'happy'},
                {'data': {'weather': 'precipitation'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'clear'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'precipitation'}) == {'sad': 1.0})


def test_field_names_do_not_affect_the_decision():
    examples = [{'data': {'climate': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'climate': 'rain'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'climate': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'climate': 'rain'}) == {'sad': 1.0})


def test_only_one_conclusion():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})


def test_two_fields_with_second_one_redundant():
    examples = [{'data': {'weather': 'sunny', 'horoscope': 'bad'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'bad'}, 'conclusion': 'sad'},
                {'data': {'weather': 'sunny', 'horoscope': 'good'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'good'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'bad'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'good'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'bad'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'good'}) == {'sad': 1.0})


def test_two_fields_with_first_one_redundant():
    examples = [{'data': {'weather': 'sunny', 'horoscope': 'bad'}, 'conclusion': 'sad'},
                {'data': {'weather': 'rainy', 'horoscope': 'bad'}, 'conclusion': 'sad'},
                {'data': {'weather': 'sunny', 'horoscope': 'good'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'good'}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'bad'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'good'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'bad'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'good'}) == {'happy': 1.0})


def test_decide_on_two_union_fields():
    examples = [{'data': {'weather': 'sunny', 'horoscope': 'bad'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'bad'}, 'conclusion': 'sad'},
                {'data': {'weather': 'sunny', 'horoscope': 'good'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'good'}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'bad'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'good'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'bad'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'good'}) == {'happy': 1.0})


def test_decide_on_two_xor_fields():
    examples = [{'data': {'weather': 'sunny', 'horoscope': 'bad'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy', 'horoscope': 'bad'}, 'conclusion': 'sad'},
                {'data': {'weather': 'sunny', 'horoscope': 'good'}, 'conclusion': 'sad'},
                {'data': {'weather': 'rainy', 'horoscope': 'good'}, 'conclusion': 'happy'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'bad'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'sunny', 'horoscope': 'good'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'bad'}) == {'sad': 1.0})
    assert(tree.decide({'weather': 'rainy', 'horoscope': 'good'}) == {'happy': 1.0})


def test_can_choose_from_a_three_choice_option():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'cloudy'}, 'conclusion': 'cheerful'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'cloudy'}) == {'cheerful': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})


def test_prune_does_nothing_on_decisive_tree():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})


def test_prune_removes_outliers():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'}] * 99
    examples += [{'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree, threshold=0.1)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'happy': 1.0})


def test_no_pruning_unless_gain_is_less_than_threshold():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'}] * 99
    examples += [{'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree, threshold=0.01)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})


def test_with_no_data_result_is_divided():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({}) == {'happy': 0.5, 'sad': 0.5})


def test_with_no_data_falls_back_training_weights():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(approximately(tree.decide({})) == {'happy': 0.66, 'sad': 0.33})


def test_missing_data_in_examples_is_treated_as_an_option():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'cheerful'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({}) == {'cheerful': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})


def test_missing_example_determines_decision_emphatically_when_test_data_is_missing():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'cheerful'}]
    tree = build(examples)
    assert(tree.decide({}) == {'cheerful': 1.0})


def test_probablity_is_apportioned_down_the_tree():
    examples = [{'data': {'sky': 'sunny', 'rain': 'no'}, 'conclusion': 'happy'},
                {'data': {'sky': 'cloudy', 'rain': 'no'}, 'conclusion': 'cheerful'},
                {'data': {'sky': 'sunny', 'rain': 'yes'}, 'conclusion': 'confused'},
                {'data': {'sky': 'cloudy', 'rain': 'yes'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({}) == {'happy': 0.25, 'sad': 0.25,
                               'cheerful': 0.25, 'confused': 0.25})


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
