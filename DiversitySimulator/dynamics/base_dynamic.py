from abc import ABC, abstractmethod 
import numpy as np

from graph_envs.base_simulator import BaseSimulator

'''
    World dynamics captures the rules for moving the vertices in the world. 
'''

class DynamicsOutput:
    '''
        Output for dynamics for the vectors that moved

        Args:
            past_locations: list of past locations indices
            new_locations: list of new locations indices
    '''
    past_locations: np.array = None
    new_locations: np.array = None


class BaseDynamics(ABC):

    @abstractmethod
    def step(self, env: BaseSimulator):
        '''
            Run the dynamics for one step.

            Args:
                env: the simulator object

            Return:
                DynamicsOutput
        '''
        return None