"""Create tables from data-objects"""
# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>

from __future__ import division

from itertools import izip
import re

import numpy as np

from . import fmtxt
from ._data_obj import (ascategorial, asvar, asndvar, assub, isfactor, isuv,
                        isinteraction, Dataset, Factor, Var, Celltable, combine,
                        cellname, as_legal_dataset_key)


def difference(y, x, c1, c0, match, by=None, sub=None, ds=None):
    """Subtract data in one cell from another

    Parameters
    ----------
    y : Var | NDVar
        Dependent variable.
    x : categorial
        Model for subtraction.
    c1 : str | tuple
        Name of the cell in ``x`` that forms the minuend.
    c0 : str | tuple
        Name of the cell in ``x`` that is to be subtracted from ``c1``.
    match : categorial
        Units over which measurements were repeated.
    by : None | categorial
        Grouping variable to define cells for which to calculate differences.
    sub : None | index
        Only include a subset of the data.
    ds : None | Dataset
        If a Dataset is specified other arguments can be str instead of
        data-objects and will be retrieved from ``ds``.

    Returns
    -------
    diff : Dataset
        Dataset with the difference between ``c1`` and ``c0`` on ``y``.
    """
    sub = assub(sub, ds)
    x = ascategorial(x, sub, ds)
    out = Dataset()
    if by is None:
        ct = Celltable(y, x, match, sub, ds=ds)
        out.add(ct.groups[c1])
        if not ct.all_within:
            raise ValueError("Design is not fully balanced")
        yname = y if isinstance(y, basestring) else ct.Y.name
        out[yname] = ct.data[c1] - ct.data[c0]
    else:
        by = ascategorial(by, sub, ds)
        ct = Celltable(y, x % by, match, sub, ds=ds)
        if not ct.all_within:
            raise ValueError("Design is not fully balanced")

        yname = y if isinstance(y, basestring) else ct.Y.name
        dss = []
        if isinstance(c1, str):
            c1 = (c1,)
        if isinstance(c0, str):
            c0 = (c0,)
        for cell in by.cells:
            if isinstance(cell, str):
                cell = (cell,)
            cell_ds = Dataset()
            cell_ds.add(ct.groups[c1 + cell])
            cell_ds[yname] = ct.data[c1 + cell] - ct.data[c0 + cell]
            if isfactor(by):
                cell_ds[by.name, :] = cell[0]
            else:
                for b, c in zip(by.base, cell):
                    cell_ds[b.name, :] = c
            dss.append(cell_ds)
        out = combine(dss)

    return out


def frequencies(y, x=None, of=None, sub=None, ds=None):
    """Calculate frequency of occurrence of the categories in ``y``

    Parameters
    ----------
    y : categorial
        Factor with values whose frequencies are of interest.
    x : None | categorial
        Optional model defining cells for which frequencies are displayed
        separately.
    of : None | categorial
        With ``x`` constant within ``of``, only count frequencies for each value
        in ``of`` once. (Compress y and x before calculating frequencies.)
    sub : None | index
        Only use a subset of the data.
    ds : Dataset
        If ds is specified, other parameters can be strings naming for
        variables in ``ds``.

    Returns
    -------
    freq : Dataset
        Dataset with frequencies.
    """
    sub = assub(sub, ds)
    y = ascategorial(y, sub, ds)
    if x is not None:
        x = ascategorial(x, sub, ds)
    if of is not None:
        of = ascategorial(of, sub, ds)
        y = y.aggregate(of)
        if x is not None:
            x = x.aggregate(of)

    # find name
    if getattr(y, 'name', None):
        name = "Frequencies of %s" % y.name
    else:
        name = "Frequencies"

    # special case
    if x is None:
        out = Dataset(name=name)
        out['cell'] = Factor(y.cells, random=y.random)
        n = np.fromiter((np.sum(y == cell) for cell in y.cells), int,
                        len(y.cells))
        out['n'] = Var(n)
        return out

    # header
    if getattr(x, 'name', None):
        name += ' by %s' % x.name
    out = Dataset(name=name)

    if isinteraction(x):
        for i, f in enumerate(x.base):
            random = getattr(f, 'random', False)
            out[f.name] = Factor((c[i] for c in x.cells), random=random)
    else:
        out[x.name] = Factor(x.cells)

    y_idx = {cell: y == cell for cell in y.cells}
    x_idx = {cell: x == cell for cell in x.cells}
    for y_cell in y.cells:
        n = (np.sum(np.logical_and(y_idx[y_cell], x_idx[x_cell]))
             for x_cell in x.cells)
        name = as_legal_dataset_key(cellname(y_cell, '_'))
        out[name] = Var(np.fromiter(n, int, len(x.cells)))

    return out


