import csv
import os
import pandas as pd
import matplotlib.pyplot as plt


class Engine:

    def __init__(self, info, data_frame, file_name) -> None:
        self.info = info
        self.data_frame = data_frame
        self.file_name = file_name


def getConstColNames(data) -> list:
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


def check_const_data_cols():
    global i
    const_cols = getConstColNames(engines[1].data_frame)
    print('constant columns')
    print(const_cols)
    print('\n')
    for i in range(1, len(engines)):
        this_cols = getConstColNames(engines[i].data_frame)
        if this_cols != const_cols:
            print('{0}: {1}'.format(i, list(set(const_cols) ^ set(this_cols))))


def check_const_info(name: str) -> bool:
    global engine
    info0 = set()
    for engine in engines:
        info0.add(engine.info[name])
    # print(info0)
    if len(info0) == 1:
        return True
    else:
        # print('{0}: {1}'.format(name, info0))
        return False


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

# remove constant columns
# 'Vessel Valve' is constant in some Data
# Engine 18 Data has cycle stops
for engine in engines:
    engine.data_frame = engine.data_frame.drop(columns=['Cycle Number', 'Active Countdown', 'Overload Alarm', 'System '
                                                                                                              'Alarm'])

# check which info fields are constant
var_info_names = []
for field in list(engines[0].info.keys()):
    if not check_const_info(field):
        var_info_names.append(field)
# info variable fields are 'Batch Number', 'Vessel Serial Number'


