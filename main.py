##This script was used to extract the point count from the images

import matplotlib as mpl
import matplotlib.pyplot as plt

import os

import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience

import pims
import trackpy as tp
##---------##
PixelsPerParticle = 53
minmas = 100
path = ""# path to folder with imigaes
##---------##


@pims.pipeline
def gray(image):
    return image[:, :, 1]  # Take just the green channel


files = os.listdir(path)
frames = []
for file in files:
    frames.append(gray(pims.open(path + "/" + file)))



for i in range(len(frames)):
    f = tp.locate(frames[i], PixelsPerParticle, invert=True, minmass=minmas)
    print(len(f["mass"]))
    tp.annotate(f, frames[i][0])
    
    fig, ax = plt.subplots()
    ax.hist(f['mass'], bins=20)
#plt.show()
# Optionally, label the axes.
    ax.set(xlabel='mass', ylabel='count')
    
    tp.subpx_bias(f)
    plt.show()
