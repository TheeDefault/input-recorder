# Mouse Input Recorder

A small Windows desktop utility that displays recent keyboard and mouse input.
Recording starts when you press `Ctrl+R`; events are shown in the console and
the on-screen window. Press `Ctrl+C` in the console to stop the program.

## Setup

Use Python 3 and install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python pos.py
```

The program records key presses and mouse clicks only after recording has
started. Input events are displayed locally and are not written to a file.
