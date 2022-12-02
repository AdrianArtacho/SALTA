# /ORBIS/ (working name)

This document describes the usage and troubleshooting of the *Orbis* App. Other related documents are:

- [Setting up a virtual environment](readme_venv.md)
* [Communicating across modules using OSC](readme_osc.md) 

* [Install and troubleshoot](readme_install.md)

### Settings

The udp port `53534` is kinda fix, and refers to the computer (ip) where the script is running. The *ClientIP* is where the landmarks, reading, results... etc. are sent. One can change the ClienIP and port in `server_config.py`.

In order to run the application, go to the appropriate *.venv* and run **index.py**:

```python
source .venv/bin/activate
python index.py
```

Using a different terminal window, one can start/stop and configure different settings using the following commands (via OSC). All of them can be run using the following osc message syntax:

`sendosc [Client IPadress] [Client port] /Command [optional: i 1]`

## Usage for real-time MoCap

This module uses the Mediapipe library to capture the performer's body skeleton as landmarks. For instructions on how to intall and troubleshoot mediapipe, go to [readme_mediapipe.md](readme_mediapipe.md).

1. Go to repository's root folder

2. run `python index.py` (this will print the server's IP and PORT )
   
   *) You may ask the seerver to print client IP and port anytime by running:
   
   `sendosc [IP] [PORT] /printClientInfo`

3. Start/Stop video capture:
   
   *sendosc [ip] [port]* `/startVideoCapture i 1 i 1`
   
   *sendosc [ip] [port]*  `/stopVideoCapture`

4. Start/Stop server:
   
   *sendosc [ip] [port]*  `/startServer`
   
   *sendosc [ip] [port]*  `/stopServer`

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

### Gaussian mixture model (gmm)

MediaPipe in 'pose' mode yields 32 landmarks, each with three spatial values (96 values in total). The Gaussian mixture model  takes 3 points in time for each value (288 values in total). 

---

# To-Do

- Adapt to the Effects format
- have the csv pulled directly from Motion Bank (API)

Frontend little contributions:

- browse and select file when python testLandMarks is run

- fromCache flag

- rename 'testAgainMaria.csv' into something neutral

# Authors

[Leonhard Horstmeyer](https://www.csh.ac.at/researcher/leonhard-horstmeyer/),
[Adrián Artacho](http://www.artacho.at/)