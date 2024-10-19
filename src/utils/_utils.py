#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.transforms as transforms
import numpy as np
import scipy as sp
from matplotlib.patches import Ellipse


def prepend_h_0(arr_coef):
    """
    add a_0 = b_0 = c_0 = d_0 = 0 to a coef array.
    """
    arr_coef_ = arr_coef.reshape(len(arr_coef), 4, -1)
    arr_coef_with_h0 = np.array(
        [np.hstack([np.zeros([4, 1]), arr]) for arr in arr_coef_]
    )
    return arr_coef_with_h0.reshape(len(arr_coef), -1)


def cvt_conf2std(conf):
    std = np.sqrt(2) * sp.special.erfinv(np.sqrt(conf))
    return std


def get_pc_scores_for_morphospace(ax, num=5, precision=4, scale=1.0):
    """PC scores for visualizing reconstructed shapes on morphospace

    Parameters
    ----------
    ax : matplotlib.axes.Axes object
        Axes object to get the limits of x and y axes.
    num : int, optional
        Number of PC scores to generate along each axis
        , by default 5
    precision : int, optional
        Precision of PC scores, how many decimal digits to use
        , by default 4
    scale : float, optional
        The PC scores are generated within the range of
        +/- `scale`*xlim and +/-`scale`*ylim of axes, by default 1.0

    Returns
    -------
    _type_
        _description_
    """
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    x_min = scale * x_min
    x_max = scale * x_max
    y_min = scale * y_min
    y_max = scale * y_max

    x_min = np.true_divide(np.floor(x_min * 10**precision), 10**precision)
    x_max = np.true_divide(np.ceil(x_max * 10**precision), 10**precision)
    y_min = np.true_divide(np.floor(y_min * 10**precision), 10**precision)
    y_max = np.true_divide(np.ceil(y_max * 10**precision), 10**precision)

    xrange = np.linspace(x_min, x_max, num)
    yrange = np.linspace(y_min, y_max, num)

    return xrange, yrange


def confidence_ellipse(x, y, ax, n_std=3.0, facecolor="none", **kwargs):
    """
    Generate the confidence ellipse.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson, pval = sp.stats.pearsonr(x, y)

    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse(
        (0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs,
    )

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = (
        transforms.Affine2D()
        .rotate_deg(45)
        .scale(scale_x, scale_y)
        .translate(mean_x, mean_y)
    )

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
