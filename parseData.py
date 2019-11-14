import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import RangeIndex


class Engine:

    def __init__(self, info, data_frame, file_name) -> None:
        self.info: dict = info
        self.data_frame: pd.DataFrame = data_frame
        self.file_name: str = file_name
        from pandas._libs.tslibs.timedeltas import Timedelta
        self.duration: Timedelta = data_frame['Datetime'][data_frame.__len__() - 1] - data_frame['Datetime'][0]

        # self.data_frame['Countdown Step'] = self.data_frame['Countdown Step'] / 10

        # TODO should apply only to columns with ON/OFF values
        def apply(x):
            if type(x) == str:
                xstrip = x.strip()
                if xstrip == 'ON':
                    return 100
                elif xstrip == 'OFF':
                    return 0
                else:
                    return x
            else:
                return x

        self.data_frame = self.data_frame.applymap(lambda x: apply(x))
        self.active_data = None


class Engines:
    # a = np.full((18,), 2)
    def __init__(self, engines) -> None:
        super().__init__()
        self.engines = engines
        # remove constant columns
        # 'Vessel Valve' is constant in some Data
        # Engine 18 Data has cycle stops
        for i in range(0, len(self.engines)):
            print('Engines: ', i, ' of: ', len(self.engines))
            self.engines[i].data_frame = self.engines[i].data_frame.drop(
                columns=['Cycle Number', 'Active Countdown', 'Overload Alarm', 'System Alarm'])
            self.engines[i].active_data = self.get_active_area_data(self.engines[i]).reset_index(drop=True)
            # engine.data_frame['Countdown Step'] = engine.data_frame['Countdown Step'] / 10
        self.array = np.array([self.engines[0].active_data[::60].Pressure.to_list()])
        for i in range(1, len(self.engines)):
            l = np.array([self.engines[i].active_data[::60].Pressure.to_list()])
            # a = np.array([self.engines[1].active_data[::60].Pressure.to_list()])
            self.array = np.append(self.array, l, axis=0)
        # Temperature range
        self.max_temp = max(map(lambda x: max(x.data_frame.Temperature), self.engines))
        self.min_temp = min(map(lambda x: min(x.data_frame.Temperature), self.engines))
        # Pressure range
        self.max_pressure = max(map(lambda x: max(x.data_frame.Pressure), self.engines))
        self.min_pressure = min(map(lambda x: min(x.data_frame.Pressure), self.engines))
        # Countdown Step range
        self.max_CountdownStep = max(map(lambda x: max(x.data_frame['Countdown Step']), self.engines))
        self.min_CountdownStep = min(map(lambda x: min(x.data_frame['Countdown Step']), self.engines))
        # duration range
        self.max_duration = max(map(lambda x: x.duration, self.engines))
        self.min_duration = min(map(lambda x: x.duration, self.engines))

    def get_active_area_data(self, engine: Engine) -> pd.DataFrame:
        # check running time
        start_date_i = None
        stop_date_i = None
        start_flag = True
        for index, row in engine.data_frame.iterrows():
            if row['Countdown Step'] == 0:
                stop_date_i = index
                break
        for index, row in reversed(list(engine.data_frame.iterrows())):
            if row['Countdown Step'] == 1800:
                start_date_i = index + 1
                break
        # active area
        active = engine.data_frame[start_date_i - 1:stop_date_i + 1][
            ['Datetime', 'Pressure', 'Countdown Step']]
        active = active.reset_index(drop=True)
        # start
        delta = active.T[1].Datetime - active.T[0].Datetime
        active.at[0, 'Countdown Step'] = active.T[1]['Countdown Step'] + delta.total_seconds()
        # stop
        delta = active.T[active.__len__() - 1].Datetime - active.T[active.__len__() - 2].Datetime
        active.at[active.__len__() - 1, 'Countdown Step'] = active.T[active.__len__() - 2][
                                                                'Countdown Step'] - delta.total_seconds()
        # make dataframe with 1 second step
        df = pd.DataFrame({'Countdown Step': reversed(range(active['Countdown Step'][active.__len__() - 1],
                                                            active['Countdown Step'][0] + 1, 1))})
        merged = pd.merge(active, df, right_on='Countdown Step', left_on='Countdown Step', how='right')
        merged = merged.sort_values(by=['Countdown Step'], ascending=False)
        # interpolate nulls
        merged = merged.interpolate(method='linear')
        # reset index from zero
        merged = merged.reset_index(drop=True)
        start = merged.index[merged['Countdown Step'] == 1800].values[0]
        stop = merged.index[merged['Countdown Step'] == 0].values[0]
        merged = merged[start:stop + 1][['Pressure', 'Countdown Step']]
        return merged

    def check_const_info(self, name: str) -> bool:
        info0 = set()
        for engine in engines:
            info0.add(engine.info[name])
        # print(info0)
        if len(info0) == 1:
            return True
        else:
            # print('{0}: {1}'.format(name, info0))
            return False
    # check which info fields are constant
    # var_info_names = []
    # for field in list(engines[0].info.keys()):
    #     if not check_const_info(field):
    #         var_info_names.append(field)
    # info variable fields are 'Batch Number', 'Vessel Serial Number'

    def getConstColNames(self, data) -> list:
        const_cols = []
        for colName in data.columns:
            col = data[colName]
            # check for duplicates
            object0 = str(col[0]).strip()
            equals = True
            for item in col:
                if str(item).strip() != object0:
                    equals = False
                    break
            if equals:
                const_cols.append(colName)
        return const_cols

    def check_const_data_cols(self):
        global i
        const_cols = self.getConstColNames(engines[1].data_frame)
        print('constant columns')
        print(const_cols)
        print('\n')
        for i in range(1, len(engines)):
            this_cols = self.getConstColNames(engines[i].data_frame)
            if this_cols != const_cols:
                print('{0}: {1}'.format(i, list(set(const_cols) ^ set(this_cols))))


