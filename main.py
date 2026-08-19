"""
Add electrode montage to MNE raw data.

This app adds a standard electrode montage from the MNE-Python database to raw MEG/EEG data.
It allows setting channel locations for visualization and source localization. Optionally,
channel names can be renamed to match the montage naming convention.

Input:
    - raw: Path to MNE raw data file (.fif format)
    - montage: Name of the standard montage (e.g., 'GSN-HydroCel-257', 'standard_1020')
    - rename_channels: Optional comma-separated list of channel renames (format: old_name-new_name)

Output:
    - out_dir/raw.fif: MNE raw data file with montage applied
    - out_figs/montage.png: Visualization of electrode positions
    - out_report/report.html: QC report with channel information and montage details
    - product.json: Metadata with channel information
"""

# Copyright (c) 2026 brainlife.io
#
# This app adds electrode montages to MNE raw data files.
#
# Authors:
# - Kamilya Salibayeva (https://github.com/KSalibay)
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_raw_info_to_product,
    add_image_to_product,
    save_figure_with_base64
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()

# == LOAD DATA ==
fname = config['raw']
montage_name = config['montage']

# Read raw data
raw = mne.io.read_raw_fif(fname, preload=True)

# == APPLY MONTAGE ==
# Load standard montage
cap_montage = mne.channels.make_standard_montage(montage_name)

# Rename channels if needed
if config.get('rename_channels', '') and config['rename_channels'] != 'None':
    rename_channels = config['rename_channels']
    # Parse comma-separated pairs: "old1-new1,old2-new2"
    rename_ch = dict((x.strip(), y.strip())
                     for x, y in (element.split('-')
                                  for element in rename_channels.split(',')))
    cap_montage.rename_channels(rename_ch)

# Apply montage to raw data
raw.set_montage(cap_montage)

# == CREATE MONTAGE VISUALIZATION ==
fig, axs = plt.subplots(figsize=(12, 10))
plt.sca(axs)
plt.title(f'Electrode Montage: {montage_name}')
raw.plot_sensors(show_names=True, axes=axs)
plt.tight_layout()

# Save figure with base64 encoding
montage_fig_path = os.path.join('out_figs', 'montage.png')
montage_base64 = save_figure_with_base64(fig, montage_fig_path, 
                                         dpi_file=150, dpi_base64=80)

# == CREATE PSD PLOT ==
print("Computing PSD and generating report...", flush=True)
fig = raw.compute_psd().plot(exclude='bads', show=False)
fig.savefig(os.path.join('out_figs', 'psd.png'), dpi=100, bbox_inches='tight')
plt.close(fig)

# == CREATE REPORT ==
report = mne.Report(title='Add Montage Report')
report.add_raw(raw=raw, title='Raw Data with Montage')

# Add montage information to report
montage_info_html = f'<p><b>Montage Applied:</b> {montage_name}</p>'
montage_info_html += '<p><b>Channel Locations:</b></p>'
if config.get('rename_channels', '') and config['rename_channels'] != 'None':
    montage_info_html += '<p><b>Channel Renamings Applied:</b><br>'
    for old_ch, new_ch in rename_ch.items():
        montage_info_html += f'{old_ch} → {new_ch}<br>'
    montage_info_html += '</p>'
report.add_html(title='Montage Details', html=montage_info_html)

# Add montage figure to report
report.add_image(montage_fig_path, title='Electrode Positions')

# Add channel information to report
channel_info_html = '<p><b>Channels in this file:</b></p>' + ', '.join(raw.ch_names)
report.add_html(title='Channels', html=channel_info_html)

# == SAVE DATA ==
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == CREATE PRODUCT JSON ==
product_items = []

# Add structured raw info messages
add_raw_info_to_product(product_items, raw)

# Add montage information
montage_msg = f"Electrode montage '{montage_name}' successfully applied"
add_info_to_product(product_items, montage_msg, msg_type='success')

# Add montage figure with base64 data
add_image_to_product(product_items, 'Electrode Montage', base64_data=montage_base64)

# Add PSD plot if it exists
psd_image_path = os.path.join('out_figs', 'psd.png')
if os.path.exists(psd_image_path):
    add_image_to_product(product_items, name='Power Spectral Density (PSD)', filepath=psd_image_path)

# Create the product.json file
create_product_json(product_items)

