
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
import scipy.stats
import scipy
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import norm
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
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'k+',markersize=3)
"""lag = 5"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=5)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=5)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'k^',markersize=3)

"""lag = 15"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=15)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=15)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'k*',markersize=3)


"""lag = 25"""
price_log_1=np.diff(np.log(fetch[dic["price_log"]]),n=25)
price_log_1=np.absolute(1/np.std(price_log_1)*price_log_1)

price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]),n=25)
price_fund_1=np.absolute(1/np.std(price_fund_1)*price_fund_1)

counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
cdf = np.cumsum(counts)
plt.loglog(bin_edges[1:], cdf/cdf[-1],'k1',markersize=3)


# price_log_=np.diff(np.log(fetch[dic["price_log"]]),n=5)
# price_log_1=np.absolute(np.std(price_log_1)*price_log_1)
#
# price_fund_1=np.diff(np.log(fetch[dic["price_fund_log"]]))
# price_fund_1=np.absolute(np.std(price_fund_1)*price_fund_1)
#
# counts, bin_edges = np.histogram(price_log_1,bins=sorted(price_fund_1))
# cdf = np.cumsum(counts)
# plt.loglog(bin_edges[1:], cdf/cdf[-1])


"""Pandas plot"""
# ser = pd.Series(price_fund_log)
# ser = ser.sort_values()
# ecdf=ECDF(price_log)
# ser_cdf = pd.Series(ecdf.y[1:], index=ser)
# (1-ser_cdf).plot(loglog=True, drawstyle='steps')
# plt.show()

# print(bin_edges)
#
# ser = pd.Series(price_fund_log)
# ser = ser.sort_values()
# # ecdf=ECDF(price_log)
# ser_cdf = pd.Series(cdf, index=ser[1:])
# # print(ser_cdf)
# # ser_cdf=ser_cdf[::-1]
# (1-ser_cdf).plot(loglog=True, drawstyle='steps')
# # plt.loglog(ser[1:],ser_cdf)
plt.show()

# cdf=np.cumsum(np.stack((price_log,price_fund_log)),0)[0]
# plt.plot(cdf)

# ser[len(ser)] = ser.iloc[-1]
# counts, bin_edges = np.histogram (price_log, normed=True)
# cdf = np.cumsum(price_log)

# fig,ax=plt.subplots(1,1)
# ax.invert_xaxis()
#


# input,output=zip(*sorted(zip(price_log,price_fund_log)))
# plt.plot(input,output)

# plt.figure(figsize=(20, 6))
# plt.plot(fetch[0][:1000],linewidth = '0.5',label='Price')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[1][:1000],linewidth = '0.5',label='Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[0][:1000],linewidth = '0.5',label='Price')
# plt.plot(fetch[1][:1000],linewidth = '0.5',label='Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[2][:1000],linewidth = '0.5',label='OPTIMIST')
# plt.plot(fetch[3][:1000],linewidth = '0.5',label="PESSIMIST")
# plt.plot(fetch[5][:1000],linewidth = '0.5',label="FUNDAMENTALIST")
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
#
# plt.figure(figsize=(20, 6))
# plt.plot(fetch[4][:1000],linewidth = '0.5',label='Chart Index')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
# plt.ylim(bottom=0)
#
# plt.figure(figsize=(20,6))
# plt.plot(fetch[6][:1000],linewidth = '0.5',label='Opinion Index')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
#
# plt.figure(figsize=(20,6))
# plt.plot(np.diff(np.log(fetch[0][:1000])),color='k',linewidth = '0.5',label='Log changes of price')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
# plt.ylim(bottom=-0.015,top=0.020)
#
#
# plt.figure(figsize=(20,6))
# plt.plot(np.diff(np.log(fetch[1][:1000])),color='k', linewidth = '0.5',label='Log changes of Fundamental value')
# plt.legend(loc="upper left")
# plt.xlim(0, 1000)
# plt.ylim(bottom=-0.015,top=0.020)
# #
# plt.show()

