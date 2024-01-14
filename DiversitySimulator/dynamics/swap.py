from __future__ import annotations
import numpy as np

from dynamics.base_dynamic import BaseDynamics, DynamicsOutput
from graph_envs.base_graph_env import Vertex

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment


INDIVIDUAL_GREATER = 0
INDIVIDUAL_NO_WORSE = 1
SUM_GREATER = 2
COLLECTIVE_GREATER = 3


class BaseSwapper(BaseDynamics):

    def __init__(self, swap_condition:int=0):
        '''
            Args:
                swap_condition: a function with input four utilities and decide whether to swap
        '''
        if swap_condition == INDIVIDUAL_NO_WORSE:
            self.swap_condition = lambda u1, u2, u12, u21: (u12 >= u1) and (u21 >= u2) and (u12 + u21) > (u1 + u2) 
        elif swap_condition == SUM_GREATER:
            self.swap_condition = lambda u1, u2, u12, u21: (u12 + u21) > (u1 + u2) 
        elif swap_condition == COLLECTIVE_GREATER:
            pass
            # TODO: considering neighbour utilities
        else: # swap_condition == INDIVIDUAL_GREATER
             self.swap_condition = lambda u1, u2, u12, u21: (u12 > u1) and (u21 > u2)

    def _can_swap(self, 
                   v1: Vertex, 
                   v2: Vertex, 
                   env: BaseGraphEnvironment,
                   u1:Any=None,
                   u2:Any=None):
        '''
            Can swap the colors at two locations 
            if both improve their utilities.
        '''
        v12 = Vertex(loc_idx=v2.loc_idx, type=v1.type)
        v21 = Vertex(loc_idx=v1.loc_idx, type=v2.type)

        if u1 is None:
            u1 = env.compute_utility(v1)
        if u2 is None:
            u2 = env.compute_utility(v2)
        env.move_vertices(self._swap(v1, v2))
        u12 = env.compute_utility(v12)
        u21 = env.compute_utility(v21)
        env.move_vertices(self._swap(v12, v21))

        if env.verbosity==2:
            print('Swapping', v1, 'and', v2)
            print('Old utilities:', u1, u2, '-> New utilities:', u12, u21)

        return self.swap_condition(u1, u2, u12, u21)

    def _swap(self, v1: Vertex, v2: Vertex):
        loc_idx_list = [v1.loc_idx, v2.loc_idx]
        return DynamicsOutput(
            past_locations=loc_idx_list,
            new_locations=loc_idx_list[::-1],
            is_end=False
        )


class RandomSwapper(BaseSwapper):
    '''
        Randomly select a pair of vertices and swap them if both of their utilities can 
    '''
    def step(self, env: BaseGraphEnvironment):
        samples = env.sample_vertices(2)
        if self._can_swap(samples[0], samples[1], env):
            return self._swap(samples[0], samples[1])
        return None


class UtilityOrderedSwapper(BaseSwapper):
    '''
        Iterate by priority based on the utility of the vertex
    '''
    def step(self, env: BaseGraphEnvironment):
        util_vertex = [(v, env.compute_utility(v)) for v in env]
        util_vertex.sort(key=lambda x: x[1])
        for i in range(env.num_vertices-1):
            for j in range(i+1, env.num_vertices):
                if util_vertex[i][0].type == util_vertex[j][0].type:
                    continue
                if self._can_swap(util_vertex[i][0], util_vertex[j][0], env,
                                   u1=util_vertex[i][1], u2=util_vertex[j][1]):
                    return self._swap(util_vertex[i][0], util_vertex[j][0])
        return self.end_response()