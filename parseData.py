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


# List all files in a dataFolder using os.listdir
cur_path = os.getcwd()
basepath = cur_path + '/dataFolder/'
files = []
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        files.append(entry)

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
    settings: list = []
    index = -1
    for row in csv_reader:
        index = index + 1
        if len(row) == 0:
            break
        settings.append({row[0]: int(row[1])})
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

const_cols = getConstColNames(engines[0].data_frame)
print('constant columns')
print(const_cols)
print('\n')

for i in range(1, len(engines)):
    this_cols = getConstColNames(engines[i].data_frame)
    if this_cols != const_cols:
        print('{0}: {1}'.format(i, this_cols))
