'''
Created on Feb 8, 2014

@author: Silver
'''

from SORSimulation import SORSimulation
from agent.TD1_agent import TD1_agent

if __name__ == "__main__":
    parameters = {"agent": TD1_agent, "agent-parameters": {"side": "Buy", "size": 15000, "price": 102, "id": "my_agent_01"}}
    sim = SORSimulation(parameters)
    sim.run()
    df = sim.get_results()
    print df