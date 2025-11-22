# SALTA

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17379378.svg)](https://doi.org/10.5281/zenodo.17379378)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

This document describes the usage and troubleshooting of the *SALTA* App. 

---

## USAGE

1. Process the captured performance to extract features
   
   1. Landmarks from video
   
   2. Sound features
   
   3. IMU features

2. Prepare the data

3. Create the JSON exchange files (one per feature)
   
   1. Use [CompareSegments](https://github.com/AdrianArtacho/salta_COMPARESEGMENTS) ([readme](COMPARESEGMENTS/README.md)) to create exchange JSONs.
      
      1. `python BATCH.py` (:exclamation:The feature names need to be written *ToGetHer*)
      
      2. (optional) normalize relative weights: `python feat_relnorm.py`

4. Generate the Probability Density Plots
   
   1. Use [PLOTLY](https://github.com/AdrianArtacho/salta_PLOTLY) ([readme](NOTATION//sandbox/plotly/README.md)) to generate PDPs. (:exclamation:Overlap/Lonely not yet implemented)
      1. `python PLOT.py` What is the 'd' feature?
   2. 

5. Upload file to SALTA online interface (github)

---

## Flowchart

Schematics of [how](https://docs.google.com/drawings/d/1u-_OJqQOnERBq5nKTgcgC5h74TIYdE5KG7-KlFpBDek/edit), the modules work together:

![salta-flow](https://docs.google.com/drawings/d/e/2PACX-1vQ6YH0G3eIGlIqlA_UasLVZIItqwbjav4mLcHy-yWROlnjK5y5GIFips0ILr52scMdeZJIRmCjuaTAA/pub?w=4184&h=10719)

---

### File structure

This [diagram](https://docs.google.com/drawings/d/1XH8ffvW79GotAoOFbCXrc6DADwYCszLQ9xLzEzUn4SQ/edit) shows the folder structure for the files produced during the process.

![tap-files](https://docs.google.com/drawings/d/e/2PACX-1vR3lDOY8zUI7nY0Vahhy_xumCK1TDGWru3QoA2fSZm4olGTVXjJKrSMV6YpNrrEMyBz5mHNjnGfmEZN/pub?w=1064&h=622)

---

## Other documents

Related documents can be found:

- [SALTA/installation](documentation/readme_install.md)

- [SALTA/ communicate across modules using OSC](documentation/readme_osc.md)

- [SALTA/ mediapipe](documentation/readme_mediapipe.md)

- [SALTA/ extract landmarks from video](documentation/readme_video2csv.md)

- [SALTA/motionbank](documentation/readme_motionbank.md)

- [SALTA/ annotations](documentation/readme_annotations.md)

---

### To-Do

[To-do list...](https://trello.com/b/eNrZMJnA/salta-segmentation-app)

---
