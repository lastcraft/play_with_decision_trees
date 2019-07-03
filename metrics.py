from math import log
log2 = lambda x: log(x) / log(2)


def calculate_gain(both, yesses, nos):
    return measure_entropy(both) \
        - len(yesses)/len(both) * measure_entropy(yesses) \
        - len(nos)/len(both) * measure_entropy(nos)


def variance(examples):
    mean = sum([example['conculsion'] for example in examples])
    return sum([(example['conclusion'] - mean) ** 2 for example in examples])


def measure_entropy(examples):
    probabilities = probability_distribution(examples)
    entropy = 0.0
    for key, probability in probabilities.iteritems():
        entropy -= probability * log2(probability)
    return entropy


def probability_distribution(examples):
    counts = histogram(examples)
    total = sum(counts.values())
    return {key: float(value)/total for key, value in counts.iteritems()}


def histogram(examples):
    counts = {}
    for example in examples:
        if example['conclusion'] not in counts:
            counts[example['conclusion']] = 1
        else:
            counts[example['conclusion']] += 1
    return counts
