# OSC communication in python

In order to send/receive OSC data (according to this online documentation: [python-osc · PyPI](https://pypi.org/project/python-osc/)).

```python
pip install python-osc
```

If you want to run the server just execute:

```
python index.py
```

### Usage

The udp port ``53534`` is kinda fix, and refers to the computer (ip) where the script is running. The *ClientIP* is where the landm,arks, reading, results... etc. are sent. One can change the ClienIP and port in ``server_config.py``.

In order to run the application, go to the appropriate *.venv* and run:

```python
python index.py
```

Using a different terminal window, one can start/stop and configure different settings using the following commands (via OSC). All of them can be run using the following osc message syntax:

``sendosc [Client IPadress] [Client port] /Command [optional: i 1]``

#### Start Capture

Value *1* enables video on screen. Zero disables it.

`sendosc [Client IP] [Client PORT] /startCapture i [1/0]`

#### Change Client

`sendosc [Client IP] [Client PORT] /changeClient s [new IP] i [new PORT]`

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

## Saving Requirements

When adding a new package, freeze the requirements into the `requirements.txt` file:

```
pip freeze > requirements.txt
```

Then when loading the new packages run:

```
pip install -r requirements.txt
```

____

# To-Do

- 