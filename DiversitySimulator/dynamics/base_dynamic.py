from __future__ import annotations
from abc import ABC, abstractmethod 
from dataclasses import dataclass 

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment

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
            is_end: True if there is no more moves to make
    '''
    past_locations: list = None
    new_locations: list = None
    is_end: bool = None


class BaseDynamics(ABC):

    @abstractmethod
    def step(self, env: BaseGraphEnvironment):
        '''
            Run the dynamics for one step.

            Args:
                env: the simulator object

            Return:
                DynamicsOutput
        '''
        return None
    
    def end_response(self):
        return DynamicsOutput(
            past_locations=None,
            new_locations=None,
            is_end=True
        )