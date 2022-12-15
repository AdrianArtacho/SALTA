# Virtual Environment (VENV)

This document describes the process of setting up a virtual environment (inside a repo) to run the MediaPipe for python.

## Make a (repo)folder

- Create a repo in bitbucket

- clone to a local folder

- edit *.gitignore* to include everything in the hidden folder *.venv/*

```
# Exclude files from virtual environment
.venv/
```

Then you can launch the terminal in that folder and set up an instance.

## Setting up an instance

Using the [getting started](https://google.github.io/mediapipe/getting_started/python) instructions. Calling the virtual environment `venv` is a convention...

```python
# create a python instance
# createing it in a hidden folder is a convention for better version control.
# the folder ./.venv (I assume) will be included in .gitignore
python3 -m venv ./.venv
source .venv/bin/activate


# (leave an environment)
deactivate
```

you can check out where the local python and pip binaries live:

```python
which python
which pip

# in order to check the versions:
python --version
pip --version
```

Just for the fun of it, we may want to install a jupyter notebook:

```python
pip install jupyter


# numpy is already included in jupyter, otherwise:
pip install numpy


# launch Visual Studio Code using the command included in PATH
code .
```

Once in *Visual Studio Code*, create a new *Jupyter* notebook:

- New file (Jupyter)

- Set kernel to the python local installation: **.venv/ (Python 3.7.0)**

- Save with an appropriate name (inside the git folder)

- Test that everything is fine by running:

```python
test = 1

# hit the run icon on the left
# alternatively: Shift + Return
```

If everything seems fine, we can start working in the notebook :)

### Using the python interpreter:

```python
# Enter the python interpreter
python3

# (leave the interpreter)
>>> exit()
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

### Create a virtual environment with CONDA

1. Check conda is installed and in your PATH
   
   ```
   conda -V
   ```

2. Check conda is up to date
   
   ```
   conda update conda
   ```

3. Create env
   
   ```
    conda create python=3.7 -n Chen2020
   ```

4. .

____

### How to delete a virtual environment

##### In CONDA:

1. Step 1: Find the Conda environment to delete
   
   ```terminal
   conda env list
   ```

2. Step 2: Get out of the environment
   
   ```terminal
   conda deactivate
   ```

3. Step 3: Delete the Conda Environment
   
   ```python
   conda env remove -n corrupted_env
   # OR
   conda env remove -p /path/to/env
   ```

____

# To-Do

- 