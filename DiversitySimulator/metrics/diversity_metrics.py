''' 
    Global diversity mesures
    taking input the final type assigment 
    from the graph environment (`BaseGraphEnvironment`). 
'''
from __future__ import annotations
import numpy as np

from utilities.neighborhood_vector_metrics import count_diversity_utility

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import BaseGraphEnvironment


def degree_of_intergration(graph: BaseGraphEnvironment):
    '''
        DOI_k, the number of vectors with at least k neighbouring 
        vectors of a different type to itself.

        Return:
            vector of DOI_k from k = 1 to max degree in the graph
    '''
    doi = np.zeros(graph.get_max_degree())
    for v in graph:
        count = graph.compute_utility(v, count_diversity_utility)
        doi[:count] += 1
    return doi


def number_of_colorful_edges(graph: BaseGraphEnvironment):
    '''
        The number of colorful edges, that is, 
        connections between vertices of different type.

        This is equivalent to half of the sum of DOI_k over all k.
    '''
    return np.sum(degree_of_intergration(graph)) / 2