import datetime

import PySimpleGUI as sg
import engine

layout = [[sg.Text('START'), sg.Input()],
          [sg.Text('STOP'), sg.Input()],
          [sg.Text('Date'), sg.Input()],
          [sg.Text('Cycle ID'), sg.Input()],
          [sg.T('Source Folder')],
          [sg.In()],
          [sg.FolderBrowse(target=(-1, 0)), sg.OK()],
          [sg.Button('Submit'), sg.Exit()]]

window = sg.Window('Window that stays open', layout)


event, values = window.Read()
print(event, values)

# start: datetime.time = datetime.datetime.strptime(values[0], "%H:%M").time()
# stop: datetime.time = datetime.datetime.strptime(values[1], "%H:%M").time()
# date: datetime.date = datetime.datetime.strptime(values[2], "%d/%m/%Y").date()
cycle_id: int = int(values[3])
print(cycle_id)
startInput: sg.InputText = layout[0][0]
# startInput.BackgroundColor

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    print(event, values)

window.Close()
