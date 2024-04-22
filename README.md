# SALTA

This document describes the usage and troubleshooting of the *SALTA* App. 

---

## USAGE

1. Process the captured performance to extract features
   
   1. Landmarks from video
   
   2. Sound features
   
   3. IMU features

2. Prepare the data

3. Create the JSON exchange files (one per feature)
   
   1. Use [CompareSegments](https://bitbucket.org/smoothspaces/comparesegments) ([readme](comparesegments/README.md)) to create exchange JSONs.
      
      1. `python BATCH.py` (:exclamation:The feature names need to be written *ToGetHer*)
      
      2. (optional) normalize relative weights: `python feat_relnorm.py`

4. Generate the Probability Density Plots
   
   1. Use [PLOTLY](https://bitbucket.org/smoothspaces/plotly) ([readme](NOTATION//sandbox/plotly/README.md)) to generate PDPs. (:exclamation:Overlap/Lonely not yet implemented)
      1. `python PLOT.py`(:exclamation:What is the 'd' feature?
   2. 

5. Upload file to SALTA online interface (github)

---

## Flowchart

Schematics of how the modules work together:

![salta-flow](https://docs.google.com/drawings/d/e/2PACX-1vSSeaxl-8Dkjy0i_DYtegbYjZq4F4oL-teoOxTim0c4vMzLSerRn9PVWJHqMw458Vh1KaAfw_5Htdg6/pub?w=596&h=1024)

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
