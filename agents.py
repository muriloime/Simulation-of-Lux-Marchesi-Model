class Agents(object):
    count_all = 500
    agents_opt = 0
    agents_pes = 0
    agents_noise = 0
    agents_fund = 0
    def __init__(self,state="FUNDAMENTALIST", cash=0, holding=0):
        self.cash = 0
        self.hoding = 0
        self.state=state

    def get_state(self):
        return self.state

    def set_state(self,state):
        assert state in ["FUNDAMENTALIST", "OPTIMIST", "PESSIMIST"]
        self.state=state

    # def initialize_class_var(self, agents_min, N):
    #     agents.count_all = N
    #     agents.agents_opt = agents_min
    #     agents.agents_pes = agents_min
    #     agents.agents_noise = agents_min * 2
    #     agents.agents_fund = N - 2 * agents_min
    @classmethod
    def add_opt(cls):
        cls.agents_opt += 1
        cls.agents_noise = cls.agents_opt + cls.agents_pes
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def drop_opt(cls):
        cls.agents_opt -= 1
        cls.agents_noise = cls.agents_opt + cls.agents_pes
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def add_pes(cls):
        cls.agents_pes +=1
        cls.agents_noise = cls.agents_opt + cls.agents_pes
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def drop_pes(cls):
        cls.agents_pes -=1
        cls.agents_noise = cls.agents_opt + cls.agents_pes
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def add_fund(cls):
        cls.agents_fund += 1
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def drop_fund(cls):
        cls.agents_fund -= 1
        # assert agents.agents_noise + agents.agents_fund == agents.count_all

    @classmethod
    def get_flow_noise(cls):
        return (cls.agents_opt - cls.agents_pes) / cls.agents_noise

    @classmethod
    def check_num(cls):
        assert cls.agents_noise==(cls.agents_opt+cls.agents_pes)
        assert cls.count_all==(cls.agents_noise+cls.agents_fund)
        print("correct")