from __future__ import annotations
from abc import ABC, abstractmethod 
from dataclasses import dataclass 

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_simulator import BaseSimulator

'''
    World dynamics captures the rules for moving the vertices in the world. 
'''

@dataclass
class DynamicsOutput:
    '''
        Output for dynamics for the vectors that moved

        Args:
            past_locations: list of past locations indices
            new_locations: list of new locations indices
    '''
    past_locations: list = None
    new_locations: list = None


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