import math
import random
random.seed(324)
N = 0
v_1 = 0
v_2 = 0
alpha_1 = 0
alpha_2 = 0
alpha_3 = 0
R = 0
s = 0
t_c = 0
gamma = 0
beta = 0
std = 0
t_inc_price = 0
t_inc = 0


def set_constant(args):
    global N, v_1, v_2, alpha_1, alpha_2, alpha_3, R, s, t_c, gamma, beta, std, t_inc_price, t_inc
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


def get_Nominal_dividend(priceIns):
    return priceIns.price_fund * R


def get_U_noise(agentIns, priceIns):
    flow_noise = agentIns.get_flow_noise()
    return alpha_1 * flow_noise + (alpha_2 / v_1) * (priceIns.price_dot / priceIns.price)


def get_U_fund_opt(priceIns):
    r = get_Nominal_dividend(priceIns)
    # U_(2,1)
    return alpha_3 * ((r + priceIns.price_dot / v_2) / priceIns.price - R - s * abs(
        (priceIns.price_fund - priceIns.price) / priceIns.price))


def get_U_fund_pes(priceIns):
    r = get_Nominal_dividend(priceIns)
    # U_(2,2)
    return alpha_3 * (R - (r + priceIns.price_dot / v_2) / priceIns.price - s * abs(
        (priceIns.price_fund - priceIns.price) / priceIns.price))


def get_pes_t_opt(agentIns, priceIns):
    U_noise = get_U_noise(agentIns, priceIns)
    return v_1 * (agentIns.agents_noise / N) * math.exp(U_noise)


def get_opt_t_pes(agentIns, priceIns):
    U_noise = get_U_noise(agentIns, priceIns)
    return v_1 * (agentIns.agents_noise / N) * math.exp(-U_noise)


def get_fund_t_opt(agentIns, priceIns):
    U_fund_opt = get_U_fund_opt(priceIns)
    return v_2 * (agentIns.agents_opt / N) * math.exp(U_fund_opt)


def get_opt_t_fund(agentIns, priceIns):
    U_fund_opt = get_U_fund_opt(priceIns)
    return v_2 * (agentIns.agents_fund / N) * math.exp(-U_fund_opt)


def get_fund_t_pes(agentIns, priceIns):
    U_fund_pes = get_U_fund_pes(priceIns)
    return v_2 * (agentIns.agents_pes / N) * math.exp(U_fund_pes)


def get_pes_t_fund(agentIns, priceIns):
    U_fund_pes = get_U_fund_pes(priceIns)
    return v_2 * (agentIns.agents_fund / N) * math.exp(-U_fund_pes)


def get_edc(agentIns):
    return (agentIns.agents_opt - agentIns.agents_pes) * t_c


def get_edf(agentIns, priceIns):
    return agentIns.agents_fund * gamma * ((priceIns.price_fund - priceIns.price) / priceIns.price)


def util_update_price(agentIns, priceIns):
    efc = get_edc(agentIns)
    edf = get_edf(agentIns, priceIns)
    ed = efc + edf
    pro_up = max(0, beta * ed)
    pro_down = -min(0, beta * ed)
    rnd_num=random.uniform(0,1)
    if ed>0 and pro_up>rnd_num:
        price_change=0.001 * priceIns.price
        priceIns.price_queue.append(price_change)
        # newprice = priceIns.price + 0.001 * priceIns.price
        # priceIns.update_price(newprice)
    elif ed<0 and pro_down>rnd_num:
        price_change = -0.001 * priceIns.price
        priceIns.price_queue.append(price_change)
        # newprice = priceIns.price - 0.001 * priceIns.price
        # priceIns.update_price(newprice)
    else:
        price_change = 0
        priceIns.price_queue.append(price_change)
        # newprice = priceIns.price
        # priceIns.update_price(newprice)
    priceIns.price_queue.popleft()
    # print(priceIns.price_queue)
    # return price_change
    # priceIns.price_dot=price_change/t_inc