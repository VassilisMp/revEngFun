# https://github.com/PySimpleGUI/PySimpleGUI
# https://pysimplegui.readthedocs.io/en/latest/
# https://github.com/nngogol/PySimpleGUIDesigner
import datetime
import re
from typing import Match
from engine import Engine

import PySimpleGUIQt as sg

layout = [[sg.Text('START', size=(8, 1)), sg.Input('00:00', key='_start_', size=(5, 1), enable_events=True)],
          [sg.Text('STOP', size=(8, 1)), sg.Input('00:00', key='_stop_', size=(5, 1), enable_events=True)],
          [sg.Text('Date', size=(8, 1)), sg.Input('01/01/2019', key='_date_', size=(10, 1), enable_events=True)],
          [sg.Text('Cycle ID', size=(8, 1)), sg.Input('1', key='_cycle_id_', size=(5, 1), enable_events=True)],
          [sg.Button('Submit', size=(8, 1), key='_submit_', enable_events=True), sg.Exit(size=(5, 1))]]

window = sg.Window('engine data', layout)
bgColor_default = window['_start_'].TextColor

time_regex = re.compile(r'^(0\d|1\d|2[0-3]):[0-5]\d$')
date_regex = re.compile(r'^(0\d|1\d|2\d|3[0-1])/(0\d|1[0-2])/(\d{4})$')
int_regex = re.compile(r'^\d+$')


def check_input(match: Match, element: str):
    if match is None:
        window[element].Update(background_color='#FF3333')
        window[element].BackgroundColor = '#FF3333'
    else:
        window[element].Update(background_color=bgColor_default)
        window[element].BackgroundColor = bgColor_default


def check_input_len(name, length):
    flag = True
    if len(values[name]) > length:
        window[name].Update(globals()[name + 'prev'])
        flag = False
    globals()[name + 'prev'] = values[name]
    return flag


_start_prev = '00:00'
_stop_prev = '00:00'
_date_prev = '01/01/2019'
_cycle_id_prev = '1'
while True:
    event, values = window.Read(timeout=10)
    # input check
    if event is '_start_':
        if not check_input_len(event, 5):
            continue
        match = time_regex.match(values['_start_'])
        check_input(match, '_start_')
    if event is '_stop_':
        if not check_input_len(event, 5):
            continue
        match = time_regex.match(values['_stop_'])
        check_input(match, '_stop_')
    if event is '_date_':
        if not check_input_len(event, 10):
            continue
        match = date_regex.match(values['_date_'])
        check_input(match, '_date_')
    if event is '_cycle_id_':
        if not check_input_len(event, 5):
            continue
        match = int_regex.match(values['_cycle_id_'])
        check_input(match, '_cycle_id_')
    # on submit click
    if event is '_submit_':
        error = ''
        if window['_start_'].BackgroundColor != bgColor_default:
            error += 'Wrong START input!\n'
        if window['_stop_'].BackgroundColor != bgColor_default:
            error += 'Wrong STOP input!\n'
        if window['_date_'].BackgroundColor != bgColor_default:
            error += 'Wrong date input!\n'
        if window['_cycle_id_'].BackgroundColor != bgColor_default:
            error += 'Wrong cycle id input!\n'
        if len(error) > 0:
            sg.PopupAutoClose(error)
        else:
            start: datetime.datetime = datetime.datetime.strptime(values['_date_'] + values['_start_'], "%d/%m/%Y%H:%M")
            stop: datetime.datetime = datetime.datetime.strptime(values['_date_'] + values['_stop_'], "%d/%m/%Y%H:%M")
            if (stop - start).total_seconds() // 60 <= 0:
                sg.PopupAutoClose('stop must be bigger than start')
            else:
                cycle_id: int = int(values['_cycle_id_'])
                myEngine: Engine = Engine(start, stop, cycle_id)
                sg.PopupAutoClose(myEngine)
                print(myEngine)

    if event in ('Exit', 'Window closed using X'):
        break

window.Close()
