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

def get_condition_name(cond):
    if cond == INDIVIDUAL_GREATER:
        return 'individual_greater'
    if cond == INDIVIDUAL_NO_WORSE:
        return 'individual_no_worse'
    if cond == SUM_GREATER:
        return 'sum_greater'
    return 'collective_greater'


class BaseSwapper(BaseDynamics):

    def __init__(self, swap_condition:int=0):
        '''
            Args:
                swap_condition: a function with input four utilities and decide whether to swap
        '''
        self.swap_condition = swap_condition

    def _pairwise_swap_condition(self, 
                                v1: Vertex, 
                                v2: Vertex, 
                                env: BaseGraphEnvironment,
                                u1:Any=None,
                                u2:Any=None):
        
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

        can_swap = False
        if self.swap_condition == INDIVIDUAL_NO_WORSE:
            can_swap = (u12 >= u1) and (u21 >= u2) and (u12 + u21) > (u1 + u2) 
        elif self.swap_condition == SUM_GREATER:
            can_swap = (u12 + u21) > (u1 + u2)
        else: # swap_condition == INDIVIDUAL_GREATER
            can_swap = (u12 > u1) and (u21 > u2)
        return can_swap

    def _collective_wise_swap_condition(self, 
                                        v1: Vertex, 
                                        v2: Vertex, 
                                        env: BaseGraphEnvironment,
                                        u1:Any=None,
                                        u2:Any=None):
        
        def _get_all_neighbour_utilities(v, u=None):
            neigh = env.get_immediate_neighbours(v)
            if u is None:
                u = env.compute_utility(v)
            return u, [env.compute_utility(n) for n in neigh]

        u1, nu1 = _get_all_neighbour_utilities(v1, u1)
        u2, nu2 = _get_all_neighbour_utilities(v2, u2)

        v12 = Vertex(loc_idx=v2.loc_idx, type=v1.type)
        v21 = Vertex(loc_idx=v1.loc_idx, type=v2.type)
        env.move_vertices(self._swap(v1, v2))
        u12, nu12 = _get_all_neighbour_utilities(v12)
        u21, nu21 = _get_all_neighbour_utilities(v21)

        # If the majority of the people, including myself, want me to move
        # Then I can move.
        score1, score2 = int(u1 < u12), int(u2 < u21)
        for i in range(len(nu1)):
            score1 += int(nu1[i] < nu21[i]) 
            score2 += int(nu2[i] < nu12[i])
        return score1 >= (len(nu1)+1)/2 and score2 >= (len(nu2)+1)/2

    def _can_swap(self, 
                   v1: Vertex, 
                   v2: Vertex, 
                   env: BaseGraphEnvironment,
                   u1:Any=None,
                   u2:Any=None):
        '''
            Can swap the type at two locations 
            if the swap condition is satisfied.
        '''
        if self.swap_condition == COLLECTIVE_GREATER:
            return self._collective_wise_swap_condition(v1, v2, env, u1, u2)
        else:
            return self._pairwise_swap_condition(v1, v2, env, u1, u2)

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