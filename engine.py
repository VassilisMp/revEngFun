import datetime


class Engine:
    def __init__(self, start: datetime.datetime, stop: datetime.datetime, cycle_id: int):
        self.start = start
        self.stop = stop
        self.cycle_id = cycle_id
        self.date: datetime.date = start.date()
        self.total_duration: int = int((self.stop - self.start).total_seconds()) // 60
        x1plusx2 = self.total_duration - 30 - 5
        self.x1: int = int(x1plusx2 * 0.8)
        self.x2: int = int(x1plusx2 * 0.2)

    def y(self):
        return (self.stop - self.start).total_seconds() // 60

    def __str__(self) -> str:
        return 'start: {0}\nstop: {1}\ndate: {2}\ncycle id: {3}\ntotal duration: {4}\nx1: {5}\nx2: {6}'.format(self.start.time().__str__(),
                                                                        self.stop.time().__str__(),
                                                                        self.date.__str__(),
                                                                        self.cycle_id,
                                                                        self.total_duration,
                                                                        self.x1,
                                                                        self.x2)
