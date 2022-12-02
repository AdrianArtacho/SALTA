# Mediapipe library

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

### Troubleshooting...

Errors related to the [pafy](https://pypi.org/project/pafy/) library.

```terminal
raise IOError(str(e).replace('YouTube said', 'Youtube says'))
OSError: ERROR: Unable to download API page: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1045)> (caused by URLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1045)')))
```

  other issue...

```terminal
self._likes = self._ydl_info['like_count']
KeyError: 'like_count'
```

The easiest fix is to go into `.venv/liv.python... /site-packages/pafy/backend_youtube_dl.py` and comment out this line

```
#self._dislikes = self._ydl_info['dislike_count']
```

What about this one?

```terminal
FileNotFoundError: [Errno 2] No such file or directory: 'data/csv/testAgainMaria.csv'
```

### How to find out my local python architecture (32/64 bits)

Go into python console by typin `python` in the terminal (inside /MediaPipe folder)

```python
#go into python console
python

# exectute commands to get python's architecture
import platform
platform.architecture()[0]


# leave the python console
exit()
```

____

# To-Do

- 