# Troubleshooting

This document describes how to intall and troubleshoot the *Orbis* App. Click [here](README.md) to go to the main document.

* [Settings](#markdown-header-settings)

* [Troubleshooting *MediaPipe*](#markdown-header-troubleshooting-mediapipe)

* [Troubleshooting *Pafy*](#markdown-header-troubleshooting-pafy)

### Settings

The udp port `53534` is kinda fix, and refers to the computer (ip) where the script is running. The *ClientIP* is where the landmarks, reading, results... etc. are sent. One can change the ClienIP and port in `server_config.py`.

In order to run the application, go to the appropriate *.venv* and run:

```python
python index.py
```

Using a different terminal window, one can start/stop and configure different settings using the following commands (via OSC). All of them can be run using the following osc message syntax:

`sendosc [Client IPadress] [Client port] /Command [optional: i 1]`

### Troubleshooting *Mediapipe*

I encountered an error when attempting to install **mediapipe** that seems to have to do with my python version...

```python
# trying to instal mediapipe
pip install mediapipe

# error message
ERROR: Could not find a version that satisfies the requirement mediapipe (from versions: none)
ERROR: No matching distribution found for mediapipe
```

in order to find out my python version:

```python
python --version
```

*(my version shows to be Python 3.9.12)*

Trying to fix the issue using `virtualenv` instead of `venv`, which seems to allow me to set the python version to the accepted 3.7.0.

```python
# install virtualenv
virtualenv -p python3.7 mp_env

#create instance with specific python version
virtualenv -p python3.7 mp_env
source .mp_env/bin/activate
```

This environment is set to 3.7.0 version of python, yet the problem persists.

```python
# Another try to create an environment, this time with venv
python3.7 -m venv ./.venv37
source .venv37/bin/activate
```

I'll try installing MediaPipe fro MacOs first, according to these instructions:

[MediaPipe#installing-on-macos](https://google.github.io/mediapipe/getting_started/install.html#installing-on-macos)

```python
pip install -r requirements.txt
```

```python
python index.py
```





____

# To-Do

- Adapt to the Effects format
- have the csv pulled directly from Motion Bank (API)
- Frontend

# Contributors

Adrián Artacho, Leonhard Horstmeyer