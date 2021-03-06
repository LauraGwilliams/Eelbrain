*********
Reference
*********

^^^^^^^^^^^^
Data Classes
^^^^^^^^^^^^

.. currentmodule:: eelbrain

Primary data classes:

.. autosummary::
   :toctree: generated

   Dataset
   Factor
   Var
   NDVar
   Datalist


Secondary classes (not usually initialized by themselves but through operations
on primary data-objects):

.. autosummary::
   :toctree: generated

   Interaction
   Model


^^^^^^^^
File I/O
^^^^^^^^

Load
====

.. py:module:: eelbrain.load
.. py:currentmodule:: eelbrain

Eelbrain has its own function for unpickling. In contrast to `normal unpickling
<https://docs.python.org/2/library/pickle.html>`_, this function can also load 
files pickled with earlier Eelbrain versions:

.. autosummary::
   :toctree: generated

   load.unpickle

Modules:

.. autosummary::
   :toctree: generated

   load.eyelink
   load.fiff
   load.txt
   load.besa


Save
====

.. py:module:: eelbrain.save
.. py:currentmodule:: eelbrain

* `Pickling <http://docs.python.org/library/pickle.html>`_: All data-objects
  can be pickled. :func:`save.pickle` provides a shortcut for pickling objects.
* Text file export: Save a Dataset using its :py:meth:`~Dataset.save_txt`
  method. Save any iterator with :py:func:`save.txt`.

.. autosummary::
   :toctree: generated

   save.pickle
   save.txt


^^^^^^^^^^^^^^^^^^^^^^
Sorting and Reordering
^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated

   align
   align1
   choose
   combine
   Celltable
   

^^^^^^^^^^^^^^^^^^^^^
NDVar Transformations
^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated

   cwt_morlet
   labels_from_clusters
   morph_source_space


^^^^^^
Tables
^^^^^^

.. py:module:: eelbrain.table
.. py:currentmodule:: eelbrain

Manipulate data tables and compile information about data objects such as cell
frequencies:

.. autosummary::
   :toctree: generated

    table.difference
    table.frequencies
    table.melt
    table.melt_ndvar
    table.repmeas
    table.stats


^^^^^^^^^^
Statistics
^^^^^^^^^^

.. py:module:: eelbrain.test
.. py:currentmodule:: eelbrain

Univariate statistical tests:

.. autosummary::
   :toctree: generated
   
   test.anova
   test.pairwise
   test.ttest
   test.correlations
   test.lilliefors


^^^^^^^^^^^^^^^^^^^^^^^^^^
Mass-Univariate Statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:module:: eelbrain.testnd
.. py:currentmodule:: eelbrain

.. autosummary::
   :toctree: generated

   testnd.ttest_1samp
   testnd.ttest_rel
   testnd.ttest_ind
   testnd.t_contrast_rel
   testnd.anova
   testnd.corr


By default the tests in this module produce maps of statistical parameters
along with maps of p-values uncorrected for multiple comparison. Using different
parameters, different methods for multiple comparison correction can be applied
(for more details and options see the documentation for individual tests):

**1: permutation for maximum statistic** (``samples=n``)
    Look for the maximum
    value of the test statistic in ``n`` permutations and calculate a p-value
    for each data point based on this distribution of maximum statistics.
**2: Threshold-based clusters** (``samples=n, pmin=p``)
    Find clusters of data
    points where the original statistic exceeds a value corresponding to an
    uncorrected p-value of ``p``. For each cluster, calculate the sum of the
    statistic values that are part of the cluster. Do the same in ``n``
    permutations of the original data and retain for each permutation the value
    of the largest cluster. Evaluate all cluster values in the original data
    against the distributiom of maximum cluster values (see [1]_).
**3: Threshold-free cluster enhancement** (``samples=n, tfce=True``)
    Similar to
    (1), but each statistical parameter map is first processed with the
    cluster-enhancement algorithm (see [2]_). This is the most computationally
    intensive option.

To get information about the progress of permutation tests use
:func:`set_log_level` to change the logging level to 'info'::

    >>> set_log_level('info')


.. [1] Maris, E., & Oostenveld, R. (2007). Nonparametric
    statistical testing of EEG- and MEG-data. Journal of Neuroscience Methods,
    164(1), 177-190. doi:10.1016/j.jneumeth.2007.03.024
.. [2] Smith, S. M., and Nichols, T. E. (2009). Threshold-Free Cluster
    Enhancement: Addressing Problems of Smoothing, Threshold Dependence and
    Localisation in Cluster Inference. NeuroImage, 44(1), 83-98.
    doi:10.1016/j.neuroimage.2008.03.061


.. _ref-plotting:

^^^^^^^^
Plotting
^^^^^^^^

.. py:module:: eelbrain.plot
.. py:currentmodule:: eelbrain


Plot univariate data (:class:`Var` objects):

.. autosummary::
   :toctree: generated

   plot.Barplot
   plot.Boxplot
   plot.PairwiseLegend
   plot.Correlation
   plot.Histogram
   plot.Regression
   plot.Timeplot


Color tools for plotting:

.. autosummary::
   :toctree: generated

   plot.colors_for_categorial
   plot.colors_for_oneway
   plot.colors_for_twoway
   plot.ColorBar
   plot.ColorGrid
   plot.ColorList


