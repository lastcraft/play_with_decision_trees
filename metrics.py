from math import log
log2 = lambda x: log(x) / log(2)


def calculate_gain(both, yesses, nos):
    return measure_entropy(probability_distribution(both)) \
        - len(yesses)/len(both) * measure_entropy(probability_distribution(yesses)) \
        - len(nos)/len(both) * measure_entropy(probability_distribution(nos))


def histogram(examples):
    counts = {}
    for example in examples:
        if example['conclusion'] not in counts:
            counts[example['conclusion']] = 1
        else:
            counts[example['conclusion']] += 1
    return counts


def probability_distribution(examples):
    counts = histogram(examples)
    total = sum(counts.values())
    return {key: float(value)/total for key, value in counts.iteritems()}


def measure_entropy(probabilities):
    entropy = 0.0
    for key, probability in probabilities.iteritems():
        entropy -= probability * log2(probability)
    return entropy
