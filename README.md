# NAME Protocol Test
Test NAME Message Decode Result With pynmea2 package with log.

## Required
- Python 3.8 or Later
- [Pyserial](https://pypi.org/project/pyserial/)
- [Pynmea2](https://pypi.org/project/pynmea2/)

# Using 
```
python ./appmain.py
```

# Config File
```ini
[DEFAULT]
PORT=/dev/ttyUSB0   # Port Name, In Windows Change To COMXX.
BAUD=9600           # baudrate, default is 9600 bps
```