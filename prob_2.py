# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 12:18:06 2016

@author: Yifei Wei
"""
import numpy as np
import pandas as pd

# --------------------
# import csv data
Location = r'C:\Users\weiyi\Downloads\Calls_for_Service_'
years = ['2011', '2012', '2013', '2014', '2015']
df = pd.DataFrame()
for year in years:
    location = Location + year + '.csv'
    exec('df'+'_'+ year +' = pd.read_csv(location)')
    exec('df = df.append(df_'+year +',ignore_index=True)')

# -------------------------------
# Question 1: fraction of most frequent type
def Que_1(df):
    # Identify how many types
    all_types_counts = df['Type_'].value_counts()
    # visualize type and number
    all_types_counts.head()
    # calculate fraction
    fraction = all_types_counts[0].astype(np.float)/all_types_counts.sum()
    # Print fraction
    return fraction

# ---------------------------------
# Question 2: time from dispatch to arrival
def Que_2(df):
    df2 = df[np.all([df['TimeDispatch'].notnull(),df['TimeArrive'].notnull()], axis=0)]
    # Calculate time difference between TimeDispatch and TimeArrive
    # Convert to datetime
    TimeArrive = pd.to_datetime(df2['TimeArrive'])
    TimeDispatch = pd.to_datetime(df2['TimeDispatch'])
    # time difference
    median_time = (TimeArrive-TimeDispatch).median()
    return median_time

# ---------------------------------
# Question 3: Difference of largest and smallest average response time in each District
def Que_3(df):
    # clean data
    df3 = df[np.all([df['TimeDispatch'].notnull(),df['TimeCreate'].notnull()], axis=0)]
    # Convert to datetime
    Time_Create = pd.to_datetime(df3['TimeCreate'])
    Time_Dispatch = pd.to_datetime(df3['TimeDispatch'])
    # Calculate time diff
    time_diff = Time_Dispatch - Time_Create
    # see how many districts there are
    district = df3['PoliceDistrict'].unique()
    # creat an empty list to store average time response in each district
    avg = []
    for element in district:
        avg.append(time_diff[df3['PoliceDistrict']==element].mean())
    avg_df = pd.DataFrame(avg)
    # max - min
    return avg_df.max()-avg_df.min()

# -------------------------------
# Question 4 Surpring event
def Que_4(df):
    # clean data: remove district 0
    df4 = df[df['PoliceDistrict'] != 0]
    # calculate overall event 
    types_counts = df4['Type_'].value_counts()
    cond_prob_overall = types_counts.astype(np.float)/types_counts.sum()
    accept = types_counts >= 100 # accept events >= 100
    # district-wise cond_prob
    district = df4['PoliceDistrict'].unique()
    f = pd.DataFrame(index = pd.DataFrame(types_counts).index)
    for element in district:
       temp_counts = df4['Type_'][df4['PoliceDistrict']==element].value_counts()
       f[element] = temp_counts.astype(np.float)/temp_counts.sum()
    f = f.div(cond_prob_overall, axis = 0)
    f = f.fillna(0)[accept]
    return f.max().max()

# ----------------------------------
# difference of 2011 and 2015 regarding decrease of events
def Que_5(df_2011, df_2015):
    types_counts_diff = pd.DataFrame(df_2011['Type_'].value_counts().sub(df_2015['Type_'].value_counts()))
    f = pd.DataFrame(df_2011['Type_'].value_counts(),index = pd.DataFrame(types_counts_diff).index)
    fraction = types_counts_diff.div(f, axis = 0)
    return fraction.max()

# -----------------------------------
# disposition with respect to hour created    
def Ques_6(df):
    # clean data remove nan in created time
    df6 = df[df['TimeCreate'].notnull()]
    index_num = len(df6.index)
    Time_Create = pd.DatetimeIndex(df6['TimeCreate']).hour
    types_counts = df6['Disposition'].value_counts()
    f = pd.DataFrame(index = pd.DataFrame(types_counts).index)
    for element in pd.Series(Time_Create).unique():
        f[element] = df6['Disposition'][Time_Create==element].value_counts()
    
    number = 0
    for i in range(len(f.index)):
        temp = f.iloc[i].max()-f.iloc[i].min()
        if temp >= number:
            number = temp
    
    return number/index_num

# -------------------------------------
# area of a manner
#def Ques_7(df):
    # clean data
df7 = df[df['Location'].notnull()]
df7 = df7[df7['Location'].str[1] != '0']
district = df7['PoliceDistrict'].unique()
number = 0
for element in district:
    location = df7[df7['PoliceDistrict'] == element]['Location'].str[1:-3].str.split(', ').apply(pd.Series).astype(float)
    temp = location[0].std()*location[1].std()*np.pi
    if temp >= number:
        number = temp
    #return number
    
# --------------------------------------
# variation in priority
def Ques_8(df):
    number = 1
    for element in df['Type_'].unique():
        fraction = float(df['Priority'][df['Type_'] == element].value_counts().iloc[0])/df['Priority'][df['Type_'] == element].value_counts().sum()
        if fraction <= number:
            number = fraction
    return number
