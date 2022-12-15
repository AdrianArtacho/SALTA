# /ORBIS/ (working name)

This document describes the usage and troubleshooting of the *Orbis* App. Other related documents are:

- [Setting up a virtual environment](documentation/readme_venv.md)

- [Communicating across modules using OSC](documentation/readme_osc.md)

- [Install and troubleshoot](documentation/readme_install.md)

## Extract landmarks from video

The easiest way to extract landmarks from a video hosted in the motion bank is
to run the script **video2csv.py**

```shell
python video2csv.py training parseannotations/csv/motionbank_test.csv examplebaa True True 3
```

Where the arguments are the following:

**arg #1** `training` is a specific process/function.

**arg #2** `data/csv/sourcefile.csv` (relative path)

**arg #3** `data/csv/outputfile.csv` (relative path)

**arg #4** `True` is a Boolean...

**arg #5** `True` is a Boolean...

**arg #6** `3` is an integer that defines the amount of...

### launch remotely

A legacy use of this feature can also be run from the terminal (via osc, therefore `index.py` should be running for this to work) using the following instruction:

```shell
sendosc [ip] [port] /startVideoCapture i 1 i 1 s [sourcefile.csv] s [outputfile.csv]
```

### Arguments

**arg0** `/startVideoCapture`command

**arg1** `i 1` integer: open display video window?

**arg2** `i 1` integer: save the obtained data in a db?

**arg3** `s data/csv/sourcefile.csv` string: relative path t the sourcefile.

**arg4** `s data/csv/outputfile.csv`
string: relative path to the sourcefile.

## Server Settings

The udp port `53534` is kinda fix, and refers to the computer (ip) where the script is running. The *ClientIP* is where the landmarks, reading, results... etc. are sent. One can change the ClienIP and port in `server_config.py`.

In order to run the application, go to the appropriate [*.venv*](documentation/readme_venv.md) and run **index.py**:

```python
source .venv/bin/activate
python index.py
```

Using a different terminal window, one can start/stop and configure different settings using the following commands (via OSC). All of them can be run using the following osc message syntax:

```shell
sendosc [Client IPadress] [Client port] /Command [optional: i 1]
```

## Usage for real-time MoCap

This module uses the Mediapipe library to capture the performer's body skeleton as landmarks. For instructions on how to intall and troubleshoot mediapipe, go to [readme_mediapipe.md](documentation/readme_mediapipe.md).

1. Go to repository's root folder

2. run `python index.py` (this will print the server's IP and PORT )

   *) You may ask the seerver to print client IP and port anytime by running:

   ```shell
   sendosc [IP] [PORT] /printClientInfo
   ```

3. Start/Stop video capture:

   *sendosc [ip] [port]* `/startVideoCapture i 1 i 1`

   *sendosc [ip] [port]*  `/stopVideoCapture`

4. Start/Stop server:

   *sendosc [ip] [port]*  `/startServer`

   *sendosc [ip] [port]*  `/stopServer`

### Start Capture

Value *1* enables video on screen. Zero disables it.

```shell
sendosc [Client IP] [Client PORT] /startCapture i [1/0]
```

#### Change Client

```shell
sendosc [Client IP] [Client PORT] /changeClient s [new IP] i [new PORT]
```

### Fit Model from Motion bank

In order to convert a video directly from the Scene in the Motion Bank (instructions on how to annotate and export [from the
motionbank](documentation/readme_motionbank.md))

```shell
sendosc [ip] [port] /startVideoCapture s [exported.csv] s [destination file]
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

### Gaussian mixture model (GMM)

MediaPipe in 'pose' mode yields 32 landmarks, each with three spatial values (96 values in total). The Gaussian mixture model  takes 3 points in time for each value (288 values in total).

## Credits

This software was developed in the context of the Artistic Research Project *Atlas of Smooth Spaces* by [Leonhard Horstmeyer](https://www.csh.ac.at/researcher/leonhard-horstmeyer/) and
[Adrián Artacho](http://www.artacho.at/).

---

## To-Do

- Adapt to the Effects format
- have the csv pulled directly from Motion Bank (API)

Frontend little contributions:

- browse and select file when python testLandMarks is run

- fromCache flag

- rename 'testAgainMaria.csv' into something neutral

Open issues:

- Is index.py still a thing? or is it obsolete?
