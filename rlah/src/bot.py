""" currently unused """
from rlah import Player

class Agent(Player):
    
    def __init__(self, char):
        super().__init__(char)
        self.learning_rate = 0.1
        self.discount_rate = 0.99
        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.01