from context import seqfindr
from context import pytest
import numpy as np


def test_strip_uninteresting():
    """
    Test the strip_uninteresting function

    Function signature::

        strip_uninteresting(matrix, query_classes, query_list, cons, invert)
    """
    # No cons
    matrix = np.array([(0.5, 2, 3), (0.5, 5, 6)])
    nm, newqc, newql = seqfindr.strip_uninteresting(matrix, ['a', 'b', 'c'],
                                                    ['a1', 'b1', 'c1'], None,
                                                    False)
    assert newqc == ['b', 'c']
    assert newql == ['b1', 'c1']
    assert nm.all() == np.array([(2, 3), (5, 6)]).all()

    # Cons
    matrix = np.array([(1.0, 1.0, 3), (0.5, 1.0, 6)])
    nm, newqc, newql = seqfindr.strip_uninteresting(matrix, ['a', 'b', 'c'],
                                                    ['a1', 'b1', 'c1'], True,
                                                    False)
    assert newqc == ['a', 'c']
    assert newql == ['a1', 'c1']
    assert nm.all() == np.array([(1.0, 3), (0.5, 6)]).all()


    # Cons, invert
    matrix = np.array([(-1.0, -1.0, -3), (-0.5, -1.0, -6)])
    nm, newqc, newql = seqfindr.strip_uninteresting(matrix, ['a', 'b', 'c'],
                                                    ['a1', 'b1', 'c1'], True,
                                                    True)
    assert newqc == ['a', 'c']
    assert newql == ['a1', 'c1']
    assert nm.all() == np.array([(-1.0, -3), (-0.5, -6)]).all()
