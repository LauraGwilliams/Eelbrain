'''Eelbrain GUIs'''


def run():
    "Hand over command to the GUI (quit the GUI to return to the terminal)"
    from . import _wxgui
    _wxgui.run()


def select_epochs(*args, **kwargs):
    """GUI for rejecting trials

    Parameters
    ----------
    ds : Dataset | mne.Epochs
        The data for which to select trials. If ds is an mne.Epochs object
        the subsequent parameters up to 'trigger' are irrelevant.
    data : str
        Name of the epochs data in ds.
    accept : str
        Name of the boolean Var in ds to accept or reject epochs.
    blink : str
        Name of the eye tracker data in ds.
    tag : str
        Name of the rejection tag (storing the reason for rejecting a
        specific epoch).
    trigger : str
        Name of the int Var containing the event trigger for each epoch
        (used to assert that when loading a rejection file it comes from
        the same data).
    path : None | str
        Path to the desired rejection file. If the file already exists it
        is loaded as starting values. The extension determines the format
        (``*.pickled`` or ``*.txt``).
    nplots : None | int | tuple of 2 int
        Number of epoch plots per page. Can be an ``int`` to produce a
        square layout with that many epochs, or an ``(n_rows, n_columns)``
        tuple. The default is to use the settings from the last session.
    topo : None | bool
        Show a topomap plot of the time point under the mouse cursor.
        Default (None): use settings form last session.
    mean : None | bool
        Show a plot of the page mean at the bottom right of the page.
        Default (None): use settings form last session.
    vlim : None | scalar
        Limit of the epoch plots on the y-axis. If None, a value is
        determined automatically to show all data.
    color : None | matplotlib color
        Color for primary data (default is black).
    lw : scalar
        Linewidth for normal sensor plots.
    mark : None | index for sensor dim
        Sensors to plot as individual traces with a separate color.
    mcolor : matplotlib color
        Color for marked traces.
    mlw : scalar
        Line width for marked sensor plots.
    antialiased : bool
        Perform Antialiasing on epoch plots (associated with a minor speed
        cost).
    pos : None | tuple of 2 int
        Window position on screen. Default (None): use settings form last
        session.
    size : None | tuple of 2 int
        Window size on screen. Default (None): use settings form last
        session.
    allow_interpolation : bool
        Whether to allow interpolating individual channels by epoch (default
        True).

    Notes
    -----
    Exclude bad epochs and interpolate or remove bad channels.

    * Use the `Bad Channels` button in the toolbar to exclude channels from
      analysis (use the `GA` button to plot the grand average and look for
      channels that are consistently bad).
    * Click the `Threshold` button to automatically reject epochs in which the
      signal exceeds a certain threshold.
    * Click on an epoch plot to toggle rejection of that epoch.
    * Press ``i`` on the keyboard to toggle channel interpolation for the
      channel that is closest to the cursor along the y-axis.
    * Press ``shift-i`` on the keyboard to edit a list of interpolated channels
      for the epoch under the cursor.


    *Keyboard shortcuts* in addition to the ones in the menu:

    =========== ============================================================
    Key         Effect
    =========== ============================================================
    right-arrow go to the next page
    left-arrow  go to the previous page
    b           butterfly plot of the epoch under the pointer
    c           pairwise sensor correlation plot or the current epoch
    t           topomap plot of the epoch/time point under the pointer
    i           interpolate the channel nearest to the pointer on the y-axis
    shift-i     open dialog to enter channels for interpolation
    =========== ============================================================
    """
    from . import _wxgui
    _wxgui.select_epochs.TerminalInterface(*args, **kwargs)
