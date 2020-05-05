### Pure Python Decision Tree

This is not production code. I wrote it for my son to save him time
writing an adventure game. The creatures had a lot of "if" statements
describing the behaviour. This would have allowed
programming by example.

There are no external modules, not even a unit tester. I didn't
want to complicate his project.

In the end, he wanted to code it all himself, but hey, I
learned a bit of AI :).

Usage:

```
    from play_with_decision_trees.decision_tree_builder import build, prune

    examples = [{'data': {'weather': 'sunny'}, 'conclusion': 'happy'},
                {'data': {'weather': 'rainy'}, 'conclusion': 'sad'}]
    tree = build(examples)
    tree = prune(examples, tree)
    print (tree.decide({'weather': 'sunny'}))
    # {'happy': 1.0}
```

You essentially feed it data as a dict.
Each row has a state as a vector in "data" and the associated result in "conclusion".
The result is the chosen conclusion(s) with probabilities when given a partial example.

**Features**:
* The tree builder copes with numerical data as well as labels.
* The decision can cope with missing data, giving probalistic answers.
* The tree can be pruned to avoid overfitting.
* Confidence is linearly interpolated between conclusion boundaries.
