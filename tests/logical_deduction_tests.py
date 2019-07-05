from decision_tree_builder import build


def test_logical_deductions():
    test_only_one_conclusion()
    test_two_fields_with_second_one_redundant()
    test_two_fields_with_first_one_redundant()
    test_decide_on_two_union_fields()
    test_decide_on_two_xor_fields()


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