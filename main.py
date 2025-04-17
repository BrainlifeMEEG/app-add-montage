# Copyright (c) 2020 brainlife.io
#
# This file is the main script for applying baseline correction to MEG/EEG Epochs files.
#
# Author: Kamilya Salibayeva
# Indiana University

# set up environment
import os
import json
import mne
import matplotlib.pyplot as plt

# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Populate mne_config.py file with brainlife config.json
with open(__location__+'/config.json') as config_json:
    config = json.load(config_json)

# retrieve config.json parameters
fname = config['raw']
montage = config['montage']

# read raw data and standard montage
raw = mne.io.read_raw_fif(fname, preload=True)
cap_montage = mne.channels.make_standard_montage(montage)

# rename channels if needed
if len(config['rename_channels']) >= 1:
    rename_channels = config['rename_channels']
    rename_ch = dict((x.strip(), y.strip()) 
                     for x, y in (element.split('-')
                                  for element in rename_channels.split(',')))
    cap_montage.rename_channels(rename_ch)
    
raw.set_montage(cap_montage)

# plot montage
fig, axs = plt.subplots(figsize=(15, 15))

plt.title('Montage')
raw.plot_sensors(show_names=True, axes=axs)


# save figure
plt.savefig(os.path.join('out_figs','montage.png'))

# save mne/raw
raw.save(os.path.join('out_dir','raw.fif'), overwrite=True)

