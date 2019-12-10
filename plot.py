
import matplotlib.pyplot as plt
import numpy as np
dic = {"price_log":0,
        "price_fund_log":1,
        "opt_num_log":2,
        "pes_num_log":3,
        "chart_index_log":4,
        "fund_num_log":5,
        "opinion_index":6}

with np.load("data/data_5000_s_t_65.npz") as data:
    fetch = [data[key] for key in data]
def llplot(price,lag,marker,bin_edges):

        price_log_1 = np.diff(np.log(price), n=lag)
        price_log_1 = np.absolute(1 / np.std(price_log_1) * price_log_1)
        counts, bin_edges = np.histogram(price_log_1,bins=1000)
        cdf = 1-np.cumsum(counts)/sum(counts)
        plt.loglog(bin_edges[1:], cdf, marker, markersize=3, label='Lag={}'.format(lag))

fig, ax = plt.subplots(1, 1)
price=fetch[dic["price_log"]]
price_fund=fetch[dic["price_fund_log"]]

price_fund_1 = np.diff(np.log(price_fund), n=1)
price_fund_1 = np.absolute(1 / np.std(price_fund_1) * price_fund_1)
counts, bin_edges = np.histogram(price_fund_1, bins=1000)
cdf = 1-np.cumsum(counts)/sum(counts)
plt.loglog(bin_edges[1:], cdf,  label='N(0,1)')
llplot(price,1,'+',bin_edges)
llplot(price,5,'^',bin_edges)
llplot(price,15,'*',bin_edges)
llplot(price,25,'1',bin_edges)

plt.legend(loc="upper right")
plt.xlim(left=1e-1,right=1e1)
plt.show()
print(np.std(np.diff(np.log(fetch[0]))))
print(np.std(np.diff(np.log(fetch[1]))))