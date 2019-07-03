from math import log
log2 = lambda x: log(x) / log(2)


def calculate_gain(both, yesses, nos):
    return entropy(both) \
        - len(yesses)/len(both) * entropy(yesses) \
        - len(nos)/len(both) * entropy(nos)


def variance(examples):
    mean = sum([example['conculsion'] for example in examples])
    return sum([(example['conclusion'] - mean) ** 2 for example in examples])


def entropy(examples):
    probabilities = probability_distribution(examples)
    total_entropy = 0.0
    for key, probability in probabilities.iteritems():
        total_entropy -= probability * log2(probability)
    return total_entropy


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
