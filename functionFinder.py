# https://thispointer.com/select-rows-columns-by-name-or-index-in-dataframe-using-loc-iloc-python-pandas/
import pandas as pd
import scipy.interpolate as interpolate
import numpy as np
import matplotlib.pyplot as plt


def plotPol(poly, x, y):
    xnew = np.arange(x.min() - 10, x.max() + 10, 0.5)
    ynew = poly(xnew)
    plt.plot(x, y, 'o', xnew, ynew, '-')
    plt.show()


# data = pd.read_csv("data.csv", sep=';', parse_dates=['Date'])
# read csv with deleted constant columns, except Date
data = pd.read_csv("data_del_const_cols.csv", sep=';', parse_dates={'date_col': ["Date", "Time"]})
# read csv again to convert hours:minutes column to minutes, and delete Date
data_mins = pd.read_csv("data_del_const_cols.csv", sep=';', parse_dates={'date_col': ["Date", "Time"]})
data_mins['date_col'] = data_mins['date_col'].apply(lambda x: x.time().hour * 60 + x.time().minute)

# dataList = list(data.T.to_dict().values())
# get only time and temperature columns
date_temp = data_mins[['date_col', 'Temperature']]
date_temp = list(date_temp.T.to_dict().values())
# delete duplicate elements
date_temp_no_duplicates = [i for n, i in enumerate(date_temp) if i not in date_temp[n + 1:]]
date_temp_no_duplicates = pd.DataFrame(date_temp_no_duplicates)

# date temperature
date_col = date_temp_no_duplicates['date_col'].to_list()
Temperature = date_temp_no_duplicates['Temperature'].to_list()

date_col = np.array(date_col)
Temperature = np.array(Temperature)

# date pressure
date_press = data_mins[['date_col', 'Pressure']]

time_col = date_press['date_col'].to_list()
pressure_col = date_press['Pressure'].to_list()
# get active area data
time_col = time_col[37:87]
pressure_col = pressure_col[37:87]
# start from zero time
time_col = [item - time_col[0] for item in time_col]

# convert to ndarray
x = np.array(time_col)
y = np.array(pressure_col)
print('pressure min value: ', y.min())
print('pressure max value: ', y.max())

poly = interpolate.PchipInterpolator(x, y)
plotPol(poly, x, y)
print(poly)


# BarycentricInterpolator(x, y)

# temp = date_temp_no_duplicates[0]['Temperature']
# newarray = [date_temp_no_duplicates[0]]
# for i in range(1, len(date_temp_no_duplicates) - 2):
#     if (date_temp_no_duplicates[i]['Temperature'] != temp) | \
#             (date_temp_no_duplicates[i]['Temperature'] != date_temp_no_duplicates[i + 1]['Temperature']):
#         newarray.append(date_temp_no_duplicates[i])
#         temp = date_temp_no_duplicates[i]['Temperature']
# newarray.append(date_temp_no_duplicates[len(date_temp_no_duplicates) - 1])
# newarray = pd.DataFrame(newarray)
# newarray.to_csv('removed_continued_values.csv')

# temp = date_temp[0]['date_col']
# newarray2 = [date_temp[0]]
# for i in range(1, len(date_temp) - 1):
#     if date_temp[i]['date_col'] != temp:
#         newarray2.append(date_temp[i])
#         temp = date_temp[i]['date_col']
# newarray2 = pd.DataFrame(newarray2)
# newarray2.to_csv('removed_continued_values_and_dupl_times.csv')

# date_col = newarray2['date_col'].to_list()
# Temperature = newarray2['Temperature'].to_list()
def apply(x):
    x = x.strip()
    if x == 'ON':
        return 100
    elif x == 'OFF':
        return 0


data = pd.read_csv("new_data1.csv", parse_dates={'Datetime': ["Date", "Time"]})
x1 = data['Datetime'][0].timestamp()
data['Datetime'] = data['Datetime'].map(lambda d: int(d.timestamp() - x1))
data['Active Countdown'] = data['Active Countdown'].map(lambda d: d * 100)
data['Countdown Step'] = data['Countdown Step'].map(lambda d: d / 100)
for i in range(6, 12):
    data.iloc[:, i] = data.iloc[:, i].map(apply)
data = data.drop(columns=['Cycle Number', 'Active Countdown', 'Vessel Valve', 'Overload Alarm', 'System Alarm'])

data.plot(x='Datetime')
plt.show()
