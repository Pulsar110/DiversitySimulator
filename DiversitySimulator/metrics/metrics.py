''' 
    Global performance mesures
    taking input the final type assigment 
    from the graph environment (`BaseGraphEnvironment`). 
'''
from __future__ import annotations
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import BaseGraphEnvironment


def social_welfare_metric(graph: BaseGraphEnvironment):
    '''
        Sum of utilities of vertex in the graph environment. 
    '''
    utility_sum = 0
    for v in graph:
        utility_sum += graph.compute_utility(v)
    return utility_sum
