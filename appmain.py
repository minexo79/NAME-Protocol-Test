import configparser
from src.serialttl import serial_init, serial_open, serial_close
from src.gui import gui_load, gui_updateGpsRawMsg, gui_updateGpsMsg

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    port = config['DEFAULT']['PORT']
    baud = config['DEFAULT']['BAUD']

    serial_init(gui_updateGpsRawMsg, gui_updateGpsMsg)
    serial_open(port, int(baud))
    if(gui_load(port, int(baud)) == True):         # wait until gui closed
        serial_close()
        exit(0)