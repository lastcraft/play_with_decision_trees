from decision_tree_builder import build


def test_text_label_predicates():
    test_decide_with_just_one_example()
    test_decide_between_two_examples()
    test_conclusion_labels_do_not_affect_the_decision()
    test_datum_labels_do_not_affect_the_decision()
    test_field_names_do_not_affect_the_decision()


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