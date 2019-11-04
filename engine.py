import tkinter as tk  # for python 3
import pygubu
import datetime


class Engine:
    def __init__(self, start: datetime.time, stop: datetime.time, cycle_id: int, date: datetime.date):
        self.start = start
        self.stop = stop
        self.cycle_id = cycle_id
        self.date = date


class Application:
    def __init__(this, master):
        # 1: Create a builder
        this.builder = pygubu.Builder()
        # 2: Load an ui file
        this.builder.add_from_file('engine.ui')
        # 3: Create the widget using a master as parent
        this.mainwindow = this.builder.get_object('mainwindow', master)
        # connect callback functions
        this.builder.connect_callbacks(this)
        this.START_Entry = None

    def get_START(this):
        this.START_Entry: tk.Entry = this.builder.get_object('START_Entry')
        print(type(this.START_Entry.get()))


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
