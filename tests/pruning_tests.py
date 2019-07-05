from decision_tree_builder import build, prune


def test_pruning():
    test_prune_does_nothing_on_decisive_tree()
    test_prune_removes_outliers()
    test_no_pruning_unless_gain_is_less_than_threshold()
    test_can_prune_tree_with_missing_example_data()


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