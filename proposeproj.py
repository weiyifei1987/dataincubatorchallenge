# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:55:55 2016

@author: Yifei_Wei
"""
import pandas as pd
from pandas.io.data import DataReader
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# ---------------------------
# import stocks symbol
Location = r'C:\Users\weiyi\Downloads\constituents.csv'
df = pd.read_csv(Location)
index = range(100)
symbols_list = df['Symbol'].iloc[index]
d = {}
for ticker in symbols_list:
    d[ticker] = DataReader(ticker, "yahoo", '2013-12-01')
pan = pd.Panel(d)
df1 = pan.minor_xs('Adj Close') # only look at adj close
# ----------------------------
# Visualize raw data
df1.plot.line(figsize=(15,10))
# ----------------------------
# NMF
# Normalize data
norm_df = df1.div(df1.max()).fillna(0)
# drop nan data
norm_df = norm_df[norm_df.notnull()]

# ----------------------------------
# PCA
pca = PCA(n_components=2)
X_r = pca.fit(norm_df.values.transpose()).transform(norm_df.values.transpose())

plt.figure()
y_pred = KMeans(n_clusters=2, random_state=10).fit_predict(X_r)
plt.scatter(X_r[:, 0], X_r[:,1], marker='x', c = y_pred)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Cartesian coordinate PCA')

state_1 = filter(lambda x: x != 0, index*y_pred)
state_0 = filter(lambda x: x != 0, index*(~y_pred+2))
plt.figure()
norm_df[norm_df.columns[state_0]].plot.line(figsize=(15,10))
#plt.figure()
#norm_df[norm_df.columns[state_1]].plot.line(figsize=(15,10))
