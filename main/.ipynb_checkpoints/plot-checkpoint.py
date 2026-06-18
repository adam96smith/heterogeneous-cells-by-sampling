'''
Script for plotting the synthetic data to compare augmentations.
'''

import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
import h5py
import argparse
from utils.quality_measures import custom_het_i_calc # for surface heterogeneity
from scipy.ndimage import center_of_mass

parser = argparse.ArgumentParser(description='Sample Real Fluorecence for Synthetic Images.')
parser.add_argument('--mode', default='tif',
                    help='Config. File for Sampler')
args = parser.parse_args()

assert args.mode in ['tif']
sampling = (.49,.1,.1)

data_dir = 'synthetic_data/lipid_bilayer_vesicles/'
masks = [imread(f'{data_dir}mask_{str(i+1).zfill(5)}.{args.mode}')[0] for i in range(3)]
baseline_imgs = [imread(f'{data_dir}base_texture/image_{str(i+1).zfill(5)}.{args.mode}')[0] for i in range(3)]
specking_imgs = [imread(f'{data_dir}speckling_texture/image_{str(i+1).zfill(5)}.{args.mode}')[0] for i in range(3)]
width_scaling_imgs = [imread(f'{data_dir}width_scaling_texture/image_{str(i+1).zfill(5)}.{args.mode}')[0] for i in range(3)]
combined_imgs = [imread(f'{data_dir}combined_texture/image_{str(i+1).zfill(5)}.{args.mode}')[0] for i in range(3)]

# plot the z_slice with largest cross section

slices = []
for m in masks:
    v = np.sum(np.sum(m, axis=2),axis=1)
    slices.append( np.argmax(v) )

fig, axes = plt.subplots(3, 5, figsize=(12,7))
fs = 12.5

for i in range(3):
    zs = slices[i]

    vmin = np.quantile(baseline_imgs[i], .01)
    vmax = np.quantile(baseline_imgs[i], .99)
    axes[i, 0].imshow(masks[i][zs])
    axes[i, 1].imshow(baseline_imgs[i][zs], cmap='inferno', vmin=vmin, vmax=vmax)
    axes[i, 2].imshow(specking_imgs[i][zs], cmap='inferno', vmin=vmin, vmax=vmax)
    axes[i, 3].imshow(width_scaling_imgs[i][zs], cmap='inferno', vmin=vmin, vmax=vmax)
    axes[i, 4].imshow(combined_imgs[i][zs], cmap='inferno', vmin=vmin, vmax=vmax)

    # annotate surface heterogeneity
    for v in np.unique(masks[i][zs])[1:]:

        base_het = custom_het_i_calc(baseline_imgs[i],
                                     (masks[i] == v).astype(int),
                                     spacing=sampling,
                                     max_depth=1.0,
                                     operation='mean')[0]
        spec_het = custom_het_i_calc(specking_imgs[i],
                                     (masks[i] == v).astype(int),
                                     spacing=sampling,
                                     max_depth=1.0,
                                     operation='mean')[0]
        wsca_het = custom_het_i_calc(width_scaling_imgs[i],
                                     (masks[i] == v).astype(int),
                                     spacing=sampling,
                                     max_depth=1.0,
                                     operation='mean')[0]
        comb_het = custom_het_i_calc(combined_imgs[i],
                                     (masks[i] == v).astype(int),
                                     spacing=sampling,
                                     max_depth=1.0,
                                     operation='mean')[0]
        
        cm = center_of_mass(masks[i][zs]==v)

        if np.sum(masks[i][zs]==v) < 7500: # smaller vesicles annotate below
            xres, yres = masks[i][zs].shape
            X,Y = np.meshgrid(np.arange(xres), np.arange(yres))

            cm = (np.max(Y[masks[i][zs]==v]) + 20, cm[1])

        axes[i, 1].annotate(f'{base_het:.3f}', (cm[1],cm[0]), color='w', va='center',ha='center', weight='bold', fontsize=12.5)
        axes[i, 2].annotate(f'{spec_het:.3f}', (cm[1],cm[0]), color='w', va='center',ha='center', weight='bold', fontsize=12.5)
        axes[i, 3].annotate(f'{wsca_het:.3f}', (cm[1],cm[0]), color='w', va='center',ha='center', weight='bold', fontsize=12.5)
        axes[i, 4].annotate(f'{comb_het:.3f}', (cm[1],cm[0]), color='w', va='center',ha='center', weight='bold', fontsize=12.5)

        

axes[0,0].set_title('Masks', fontsize=fs)
axes[0,1].set_title('Baseline', fontsize=fs)
axes[0,2].set_title('Speckling', fontsize=fs)
axes[0,3].set_title('Width Scaling', fontsize=fs)
axes[0,4].set_title('Combined', fontsize=fs)

fig.tight_layout()

fig.savefig('figs/example.png', dpi=100)