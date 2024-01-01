from __future__ import annotations
import numpy as np

from dynamics.base_dynamic import BaseDynamics, DynamicsOutput
from graph_envs.base_graph_env import Vertex

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment


class RandomSwapper(BaseDynamics):
    '''
        Randomly select a pair of vertices and swap them if both of their utilities can 
    '''

    def __init__(self, pair_size:int = 2):
        '''
            Args:
                pair_size: the number of vertices to be selected per time
                TODO: hardcoded for now?
        '''
        self.pair_size = 2 # pair_size


    def __can_swap(self, v1: Vertex, v2: Vertex, env: BaseGraphEnvironment):
        '''
            Can swap the colors at two locations 
            if both improve their utilities.
        '''
        v12 = Vertex(loc_idx=v2.loc_idx, type=v1.type)
        v21 = Vertex(loc_idx=v1.loc_idx, type=v2.type)

        u1 = env.compute_utility(v1)
        u2 = env.compute_utility(v2)
        u12 = env.compute_utility(v12)
        u21 = env.compute_utility(v21)

        if env.verbosity==2:
            print('Swapping', v1, 'and', v2)
            print('Old utilities:', u1, u2, '-> New utilities:', u12, u21)

        if (u12 > u1) and (u21 > u2):
            return True
        return False

    def step(self, env: BaseGraphEnvironment):
        samples = env.sample_vertices(self.pair_size)
        if self.__can_swap(samples[0], samples[1], env):
            loc_idx_list = [v.loc_idx for v in samples]
            return DynamicsOutput(
                past_locations=loc_idx_list,
                new_locations=loc_idx_list[::-1]
            )
        return None
