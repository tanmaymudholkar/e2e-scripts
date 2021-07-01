#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function, division

# In[1]:


# import warnings
# warnings.filterwarnings('ignore')

import numpy as np
np.random.seed(0)
import os, glob

import pyarrow as pa
import pyarrow.parquet as pq

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
# get_ipython().run_line_magic('matplotlib', 'inline')

import os, sys, subprocess, argparse
# import e2e_env, e2e_common, e2e_settings

inputArgumentsParser = argparse.ArgumentParser(description='Create 2D plot of event rechit energy in the endcap/preshower region for the first event in a given parquet file.')
inputArgumentsParser.add_argument('--inputPQFile', required=True, help="Path to input parquet file.")
inputArgumentsParser.add_argument('--outputFolder', required=True, help="Path to output directory in which to store plots.")
inputArgumentsParser.add_argument('--outputFileName', required=True, help="Name of output file.")
inputArguments = inputArgumentsParser.parse_args()

# settings = e2e_settings.Settings("settings.json")

# mass_points = settings.values_["generate_pi0"]["mass_points"]

# Make output folder if it doesn't exist
subprocess.check_call("mkdir -p {o}".format(o=inputArguments.outputFolder), executable="/bin/bash", shell=True)

plt.rcParams["figure.figsize"] = (6,6)

# In[2]:

# Define parquet file
# f = 'IMG/DoublePi0Pt10To200_m0To2600_Eta1p5To2p4_noPU_AODSIM_EE_ES_EEatES_TkatES.parquet.0'
pq_in = pq.ParquetFile(inputArguments.inputPQFile)

# Print schema
print("schema:")
print(pq_in.schema)

# Print metadata
print("metadata:")
print(pq_in.metadata)


# In[3]:


# Read parquet file
X = pq_in.read(columns=['m','pt']).to_pydict() # python dict

# Convert to numpy
ma = np.float32(X['m'])
pt = np.float32(X['pt'])
print("ma.shape:")
print(ma.shape)
print("pt.shape:")
print(pt.shape)

# # Make some plots
# plt.hist(ma, histtype='step', range=(0.,2.6), bins=50)
# plt.show()

# plt.hist(pt, histtype='step', range=(0.,200.), bins=50)
# plt.show()

# plt.hist2d(ma, pt, range=((0.,2.6),(25.,200.)), bins=10)
# plt.show()


# # In[4]:


# # Invert normalized ma v pt occupancy to derive wgts for mapping distribution to a uniform one
# hmvpt, m_edges, pt_edges = np.histogram2d(np.array(ma).flatten(), np.array(pt).flatten(), range=((0.,2.6),(25.,200.)), bins=10)
# print(' >> hist, min:%f, mean:%f, max:%f'%(hmvpt.min(), hmvpt.mean(), hmvpt.max()))

# hmvpt = 1.*hmvpt/hmvpt.sum()
# lhood = 1./hmvpt
# lhood = lhood/(10.*10.)
# print(' >> likelihood, min:%f, max:%f'%(lhood.min(), lhood.max()))
# print(' >> sum(l):%f'%(lhood.sum()))
# print(' >> sum(h*l):%f'%((hmvpt*lhood).sum()))
# plt.imshow(lhood.T, origin='lower')
# plt.colorbar()
# plt.show()


