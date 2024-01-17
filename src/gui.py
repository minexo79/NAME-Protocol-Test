import PySimpleGUI as sg
import os
import platform
import subprocess

sg.theme('Topanga')

layout_l = [[sg.Text('Gps Raw Message ($GPGGA):', size=(40,1))],
            [sg.Multiline(size=(40,20), key='txtGpsRawMsg')]]

layout_r = [[sg.Text('Gps Message:', size=(40,1))],
            [sg.Multiline(size=(40,20), key='txtGpsMsg')]]

layout = [[sg.Text("Port："), sg.Text(key='txtPort', size=(10,1)), sg.Text("Baud："), sg.Text(key='txtBaud', size=(10,1))],
          [sg.Col(layout_l), sg.Col(layout_r)],
          [sg.Button('Open Log'), sg.Button('Exit', button_color=('white', 'firebrick3'))]]

def gui_load(_port: str, _baud: str) -> bool:
    global window 
    window = sg.Window('NMEA Test / Blackcat 2024.1.18', layout, location=(100, 100), finalize=True)
    window['txtPort'].update(_port)
    window['txtBaud'].update(_baud)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Open Log':
            if platform.system() == "Windows":
                os.startfile("log/")
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "log/"])
            else:
                subprocess.Popen(["xdg-open", "log/"])
            pass

    gui_close()
    return True

def gui_updateGpsRawMsg(rawmsg: str):
    global window 
    if (window == None):
        return
    
    try:
        _msg = window['txtGpsRawMsg']
        _msg.update(rawmsg + _msg.get())
    except Exception:
        pass

def gui_updateGpsMsg(msg: str):
    global window 
    try:
        _msg = window['txtGpsMsg']
        _msg.update(msg + '\n' + _msg.get())
    except Exception:
        pass

def gui_close():
    global window 
    window.close()