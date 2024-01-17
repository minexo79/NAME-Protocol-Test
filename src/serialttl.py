import serial 
import pynmea2
import time
import logging
from datetime import datetime
from threading import Thread, Lock

ser = None
line = ""
lock = Lock()
is_running = True

def read_gps_module_string():
    '''
    Keep Reading GPS Module Buffer And Get String That Begin With $GPGGA.
    @param None
    @return None
    '''
    global line, is_running
    while is_running:
        time.sleep(0.01)        # avoid read too fast
        if (ser.readable()):
            _line = ser.readline().decode("ascii")
            if (_line.startswith("$GPGGA")):
                line = _line
                updateGpsRawMsg(line)
                # print(line)
        

def parse_gps_message():
    '''
    Decoding GPS Raw Message Using pynmea2.
    @param None
    @return None
    '''
    global line, is_running
    while is_running:
        time.sleep(0.1)         # avoid read too fast
        
        lock.acquire()
        if (line == ""):
            lock.release()
            continue

        if (line[line.find(',') + 1] == ','):                   # check if gps signal is received. (use ',' location to check)
            logging.warning(f"Cannot Receive GPS Signal Yet!")
            line = ""
            lock.release()
            continue

        msg = pynmea2.parse(line)
        # TODO: Add No GPS Message And Times Count

        _timestamp = msg.timestamp.strftime("%H:%M:%S")
        updateGpsMsg(f"{_timestamp} >> {msg.lat_dir}{round(msg.latitude, 6)}, {msg.lon_dir}{round(msg.longitude, 6)}")
        if (round(msg.latitude, 6) == 0.0 and round(msg.longitude, 6) == 0.0):
            logging.info(f"Cannot Receive GPS Signal Yet: {_timestamp}")
        else:
            logging.info(f"Receive GPS Signal: {_timestamp} {msg.lat_dir}{round(msg.latitude, 6)}, {msg.lon_dir}{round(msg.longitude, 6)}")
        line = ""               # clear before line to keep new message can comes in.
        lock.release()

def serial_init(_update_raw_msg, _update_msg):
    '''
    Init Serial Port And Set Callback Function.
    @param update_raw_msg: callback function for update raw message.
    @param update_msg: callback function for update message.
    @return None
    '''
    global updateGpsRawMsg, updateGpsMsg
    updateGpsRawMsg = _update_raw_msg
    updateGpsMsg    = _update_msg

def serial_open(port: str, baud: int):
    global ser, th1, th2
    _port = port
    _baud = baud

    logging.basicConfig(filename=f'log/{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', format='%(asctime)s [%(levelname)s] > %(message)s', level=logging.DEBUG)
    ser = serial.Serial(_port, int(_baud))
    if (ser.is_open):
        logging.info("=== GPS Logging Start! ===")
        th1 = Thread(target = read_gps_module_string)
        th2 = Thread(target = parse_gps_message)
        th1.start()
        th2.start()

def serial_close():
    global is_running
    is_running = False
    logging.info("=== GPS Logging End! ===")
    th1.join()
    th2.join()
    ser.close()