# app-add-montage

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.444-blue.svg)](https://doi.org/10.25663/bl.app.444)

## Description

Adds a standard electrode montage from the MNE-Python database to raw MEG/EEG data. This app sets channel locations for proper visualization, 3D topography mapping, and source localization. It also allows optional channel renaming to match the montage naming convention.

## Inputs

- **raw**: MNE raw data file in `.fif` format

## Outputs

- **out_dir/raw.fif**: Raw data file with montage locations applied
- **out_figs/montage.png**: Visualization of electrode positions on the scalp
- **out_report/report.html**: QC report containing raw data summary and montage information
- **product.json**: Metadata with channel information and montage details

## Configuration Parameters

### Required

- `raw`: Path to the input MNE raw data file (`.fif` format)
- `montage`: Name of the standard montage to apply. Common options include:
  - `standard_1020`: Standard 10-20 system
  - `standard_1005`: Standard 10-05 system
  - `GSN-HydroCel-257`: 257-channel EGI montage
  - `GSN-HydroCel-128`: 128-channel EGI montage
  - See MNE documentation for complete list of available montages

### Optional

- `rename_channels`: Comma-separated list of channel renamings to apply to the montage. Format: `old_name-new_name,old_name2-new_name2` (e.g., "Cz-E257,Pz-E129")

## Usage

The app reads a raw MNE data file, applies the selected standard montage (optionally renaming channels), and generates:
1. A modified `.fif` file with channel locations
2. A PNG visualization of electrode positions
3. An HTML report with QC information
4. A product.json file with metadata

Example configuration:
```json
{
    "raw": "path/to/raw.fif",
    "montage": "GSN-HydroCel-257",
    "rename_channels": "Cz-E257,Pz-E129"
}
```

## Technical Details

- **Execution**: Python with MNE-Python and shared brainlife_utils library
- **Data format**: MNE `.fif` format (compatible with all downstream Brainlife.io apps)
- **Montage source**: MNE-Python's built-in standard montages
- **Visualization**: 3D sensor plot with channel names
- **Report generation**: Automatic HTML report with channel visualization

## Authors

- [Kamilya Salibayeva](https://github.com/KSalibay) (Indiana University)
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

**brainlife.io: A decentralized and open source cloud platform to support neuroscience research**. Hayashi, S., Caron, B. A., et al. & Pestilli, F. (2023). ArXiv. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10274934/

**MEG and EEG data analysis with MNE-Python**. Gramfort A, et al. & Hämäläinen MS. (2013). Frontiers in Neuroscience, 7(267):1–13. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

#### MIT Copyright (c) 2026 brainlife.io The University of Texas at Austin and Indiana University

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
