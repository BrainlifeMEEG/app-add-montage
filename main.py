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

# if there's a "tags" field in the _inputs key of config.json, collect it in a list
if '_inputs' in config:
    if 'tags' in config['_inputs'][0]:
        tags = config['_inputs'][0]['tags']


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
fig, axs = plt.subplots(1,2)

axs[0].set_title('Montage')
raw.plot_sensors(show_names=True, axes=axs[0])

axs[1].set_title('Original: '+montage)
cap_montage.plot(axes=axs[1])

# save figure
plt.savefig(os.path.join('out_figs','montage.png'))

# save mne/raw
raw.save(os.path.join('out_dir','raw.fif'), overwrite=True)

dict_json_product = {}

# if in_tags is not empty, add it to the product.json
if 'tags' in locals():
    dict_json_product['tags'] = tags
    

with open('product.json', 'w') as outfile:
    json.dump(dict_json_product, outfile)