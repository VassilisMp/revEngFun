import pandas as pd

# data = pd.read_csv("data.csv", sep=';', parse_dates=['Date'])
data = pd.read_csv("data_del_const_cols.csv", sep=';', parse_dates={'date_col': ["Date", "Time"]})
data_time_only = pd.read_csv("data_del_const_cols.csv", sep=';', parse_dates={'date_col': ["Date", "Time"]})
data_time_only['date_col'] = data_time_only['date_col'].apply(lambda x: x.time().hour * 60 + x.time().minute)

dataList = list(data_time_only.T.to_dict().values())
data_step_5 = []
for i in range(0, len(dataList)-1, 5):
    data_step_5.append(dataList[i])
# dataList = list(data.T.to_dict().values())

# df1 = df[['a','b']]
