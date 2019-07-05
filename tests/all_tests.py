from tests.logical_deduction_tests import test_logical_deductions
from tests.many_choices_tests import test_option_with_many_choices
from tests.metrics_tests import test_statistics, test_gain
from tests.label_predicate_tests import test_text_label_predicates
from tests.missing_data_tests import test_deciding_with_missing_data, test_coping_with_unseen_options
from tests.numeric_tests import test_choosing_from_numerical_data, test_numerical_evaluations
from tests.pruning_tests import test_pruning


def all_tests():
    test_statistics()
    test_gain()
    test_text_label_predicates()
    test_logical_deductions()
    test_option_with_many_choices()
    test_pruning()
    test_deciding_with_missing_data()
    test_coping_with_unseen_options()
    test_choosing_from_numerical_data()
    test_numerical_evaluations()


all_tests()
