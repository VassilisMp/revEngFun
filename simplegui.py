# https://github.com/PySimpleGUI/PySimpleGUI
# https://pysimplegui.readthedocs.io/en/latest/
# https://github.com/nngogol/PySimpleGUIDesigner
import datetime
import re
from typing import Match

import PySimpleGUI as sg
import engine

layout = [[sg.Text('START', size=(8, 1)), sg.Input('00:00', key='_start_', size=(5, 1), enable_events=True)],
          [sg.Text('STOP', size=(8, 1)), sg.Input('00:00', key='_stop_', size=(5, 1))],
          [sg.Text('Date', size=(8, 1)), sg.Input('01/01/2019', key='_date_', size=(10, 1))],
          [sg.Text('Cycle ID', size=(8, 1)), sg.Input('1', key='_cycle_id_', size=(5, 1))],
          [sg.Button('Submit', size=(8, 1)), sg.Exit(size=(5, 1))]]

window = sg.Window('engine data', layout)

# layout[0][1].BackgroundColor = '#FF6666'
# validate start, stop
# match: Match = re.compile(r'\d\d:\d\d$').match(startInput)
# valid = False
# if match is not None:
#     startInput.BackgroundColor = '#ffffff'
#     print('match')
#     valid = True
# else:
#     startInput.BackgroundColor = '#ff0000'
#     print('no match')
#     valid = False
# messagebox = tk.Tk()
# w = tk.Message(messagebox, text="this is a message")
# w.pack()
# start_time = datetime.datetime.strptime(start_time_string, "%H:%M").time()
# start_entry.setvar('time', )

# start: datetime.time = datetime.datetime.strptime(values[0], "%H:%M").time()
# stop: datetime.time = datetime.datetime.strptime(values[1], "%H:%M").time()
# date: datetime.date = datetime.datetime.strptime(values[2], "%d/%m/%Y").date()
# cycle_id: int = int(values[3])

time_regex = re.compile(r'\d\d:\d\d$')
startInput = window['_start_']
while True:
    event, values = window.Read()
    # print(window['_start_'])
    # print(values)
    if event is '_start_':
        print(startInput.BackgroundColor)
        startInput.BackgroundColor = '#FF0000'
        match = time_regex.match(values['_start_'])
        # if match is None:
        #     window['_start_'].BackgroundColor = '#FF0000'
        # else:
        #     window['_start_'].BackgroundColor = '#FFFFFF'
        # try:
        #     start: datetime.time = datetime.datetime.strptime(values[0], "%H:%M").time()
        # except ValueError or KeyError:
        #     window['_start_'].BackgroundColor = '#FF0000'
    if event in (None, 'Exit', 'Window closed using X'):
        break
    # print(event, values)
    # print(values['_start_'])

window.Close()