# In[5]:
# Plot ES granularity images one channel at a time
def plot_ES_composite(img, ax, vmin=1.e-5, vmax=None, cmap='gist_heat_r', alpha=1., colorbar=False, dolog=False): #gist_heat_r

    # Only plots single channel, single sample images
    img = img.squeeze()
    #img[img < 1.e-3] = 0.
    assert len(img.shape) == 2
    
    vmax_ = img.max() if vmax is None else vmax
    vmax_ = 1. if vmax_ == 0. else vmax_
    
    #fig, ax = plt.subplots()
    if dolog:
        im = ax.imshow(img, vmin=vmin, vmax=vmax_, cmap=cmap, alpha=alpha, origin='lower', norm=LogNorm())
    else:
        im = ax.imshow(img, vmin=vmin, vmax=vmax_, cmap=cmap, alpha=alpha, origin='lower')
    #ax.figure.colorbar(im, ax=ax, fraction=0.0228, pad=0.015, label='Energy [GeV]')
    if colorbar:
        ax.figure.colorbar(im, ax=ax, fraction=0.0469, pad=0.015, label='Energy [GeV]')

    #'''
    # By default, imshow() places tick marks at center of image pixel, 
    # so need to shift to the low side by 0.5 to match DQM convention
    # of ticks being placed on low edge of bin
    off = 0.5

    if img.shape[0] == 1280:
        tick_range = np.arange(0,img.shape[0]+128,128)
        # Set image coordinates where ticks should appear...
        ax.set_xticks(tick_range-off)
        ax.set_yticks(tick_range-off)
        # then set what values should be displayed at these coordinates
        ax.set_xticklabels(tick_range)
        ax.set_yticklabels(tick_range)
    elif img.shape[0] % 32 == 0.:
        n_ticks = img.shape[0]//32
        tick_range = np.arange(0,img.shape[0]+32,32)
        # Set image coordinates where ticks should appear...
        ax.set_xticks(tick_range-off)
        ax.set_yticks(tick_range-off)
        # then set what values should be displayed at these coordinates
        ax.set_xticklabels(tick_range)
        ax.set_yticklabels(tick_range)
    #'''

    # Make ticks face inward
    ax.xaxis.set_tick_params(direction='in', which='major', length=6.)
    ax.xaxis.set_tick_params(direction='in', which='minor', length=3.)
    ax.yaxis.set_tick_params(direction='in', which='major', length=6.)
    ax.yaxis.set_tick_params(direction='in', which='minor', length=3.)

    #plt.show()
    #plt.close()

# In[6]:
# Read sample iSample from parquet file
iSample = 0
X = pq_in.read_row_group(iSample, columns=['X_cms']).to_pydict() # python dict

# Convert to numpy array
Xcms = np.float32(X['X_cms']).squeeze() # multi-channel ES-granularity image array
print(Xcms.shape)

# img channel indices
idx_ESX = 0
idx_ESY = 1
idx_EE  = 2

# Make composite plot
fig, ax = plt.subplots()
# EE
plot_ES_composite(Xcms[idx_EE], ax, cmap='Greys', alpha=0.8, dolog=True)
# ESX + ESY
plot_ES_composite(Xcms[idx_ESX]+Xcms[idx_ESY], ax, cmap='jet',alpha=0.7, dolog=True)
plt.xlabel('strip X')
plt.ylabel('strip Y')
plt.xlabel(r"$\mathrm{strip_{X}}'$", size=24)
plt.ylabel(r"$\mathrm{strip_{Y}}'$", size=24)
plt.savefig("{o}/{ofn}".format(o=inputArguments.outputFolder, ofn=inputArguments.outputFileName))


# # In[7]:
# # Make histogram of hit intensities for each channel

# hits = {}

# nChannels = 3 # ESX, ESY, EE
# for iC in range(nChannels):
#     hits[iC] = []

# nSamples = 500
# for iS in range(nSamples):
#     if iS%100 == 0: print(iS)
#     X = pq_in.read_row_group(iS, columns=['X_cms']).to_pydict()
#     Xcms = np.float32(X['X_cms'])
#     #print(Xcms.shape)
#     for iC in range(nChannels):
#         hits[iC].append(Xcms[:,iC])

# # Convert to numpy and flatten
# for iC in range(nChannels):
#     hits[iC] = np.concatenate(hits[iC]).flatten()
#     print(hits[iC].shape)


# # In[8]:


# # Histogram intensities after scaling hits
# labels = ['ESX', 'ESY', 'EE']
# scale = [2.e4, 2.e4, 20.] # TODO: tune me to be in ~(0, 1)
# for iC in range(nChannels):
#     plt.hist(hits[iC][hits[iC]>0.]*scale[iC], label=labels[iC], histtype='step', bins=60, log=True, range=(0.,80.)) #range=(0.,1.)
# plt.xlabel('hit intensity, scaled')
# plt.legend()
# plt.show()

print("All done!")