# List all files in a dataFolder using os.listdir
cur_path = os.getcwd()
basepath = cur_path + '/dataFolder/'
files = []
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        files.append(entry)

# get engines
engines: list = []
for fileName in files:
    if fileName == 'VESSEL_9004_BATCH_1850.csv':
        continue
    # read file lines
    with open(basepath + fileName, 'r') as file:
        lines = file.readlines()
    # replace /t in lines
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace('\t', '')
    csv_reader = csv.reader(lines, delimiter=',')
    # get settings in list of dicts
    settings: dict = {}
    index = -1
    for row in csv_reader:
        index = index + 1
        if len(row) == 0:
            break
        settings.update({row[0].strip(): int(row[1])})
    # move to next row, because this is empty
    csv_reader.__next__()
    # save data in csv to use parse dates with pandas
    with open('tmp', 'w') as tmp:
        tmp.writelines(lines[index + 2:])
    # read csv
    data = pd.read_csv('tmp', parse_dates={'Datetime': ["Date", "Time"]})
    # append Engine object
    engines.append(Engine(settings, data, fileName))
# remove tmp file
os.remove('tmp')

# find constant columns
# check_const_data_cols()

enginesClass = Engines(engines)

# active.T[0].Datetime-pd.Timedelta(seconds=1800-1739)

# for engine in enginesClass.engines:
#     engine.active_data.reset_index().plot(x='index', y='Pressure')
#     plt.show()


# https://datascience.stackexchange.com/questions/5427/how-to-generate-synthetic-dataset-using-machine-learning-model-learnt-with-origi
# https://en.wikipedia.org/wiki/Anscombe%27s_quartet
# https://en.wikipedia.org/wiki/Nonparametric_statistics
# https://www.encyclopediaofmath.org/index.php/Multi-dimensional_statistical_analysis
