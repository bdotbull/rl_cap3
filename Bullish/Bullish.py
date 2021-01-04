from tools import  *
from objects import *
from routines import *


#This file is for strategy

class BullBot(GoslingAgent):
    def run(agent):
        # Using raw utilities:
        relative_target = agent.foes[0].location - agent.me.location # chases opponent
        local_target = agent.me.local(relative_target)  # convert into local coords
        
        # once we have it in local coords, we can pass it to the two main functions.
        defaultPD(agent, local_target) #
        defaultThrottle(agent, 2300)  # gets car to certain speed (max==2300)
'''
        #An example of pushing routines to the stack:
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            else:
                agent.push(atba())  # basically the same thing as the 
                                    # example using raw utils, seen above
'''
