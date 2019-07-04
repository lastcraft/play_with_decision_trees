from metrics import boltzmann_entropy, histogram, probability_distribution


def test_statistics():
    test_histogram_can_count_a_single_conclusion()
    test_histogram_can_count_a_different_conclusion()
    test_distribution_can_measure_many_conclusions()
    test_entropy_of_uniform_set_is_zero()
    test_entropy_of_a_mixed_set_is_bigger_than_zero()


def test_histogram_can_count_a_single_conclusion():
    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'}]
    assert(histogram(examples) == {'happy': 1})


def test_histogram_can_count_a_different_conclusion():
    examples = [{'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'sad'}]
    assert(histogram(examples) == {'happy': 1, 'sad': 1})


def test_distribution_can_measure_many_conclusions():
    examples = [{'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'sad'},
                {'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'sad'}]
    assert(probability_distribution(examples) == {'happy': 0.5, 'sad': 0.5})


def test_entropy_of_uniform_set_is_zero():
    examples = [{'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'happy'}]
    assert(boltzmann_entropy(examples) == 0.0)


def test_entropy_of_a_mixed_set_is_bigger_than_zero():
    examples = [{'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'sad'}]
    assert(boltzmann_entropy(examples) > 0.0)


def test_entropy_of_a_maximally_mixed_set_is_one():
    examples = [{'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'happy'},
                {'data': {}, 'conclusion': 'sad'},
                {'data': {}, 'conclusion': 'sad'}]
    assert(boltzmann_entropy(examples) == 1.0)
