from math import floor

from decision_tree_builder import build


def test_deciding_with_missing_data():
    test_with_no_data_result_is_divided()
    test_with_no_data_falls_back_training_weights()
    test_probablity_is_apportioned_down_the_tree()
    test_missing_data_in_examples_is_treated_as_an_option()
    test_missing_example_determines_decision_emphatically_when_test_data_is_missing()


def test_coping_with_unseen_options():
    test_unseen_option_treated_as_missing_data()


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


def test_unseen_option_treated_as_missing_data():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'cloudy'}) == {'happy': 0.5, 'sad': 0.5})


def one_dp(number):
    return floor(100 * number)/100.0


def approximately(a_dict):
    return {key: one_dp(value) for key, value in a_dict.iteritems()}