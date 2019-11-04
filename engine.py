import re
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from typing import Match

import pygubu
import datetime


class Engine:
    def __init__(self, start: datetime.time, stop: datetime.time, cycle_id: int, date: datetime.date):
        self.start = start
        self.stop = stop
        self.cycle_id = cycle_id
        self.date = date
        # self.stop = time_object = datetime.datetime.strptime(time_string, "%H:%M").time()


class Application:
    def __init__(self, master):
        self.master = master
        # 1: Create a builder
        self.builder = pygubu.Builder()
        # 2: Load an ui file
        self.builder.add_from_file('engine.ui')
        # 3: Create the widget using a master as parent
        self.mainwindow: tk.Tk = self.builder.get_object('mainwindow', master)
        # connect callback functions
        self.builder.connect_callbacks(self)
        # set engine
        self.engine: Engine = None
        # button style
        s: Style = ttk.Style()
        s.configure('MyEntryStyle.TEntry', foreground="black", background="white", font="black")
        # this.START_Entry = None

    def submit(self):
        start_entry: tk.Entry = self.builder.get_object('start_Entry')
        submit_Button: tk.Button = self.builder.get_object('submit_Button')

        # start_time_string = start_entry.getvar('time')

    def validate_time(self):
        print('\nvalidate')
        time_var: tk.StringVar = self.builder.tkvariables['time_var']
        match: Match = re.compile(r'\d\d:\d\d$').match(time_var.get())
        print(time_var.get())
        # print(match)
        print(type(match))
        valid = False
        if match is not None:
            print('match')
            valid = True
        else:
            self.builder.get_object('start_Entry').config({"background": "Red"})
            print('no match')
            valid = False
            # messagebox = tk.Tk()
            # w = tk.Message(messagebox, text="this is a message")
            # w.pack()
        return valid
        # start_time = datetime.datetime.strptime(start_time_string, "%H:%M").time()
        # start_entry.setvar('time', )


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
