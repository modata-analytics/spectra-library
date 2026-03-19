# Microbial Reference Library

A Streamlit-based reference library for organizing, filtering, and viewing microbial mass spectrometry reference data.

This application was designed to support curated microbial profiling workflows by allowing users to search organisms, filter by classification, and view associated reference spectra, metadata, and supporting files. The current structure supports bacteria, yeasts, and fungal organisms, with flexibility for future expansion as the library grows.

Developed by modata-analytics.

## Overview

The Microbial Reference Library provides an interactive interface for browsing reference entries tied to mass spectrometry analysis. Users can search by organism name, aliases, descriptive keywords, and metadata fields, then inspect available reference spectra and associated information.

The app is designed to accommodate different biological groups and analytical designations, including:
- Gram-negative bacteria with Lipid A profiles
- Gram-negative organisms with LOS-like profiles
- Gram-positive bacteria with cardiolipin-based profile classification
- Yeast and fungal organisms with sterol-associated profile classification

This framework is intended as a pilot library that can scale into a larger searchable reference database for curated microbial spectral data.

## Current Features

- Interactive Streamlit dashboard
- Search bar with forgiving keyword matching
- Sidebar filters for:
  - Microbe
  - Organism Type
  - Gram Status
  - Analyte Category
  - Replicate Type
- Matching entries table with cleaned column formatting
- Reference spectrum viewer from CSV files
- Optional image display for reference spectra
- Overlay view for comparing multiple entries
- Summary table of library contents
- Visible authorship footer with GitHub link

## Organism Categories Supported

### Bacteria
Bacterial entries can be grouped by:
- Gram-negative
- Gram-positive
- Gram-variable

### Organism Type
The application currently supports:
- Bacterium
- Yeast
- Fungal

### Analyte Categories
The library currently supports:
- Lipid A
- LOS Like
- Cardiolipin Profile
- Sterol Profile

## Example Use Cases

This app can be used to:
- Build a curated microbial reference library
- Organize technical and biological replicate spectra
- Search organisms by shorthand, alias, or descriptive keyword
- Compare spectra across organisms or replicate types
- Maintain a structured microbial spectral reference resource for future analysis

## Repository Structure

A typical project layout is shown below:

```text
microbial-reference-library/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── metadata.csv
    ├── spectra/
    │   ├── escherichia_coli_rep1.csv
    │   ├── klebsiella_pneumoniae_rep1.csv
    │   └── ...
    └── images/
        ├── escherichia_coli_rep1.png
        ├── klebsiella_pneumoniae_rep1.png
        └── ...
