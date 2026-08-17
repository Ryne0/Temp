#!/usr/bin/env python3
import numpy as np
import slab2_v04c_official as model

def readxyz_csv(path):
    # Official Slab2 .xyz files in the March 2018 bundle are comma-separated.
    a = np.genfromtxt(path, dtype=float, delimiter=',')
    if a.ndim == 1:
        a = a.reshape(1, -1)
    if a.shape[1] < 3:
        raise ValueError(f'Unexpected Slab2 XYZ shape {a.shape} for {path}')
    return a[:, 0], a[:, 1], a[:, 2]

model.readxyz = readxyz_csv
model.main()
