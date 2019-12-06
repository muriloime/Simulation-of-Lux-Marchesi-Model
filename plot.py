
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
import scipy.stats
import scipy
from statsmodels.distributions.empirical_distribution import ECDF
import scipy
dic = {"price_log":0,
        "price_fund_log":1,
        "opt_num_log":2,
        "pes_num_log":3,
        "chart_index_log":4,
        "fund_num_log":5,
        "opinion_index":6}

with np.load("data_5000_times.npz") as data:
    fetch = [data[key] for key in data]

'''Lag=1'''
fig,ax=plt.subplots(1,1)
ax.invert_xaxis()

price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=1)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=1)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
counts=1-counts/sum(counts)
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'+',markersize=3,label='Lag=1')
plt.legend(loc="upper right")


#
"""lag = 5"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=5)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=5)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
counts=1-counts/sum(counts)
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'^',markersize=3,label='Lag=5')
plt.legend(loc="upper right")

"""lag = 15"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=15)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=15)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
counts=1-counts/sum(counts)
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'*',markersize=3,label='Lag=15')
plt.legend(loc="upper right")


"""lag = 25"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=25)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=25)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
counts=1-counts/sum(counts)
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'1',markersize=3,label='Lag=25')
plt.legend(loc="upper right")
""""""




# plt.figure(figsize=(20, 6))
# plt.plot(fetch[0],linewidth = '0.5',label='Price')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[1],linewidth = '0.5',label='Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[0],linewidth = '0.5',label='Price')
# plt.plot(fetch[1],linewidth = '0.5',label='Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[2],linewidth = '0.5',label='OPTIMIST')
# plt.plot(fetch[3],linewidth = '0.5',label="PESSIMIST")
# plt.plot(fetch[5],linewidth = '0.5',label="FUNDAMENTALIST")
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[4],linewidth = '0.5',label='Chart Index')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
# plt.ylim(bottom=0)
#
# plt.figure(figsize=(20,6))
# plt.plot(fetch[6],linewidth = '0.5',label='Opinion Index')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
#
# plt.figure(figsize=(20,6))
# plt.plot(np.diff(np.log(fetch[0])),color='k',linewidth = '0.5',label='Log changes of price')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
# plt.ylim(bottom=-0.035,top=0.035)
#
#
# plt.figure(figsize=(20,6))
# plt.plot(np.diff(np.log(fetch[1])),color='k', linewidth = '0.5',label='Log changes of Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 5000)
# plt.ylim(bottom=-0.035,top=0.035)
# #
plt.show()
# print(np.std(np.diff(np.log(fetch[0]))))
# print(np.std(np.diff(np.log(fetch[1]))))