def melt(name, cells, cell_var_name, ds):
    """
    Restructure a Dataset such that a measured variable is in a single column

    Restructure a Dataset with a certain variable represented in several
    columns into a longer dataset in which the variable is represented in a
    single column along with an identifying variable.

    Parameters
    ----------
    name : str
        Name of the variable in the new Dataset.
    cells : sequence of str | str
        Names of the columns representing the variable in the input Dataset.
        Names can either pe specified explicitly as a sequence of str, or
        implicitly as a str containing '%i' for an integer.
    cell_var_name : str
        Name of the variable to contain the cell identifier.
    ds : Dataset
        Input Dataset.
    """
    # find source cells
    if isinstance(cells, basestring):
        cell_expression = cells
        cells = []
        cell_values = []
        if '%i' in cell_expression:
            pattern = cell_expression.replace('%i', '(\d+)')
            for key in ds:
                m = re.match(pattern, key)
                if m:
                    cells.append(key)
                    cell_values.append(int(m.group(1)))
    else:
        cell_values = cells

    # melt the Dataset
    dss = []
    for cell, cell_value in izip(cells, cell_values):
        cell_ds = ds.copy()
        cell_ds.rename(cell, name)
        for src in cells:
            if src != cell:
                del cell_ds[src]
        cell_ds[cell_var_name, :] = cell_value
        dss.append(cell_ds)
    out = combine(dss)
    return out


def melt_ndvar(ndvar, dim=None, cells=None, ds=None, varname=None):
    """
    Transform data to long format by converting an NDVar dimension into a variable

    Parameters
    ----------
    ndvar : NDVar | str
        The NDVar (or name of the NDVar in ``ds``).
    dim : str
        The name of the dimension that should be unwrapped (optional if
        ``ndvar`` has only one non-case dimension).
    cells : sequence
        The values on ``dim`` that should be included in the output Dataset
        (default is to include all values).
    ds : Dataset
        Dataset with additional variables that should be included in the long
        table.
    varname : str
        Name for the transformed ``ndvar`` (default is ``ndvar.name``).

    Returns
    -------
    long_table : Dataset
        Dataset in long format.
    """
    ndvar = asndvar(ndvar, ds=ds)
    if dim is None:
        if ndvar.ndim == ndvar.has_case + 1:
            dim = ndvar.dims[-1]
            dimname = dim.name
        else:
            raise ValueError("The ndvar has more than one possible dimensions, "
                             "the dim parameter must be one of %s"
                             % repr(ndvar.dimnames[ndvar.has_case:]))
    else:
        dimname = dim
        dim = ndvar.get_dim(dimname)

    if cells is None:
        cells = dim.values

    if varname is None:
        if ndvar.name is None:
            raise TypeError("Need to provide a name")
        varname = ndvar.name

    if ds is None:
        base_ds = Dataset()
    else:
        uv_keys = tuple(k for k, v in ds.iteritems() if isuv(v))
        base_ds = ds[uv_keys]

    dss = []
    for cell in cells:
        ds_ = base_ds.copy()
        ds_[varname] = ndvar.sub(**{dimname: cell})
        ds_[dimname, :] = cell
        dss.append(ds_)
    return combine(dss)


