'''
Created on Jul 11, 2013

@author: christian
'''
import numpy as np
from numpy.testing import assert_array_equal

from eelbrain import datasets, plot


def test_map2d():
    "Test plot.SensorMap2d"
    plot.configure_backend(False, False)
    ds = datasets.get_rand(utsnd=True)
    Y = ds['utsnd']
    p = plot.SensorMap2d(Y)

    # plot attributes
    p.set_label_color('g')
    p.set_label_text('idx')

    # connectivity
    p.show_connectivity()
    p.show_connectivity(None)

    # mark sensors
    p.mark_sensors([1, 2])
    p.mark_sensors([0])
    p.remove_markers()

    p.close()


def test_multi():
    "Test plot.SensorMaps"
    plot.configure_backend(False, False)
    ds = datasets.get_rand(utsnd=True)
    Y = ds['utsnd']
    p = plot.SensorMaps(Y)
    roi = [1, 2]
    p.set_selection(roi)
    roi2 = p.get_selection()

    test_range = np.arange(3)
    assert_array_equal(test_range[roi2], test_range[roi], "ROI changed after "
                       "set/get")

    p.close()