from collections import deque
import math
import random
random.seed(324)
class Price:
    def __init__(self,price,price_fund,pdot,que,t_inc_price):
        self.price=price
        self.price_fund=price_fund
        self.price_queue=que
        self.price_dot=pdot
        self.t_inc_price=t_inc_price


    def update_price(self):
        newprice=self.price+(sum(self.price_queue))/(len(self.price_queue))
        self.price_dot= (newprice-self.price) / self.t_inc_price
        # self.price_queue.popleft()
        # self.price_queue.append(new_price)
        self.price=newprice

    def update_price_fund(self):
        rnd_num=random.gauss(0,0.005)
        self.price_fund=math.exp(rnd_num)*self.price_fund