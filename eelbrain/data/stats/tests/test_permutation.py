'''
Created on Sep 13, 2013

@author: Christian M Brodbeck
'''
import logging

from nose.tools import eq_
import numpy as np

from eelbrain.data.stats.permutation import resample
from eelbrain.data import Factor, Var


def test_permutation():
    """Test permutation"""
    v = Var(np.arange(6))
    res = np.empty((5, 6))
    for i, y in enumerate(resample(v, samples=5)):
        res[i] = y.x
    logging.info('Standard Permutation:\n%s' % res)

    # with unit
    s = Factor('abc', tile=2)
    for i, y in enumerate(resample(v, samples=5, unit=s)):
        res[i] = y.x
    logging.info('Permutation with Unit:\n%s' % res)

    # check we have only appropriate cells
    cols = [np.unique(res[:, i]) for i in xrange(res.shape[1])]
    for i in xrange(3):
        eq_(len(np.setdiff1d(cols[i], [i, i + 3])), 0)
    for i in xrange(3, 6):
        eq_(len(np.setdiff1d(cols[i], [i, i - 3])), 0)

    # check we have some variability
    eq_(max(map(len, cols)), 2)