Plot uniform time-series:

.. autosummary::
   :toctree: generated

   plot.UTS
   plot.UTSClusters
   plot.UTSStat


Plot multidimensional uniform time series:

.. autosummary::
   :toctree: generated

   plot.Array
   plot.Butterfly


Plot topographic maps of sensor space data:

.. autosummary::
   :toctree: generated

   plot.TopoArray
   plot.TopoButterfly
   plot.Topomap


Plot sensor layout maps:

.. autosummary::
   :toctree: generated

   plot.SensorMap
   plot.SensorMaps


Xax parameter
=============

Many plots have an ``Xax`` parameter. This parameter takes a categorial data
object. The data of the plotted variable will be split into the catories in
``Xax``, and for every cell in ``Xax`` a separate subplot will be plotted.

For example, while

    >>> plot.Butterfly('meg', ds=ds)

will create a single Butterfly plot of the average response,

    >>> plot.Butterfly('meg', 'subject', ds=ds)

where ``'subject'`` is the ``Xax`` parameter, will create a separate subplot
for every subject with its average response.


Layout
======

Most plots that also share certain layout keyword arguments. By default, all
those parameters are determined automatically, but individual values can be
specified manually by supplying them as keyword arguments.

h, w : scalar
    Height and width of the figure.
axh, axw : scalar
    Height and width of the axes.
nrow, ncol : None | int
    Limit number of rows/columns. If neither is specified, a square layout
    is produced
ax_aspect : scalar
    Width / height aspect of the axes.

Plots that do take those parameters can be identified by the ``**layout`` in
their function signature.


GUI Interaction
===============

By default, new plots are automatically shown and, if the Python interpreter is
in interactive mode the GUI main loop is started. This behavior can be
controlled with 2 arguments when constructing a plot:

show : bool
    Show the figure in the GUI (default True). Use False for creating
    figures and saving them without displaying them on the screen.
run : bool
    Run the Eelbrain GUI app (default is True for interactive plotting and
    False in scripts).

The behavior can also be changed globally using :func:`plot.configure`:

.. autofunction:: eelbrain.plot.configure


^^^^^^^^^^^^^^^
Plotting Brains
^^^^^^^^^^^^^^^

.. py:module:: eelbrain.plot.brain
.. py:currentmodule:: eelbrain

:mod:`plot.brain` contains specialized functions to plot :class:`NDVar` objects
containing source space data with mayavi/pysurfer:

.. autosummary::
   :toctree: generated

    plot.brain.activation
    plot.brain.cluster
    plot.brain.dspm
    plot.brain.p_map
    plot.brain.surfer_brain

Other plotting functions:

.. autosummary::
   :toctree: generated

    plot.brain.annot
    plot.brain.annot_legend

Functions that can be applied to the :class:`surfer.Brain` instances that are
returned by the plotting functions:

.. autosummary::
   :toctree: generated

    plot.brain.bin_table
    plot.brain.copy

Plotting functions return a subclass of
`PySurfer <https://pysurfer.github.io/#>`_'s :class:`surfer.Brain` class. This
subclass contains all PySurfer functionalities, and in addition has the
following methods to better interact with Eelbrain:

.. autosummary::
   :toctree: generated

    ~plot._brain_mixin.BrainMixin.image
    ~plot._brain_mixin.BrainMixin.plot_colorbar
    ~plot._brain_mixin.BrainMixin.save_image


.. _ref-guis:

^^^^
GUIs
^^^^

.. py:module:: eelbrain.gui
.. py:currentmodule:: eelbrain

Tools with a graphical user interface (GUI):

.. autosummary::
   :toctree: generated

    gui.select_epochs


.. _gui:

Controlling the GUI Application
===============================

Eelbrain uses a wxPython based application to create GUIs. This application can
not take input form the user at the same time as the shell from which the GUI
is invoked. By default, the GUI application is activated whenever a gui is
created in interactive mode. While the application is processing user input,
the shell can not be used. In order to return to the shell, simply quit the
application (the *python/Quit Eelbrain* menu command or Command-Q). In order to
return to the terminal without closing all windows, use the alternative
*Go/Yield to Terminal* command (Command-Alt-Q). To return to the application
from the shell, run :func:`gui.run`. Beware that if you terminate the Python
session from the terminal, the application is not given a chance to assure that
information in open windows is saved.

.. autosummary::
   :toctree: generated

    gui.run


^^^^^^^^^^^^^^
MNE-Experiment
^^^^^^^^^^^^^^

The :class:`MneExperiment` class serves as a base class for analyzing MEG
data (gradiometer only) with MNE:

.. autosummary::
   :toctree: generated

   MneExperiment

.. seealso::
    For the guide on working with the MneExperiment class see
    :ref:`experiment-class-guide`.


^^^^^^^^
Datasets
^^^^^^^^

.. py:module:: eelbrain.datasets
.. py:currentmodule:: eelbrain

Datasets for experimenting and testing:

.. autosummary::
    :toctree: generated

    datasets.get_loftus_masson_1994
    datasets.get_mne_sample
    datasets.get_uts
    datasets.get_uv
