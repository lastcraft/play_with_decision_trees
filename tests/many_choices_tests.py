from decision_tree_builder import build


def test_option_with_many_choices():
    test_can_choose_from_a_three_choice_option()


def test_can_choose_from_a_three_choice_option():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'cloudy'}, 'conclusion': 'cheerful'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    assert(tree.decide({'weather': 'sunny'}) == {'happy': 1.0})
    assert(tree.decide({'weather': 'cloudy'}) == {'cheerful': 1.0})
    assert(tree.decide({'weather': 'rainy'}) == {'sad': 1.0})