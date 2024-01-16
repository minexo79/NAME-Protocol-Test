import serial 
import pynmea2
import time
import logging
import configparser
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
                
        msg = pynmea2.parse(line)
        # TODO: Add No GPS Message And Times Count
        logging.info(f"Found GPS Packet: {msg.timestamp} {msg.lat_dir}{round(msg.latitude, 6)}, {msg.lon_dir}{round(msg.longitude, 6)}")
        line = ""               # clear before line to keep new message can comes in.
        lock.release()

if __name__ == "__main__":  
    config = configparser.ConfigParser()
    config.read('config.ini')

    _port = config['DEFAULT']['PORT']
    _baud = config['DEFAULT']['BAUD']

    logging.basicConfig(filename='log/gpslog.log', format='%(asctime)s [%(levelname)s] > %(message)s', level=logging.DEBUG)
    try:
        ser = serial.Serial(_port, int(_baud))
        if (ser.is_open):
            logging.info("=== GPS Logging Start! ===")
            th1 = Thread(target = read_gps_module_string)
            th2 = Thread(target = parse_gps_message)
            th1.start()
            th2.start()
    except KeyboardInterrupt or Exception:
        is_running = False
        logging.info("=== GPS Logging End! ===")
        th1.join()
        th2.join()
        ser.close()