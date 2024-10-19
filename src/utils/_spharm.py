#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from ktch.outline import SPHARMCoefficients


def cvt_spharm_coef_SPHARMPDM_to_list(coef_SlicerSALT):
    coef_ = coef_SlicerSALT.reshape((-1, 3))
    lmax = int(np.sqrt(coef_.shape)[0] - 1)
    coef_list = [
        np.array(
            [
                coef_[l**2]
                if m == 0
                else (coef_[l**2 + 2 * m - 1] - coef_[l**2 + 2 * m] * 1j) / 2
                if m > 0
                else ((-1) ** m)
                * (coef_[l**2 + 2 * np.abs(m) - 1] + coef_[l**2 + 2 * np.abs(m)] * 1j)
                / 2
                for m in range(-l, l + 1, 1)
            ]
        )
        for l in range(0, lmax + 1, 1)
    ]

    coefficients = [
        (
            [
                [coef_list[l][m_, i] for m_ in range(2 * l + 1)]
                for l in range(len(coef_list))
            ]
        )
        for i in range(3)
    ]

    coef_x = SPHARMCoefficients()
    coef_y = SPHARMCoefficients()
    coef_z = SPHARMCoefficients()
    coef_x.from_list(coefficients[0])
    coef_y.from_list(coefficients[1])
    coef_z.from_list(coefficients[2])

    coef_list = [coef_x, coef_y, coef_z]

    return coef_list
