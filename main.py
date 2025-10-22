##This script was used to extract the point count from the images

import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.odr as odr

import os

import numpy as np

import pims
import trackpy as tp
##---------##
PixelsPerParticle = 25
minmas = 1200
path = "C:/Users/trist/OneDrive/Documents/DinoCapture 3.0/poging2"# path to folder with imigaes
##---------##


@pims.pipeline
def gray(image):
    return image[:, :, 1]  # Take just the green channel

direct = os.listdir(path)

class dataPoint:
    def __init__(self, avarage, std, name):
        self.avarage = avarage
        self.std = std
        self.name = name
datapoints = []

for directory in range(15):
    npath = path + "/" + str(directory+1)
    files = os.listdir(npath)
    frames = []
    for file in files:
        frames.append(gray(pims.open(npath + "/" + file)))

    pointsArr = np.zeros(len(frames))

    for i in range(len(frames)):
        f = tp.locate(frames[i], PixelsPerParticle, invert=True, minmass=minmas)
        pointsArr[i] = len(f["mass"])
        print(len(f["mass"]))
        tp.annotate(f, frames[i][0])
        
 #       fig, ax = plt.subplots()
 #       ax.hist(f['mass'], bins=20)
    
  #      ax.set(xlabel='mass', ylabel='count')
    
  #      tp.subpx_bias(f)
   #     plt.show()

    datapoints.append(dataPoint(pointsArr.mean(), pointsArr.std(), directory))

    print("Total detected points: ", pointsArr.sum())
    print("Samples : ", len(frames))
    print("Avarage points : ", pointsArr.mean()-6, " +-", pointsArr.std())
#%%
xassp = [0,5,10,15,20,30,40,55,75,100,130,165,215,300,385]

xass=[]
yass=[]
yerror = []
xerror = []
for i in datapoints:
    xass.append(xassp[int(i.name)]*8e-7)
    yass.append(i.avarage)
    yerror.append(i.std)
    xerror.append(0.5*8e-7)

print(xass)
print(yass)
print(yerror)
print(xerror)