def stats(y, row, col=None, match=None, sub=None, fmt='%.4g', funcs=[np.mean],
          ds=None):
    """Make a table with statistics

    Parameters
    ----------
    y : Var
        Dependent variable.
    row : categorial
        Model specifying rows
    col : categorial | None
        Model specifying columns.
    funcs : list of callables
        A list of statistics functions to show (all functions must take an
        array argument and return a scalar).
    ds : Dataset
        If a Dataset is provided, y, row, and col can be strings specifying
        members.


    Examples
    --------
    >>> ds = datasets.get_uts()
    >>> table.stats('Y', 'A', 'B', ds=ds)
                B
         -----------------
         b0        b1
    ----------------------
    a0   0.1668    -0.3646
    a1   -0.4897   0.8746

    >>> A.table.stats(Y, condition, funcs=[np.mean, np.std])
    Condition   mean     std
    ----------------------------
    control     0.0512   0.08075
    test        0.2253   0.2844

    """
    y = asvar(y, ds=ds)
    row = ascategorial(row, ds=ds)

    if col is None:
        ct = Celltable(y, row, sub=sub, match=match)

        # table header
        n_disp = len(funcs)
        table = fmtxt.Table('l' * (n_disp + 1))
        table.cell('Condition', 'bf')
        for func in funcs:
            table.cell(func.__name__, 'bf')
        table.midrule()

        # table entries
        for cell in ct.cells:
            data = ct.data[cell]
            table.cell(cell)
            for func in funcs:
                table.cell(fmt % func(data.x))
    else:
        col = ascategorial(col, ds=ds)
        ct = Celltable(y, row % col, sub=sub, match=match)

        N = len(col.cells)
        table = fmtxt.Table('l' * (N + 1))

        # table header
        table.cell()
        table.cell(col.name, width=N, just='c')
        table.midrule(span=(2, N + 1))
        table.cell()

        table.cells(*col.cells)
        table.midrule()

        # table body
        fmt_n = fmt.count('%')
        if fmt_n == 1:
            fmt_once = False
        elif len(funcs) == fmt_n:
            fmt_once = True
        else:
            raise ValueError("fmt does not match funcs")

        for Ycell in row.cells:
            table.cell(Ycell)
            for Xcell in col.cells:
                # construct address
                a = ()
                if isinstance(Ycell, tuple):
                    a += Ycell
                else:
                    a += (Ycell,)
                if isinstance(Xcell, tuple):
                    a += Xcell
                else:
                    a += (Xcell,)

                # cell
                data = ct.data[a]
                values = (f(data.x) for f in funcs)
                if fmt_once:
                    txt = fmt % values
                else:
                    txt = ', '.join((fmt % v for v in values))

                table.cell(txt)

    return table


def repmeas(y, x, match, sub=None, ds=None):
    """Create a repeated-measures table

    Parameters
    ----------
    y :
        Dependent variable (can be model with several dependents).
    x : categorial
        Model defining the cells that should be restructured into variables.
    match : categorial
        Model identifying the source of the measurement across repetitions,
        i.e. the model that should be retained.
    sub :
        boolean array specifying which values to include (generate e.g.
        with 'sub=T==[1,2]')
    ds : None | Dataset
        If a Dataset is specified other arguments can be str instead of
        data-objects and will be retrieved from ds.

    Returns
    -------
    rm_table : Dataset
        Repeated measures table. Entries for cells of ``x`` correspond to the
        data in ``y`` on these levels of ``x`` (if cell names are not valid
        Dataset keys they are modified).
    """
    ct = Celltable(y, x, match, sub, ds=ds)
    if not ct.all_within:
        raise ValueError("Incomplete data")

    out = Dataset()
    x_ = ct.groups.values()[0]
    if isinteraction(x_):
        for f in x_.base:
            out.add(f)
    else:
        out[ct.match.name] = x_

    for cell in ct.X.cells:
        key = as_legal_dataset_key(cellname(cell, '_'))
        out[key] = ct.data[cell]

    return out
