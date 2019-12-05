import argparse
import math
from collections import deque
from agents import *
from price import *
import random
from util import *
import matplotlib.pyplot as plt
import numpy as np
random.seed(324)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obs", type=int, default=5000, help='Observation times')
    parser.add_argument("--N", type=float, default=500.0, help='Determine the number of the agents')
    parser.add_argument("--v_1", type=float, default=2.0, help='Frequency of reval (Between noise trader)')
    parser.add_argument("--alpha_1", type=float, default=0.6, help='Importance of flows.')
    parser.add_argument("--alpha_2", type=float, default=1.5, help='Importance of the chart')
    parser.add_argument("--v_2", type=float, default=0.6, help='Frequency of reval (Between noise and fundamentalists)')
    parser.add_argument("--alpha_3", type=float, default=1, help='Sensitivity to profit differential')
    parser.add_argument("--R", type=float, default=0.0004, help='Average return receive by the holder of other asset')
    parser.add_argument("--s", type=float, default=0.75, help='Discount of profit of the fundamentalists')
    parser.add_argument("--t_c", type=float, default=0.001, help='Average trading volume per transaction')
    parser.add_argument("--gamma", type=float, default=0.01, help='Strengh of reaction')
    parser.add_argument("--beta", type=float, default=4, help='Parameter for the price adjustment speed')
    parser.add_argument("--std", type=float, default=0.005, help='Log return of the fundamental price obey N(0,std)')
    parser.add_argument("--price", type=float, default=10.0, help='Initial price')
    parser.add_argument("--price_fund", type=float, default=10.0, help='Initial fundamental price')
    parser.add_argument("--t_inc", type=float, default=0.002, help='Time increment')
    parser.add_argument("--t_inc_price", type=float, default=0.2,
                        help='Time interval for calculation of price updating')
    args = parser.parse_args()
    """Constant Parameters setting"""
    N = args.N
    v_1 = args.v_1
    alpha_1 = args.alpha_1
    alpha_2 = args.alpha_2
    v_2 = args.v_2
    alpha_3 = args.alpha_3
    R = args.R
    s = args.s
    t_c = args.t_c
    gamma = args.gamma
    beta = args.beta
    std = args.std
    t_inc_price = args.t_inc_price
    t_inc = args.t_inc
    set_constant(args) # for util programm

    """Agent initialization"""
    Agents_list=[]
    agents_min = N * 0.008

    for i in range(int(agents_min)):
        Agents_list.append(Agents("OPTIMIST"))
        Agents().add_opt()
    for i in range(int(agents_min)):
        Agents_list.append(Agents("PESSIMIST"))
        Agents().add_pes()
    for i in range(int(N-2*agents_min)):
        Agents_list.append(Agents("FUNDAMENTALIST"))
        Agents().add_fund()
    opt_num_log=np.array([agents_min])
    pes_num_log=np.array([agents_min])
    fund_num_log=np.array([N-2*agents_min])
    chart_index_log=np.array([agents_min*2/N])
    opinion_index=np.array([Agents().get_flow_noise()])


    """Variable Parameters"""
    price = args.price
    price_fund = args.price_fund

    """To store the price history for calculating the avg of interval of 0.2"""
    price_queue = deque([0 for i in range(int(t_inc_price / t_inc))])
    price_dot = 0 # Initialized as zero, calculate by (price-deque.popleft())/t_inc_price
    price_elem=Price(price,price_fund,price_dot,price_queue,t_inc_price)
    price_log=np.array([price])
    price_fund_log=np.array([price_fund])
    """Price, stock share and cash initialization"""
    noise_share = 0
    fund_share = 0
    noise_cash = 0
    fund_cash = 0

    Observation_times=args.obs
    steps=int(1/t_inc)
    for obs in range(Observation_times):
        for step in range(steps):
            for agent in Agents_list:
                rnd_num = random.uniform(0,1)
                if agent.get_state()=="FUNDAMENTALIST" and Agents().agents_fund>agents_min:
                    fund_t_opt_prob=get_fund_t_opt(agent,price_elem)*t_inc
                    fund_t_pes_prob = get_fund_t_pes(agent, price_elem) * t_inc
                    if rnd_num<fund_t_opt_prob:
                        agent.set_state("OPTIMIST")
                        Agents().add_opt()
                        Agents().drop_fund()
                    elif rnd_num>1-fund_t_pes_prob:
                        agent.set_state("PESSIMIST")
                        Agents().add_pes()
                        Agents.drop_fund()
                    else:
                        agent.set_state("FUNDAMENTALIST")
                elif agent.get_state()=="OPTIMIST"and Agents().agents_opt>agents_min:
                    opt_t_fund_prob = get_opt_t_fund(agent, price_elem) * t_inc
                    opt_t_pes_prob = get_opt_t_pes(agent, price_elem) * t_inc
                    if rnd_num<opt_t_fund_prob:
                        agent.set_state("FUNDAMENTALIST")
                        Agents().add_fund()
                        Agents.drop_opt()
                    elif rnd_num>1-opt_t_pes_prob:
                        agent.set_state("PESSIMIST")
                        Agents().add_pes()
                        Agents().drop_opt()
                    else:
                        agent.set_state("OPTIMIST")
                elif agent.get_state()=="PESSIMIST"and Agents().agents_pes>agents_min:
                    pes_t_fund_prob = get_pes_t_fund(agent, price_elem) * t_inc
                    pes_t_opt_prob = get_pes_t_opt(agent, price_elem) * t_inc
                    if rnd_num<pes_t_fund_prob:
                        agent.set_state("FUNDAMENTALIST")
                        Agents.add_fund()
                        Agents.drop_pes()
                    elif rnd_num>1-pes_t_opt_prob:
                        agent.set_state("OPTIMIST")
                        Agents.add_opt()
                        Agents.drop_pes()
                    else:
                        agent.set_state("PESSIMIST")
            edc=get_edc(Agents_list[0])
            edf=get_edf(Agents_list[0],price_elem)
            ed=edc+edf
            fund_share+=edf
            noise_share+=edc
            util_update_price(Agents_list[0], price_elem)
            # if (step+1)%(int(t_inc_price / t_inc))==0:
            price_elem.update_price()
            noise_cash-=edc*price_elem.price
            fund_cash-=edf*price_elem.price

            for agent in Agents_list:
                if agent.get_state()=="FUNDAMENTALIST":
                    agent.cash=fund_cash
                    agent.share=fund_share
                else:
                    agent.cash=noise_cash
                    agent.share=noise_share
        price_elem.update_price_fund()
        price_log=np.append(price_log,price_elem.price)
        price_fund_log=np.append(price_fund_log,price_elem.price_fund)
        opt_num_log=np.append(opt_num_log,Agents().agents_opt)
        pes_num_log=np.append(pes_num_log,Agents().agents_pes)
        chart_index_log=np.append(chart_index_log,Agents().agents_noise/Agents().count_all)
        fund_num_log=np.append(fund_num_log,Agents().agents_fund)
        opinion_index=np.append(opinion_index,Agents().get_flow_noise())

    """Save Numpy to file"""
    data=[price_log,
          price_fund_log,
          opt_num_log,
          pes_num_log,
          chart_index_log,
          fund_num_log,
          opinion_index]
    np.savez('data_5000_times.npz', *data)
    """Plot"""

    plt.figure(figsize=(20, 6))
    plt.plot(price_log,linewidth = '0.5',label='Price')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.figure(figsize=(20, 6))
    plt.plot(price_fund_log,linewidth = '0.5',label='Fundamental value')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.figure(figsize=(20, 6))
    plt.plot(price_log,linewidth = '0.5',label='Price')
    plt.plot(price_fund_log,linewidth = '0.5',label='Fundamental value')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.figure(figsize=(20, 6))
    plt.plot(opt_num_log,linewidth = '0.5',label='OPTIMIST')
    plt.plot(pes_num_log,linewidth = '0.5',label="PESSIMIST")
    plt.plot(fund_num_log,linewidth = '0.5',label="FUNDAMENTALIST")
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.figure(figsize=(20, 6))
    plt.plot(chart_index_log,linewidth = '0.5',label='Chart Index')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)
    plt.ylim(bottom=0)

    plt.figure(figsize=(20,6))
    plt.plot(opinion_index,linewidth = '0.5',label='Opinion Index')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.figure(figsize=(20,6))
    plt.plot(np.diff(np.log(price_log)),color='k',linewidth = '0.5',label='Log changes of price')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)


    plt.figure(figsize=(20,6))
    plt.plot(np.diff(np.log(price_fund_log)),color='k', linewidth = '0.5',label='Log changes of Fundamental value')
    plt.legend(loc="upper left")
    plt.xlim(0, Observation_times)

    plt.show()