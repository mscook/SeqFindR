from context import util
from context import pytest


def test_del_from_list():
    """
    Test the del_from_list function

    Function signature::
        del_from_list(target, index_positions)
    """
    # Standard
    test1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    del_me = [0, 3, 10]
    ret = util.del_from_list(test1, del_me)
    assert ret == [1, 2, 4, 5, 6, 7, 8, 9]

    # Empty initial list
    test2 = []
    del_me = [1]
    with pytest.raises(ValueError):
        ret = util.del_from_list(test2, del_me)

    # Not possible
    test3 = [1, 2, 3]
    del_me = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        ret = util.del_from_list(test3, del_me)

    # Negative indexes
    test4 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    del_me = [-3, -10]
    with pytest.raises(ValueError):
        ret = util.del_from_list(test4, del_me)

    # Index that does not exist
    test5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    del_me = [11]
    with pytest.raises(ValueError):
        ret = util.del_from_list(test5, del_me)

    # Index that does not exist x 2
    test5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    del_me = [10]
    ret = util.del_from_list(test5, del_me)
    assert ret == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
