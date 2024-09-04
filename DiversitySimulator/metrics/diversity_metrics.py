''' 
    Global diversity mesures
    taking input the final type assigment 
    from the graph environment (`BaseGraphEnvironment`). 
    Normalized between 0 and 1.
'''
from __future__ import annotations
import numpy as np

from utilities.neighborhood_vector_metrics import DifferenceCountDiversityUtility
from utilities.neighborhood_vector_metrics import (
    BinaryDiversityUtility, 
    TypeCountingDiversityUtility, 
    AntiSchellingSegregationUtility, 
    EntropyDiversityUtility,
    L2Utility
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from utilities.base_utility import BaseUtility
    from graph_envs.base_graph_env import BaseGraphEnvironment


COUNT_DIFF_UTILITY = DifferenceCountDiversityUtility()
COUNT_TYPE_UTILITY = TypeCountingDiversityUtility()
L2_UTILITY = L2Utility()
DIVERSITY_UTILITIES = [BinaryDiversityUtility(), TypeCountingDiversityUtility(), DifferenceCountDiversityUtility(), EntropyDiversityUtility()]


def diff_degree_of_intergration(graph: BaseGraphEnvironment):
    '''
        DOI_k, the percentage of vertices with at least k neighbouring 
        vertices of a different type to itself.

        Return:
            vector of DOI_k from k = 1 to max degree in the graph
    '''
    doi = np.zeros(graph.get_max_degree())
    for v in graph:
        count = int(graph.compute_utility(v, COUNT_DIFF_UTILITY))
        doi[:count] += 1
    return doi/graph.num_vertices


def type_degree_of_intergration(graph: BaseGraphEnvironment):
    '''
        DOI_k, the percentage of vertices with at least k different neighbouring 
        types that are different to itself.

        Return:
            vector of DOI_k from k = 1 to number of type - 1
    '''
    doi = np.zeros(min(graph.num_types-1, graph.get_max_degree()))
    for v in graph:
        count = int(graph.compute_utility(v, COUNT_TYPE_UTILITY))
        doi[:count] += 1
    return doi/graph.num_vertices


def l2(graph: BaseGraphEnvironment):
    '''
        Sum of L2 utilities. 
    '''
    l2_utility_sum = 0
    for v in graph:
        l2_utility_sum += graph.compute_utility(v, L2_UTILITY)
    best_case = np.ones(graph.num_types)
    degree = graph.get_max_degree()
    x = degree/graph.num_types
    rem = int(degree - x*graph.num_types)
    best_case *= np.floor(x)
    best_case[:rem] += 1

    return np.sum(best_case**2)/np.abs(l2_utility_sum)


def percentage_of_segregated_verticies(graph: BaseGraphEnvironment, doi_1: float =-1):
    '''
        Percentage of vertices in the graph with no neighbour of different type.
        This can be computed by 1 - diff_DOI_1.

        Return:
            float 
    '''
    if doi_1 < 0:
        doi_1 = diff_degree_of_intergration(graph)[0]
    return 1 - doi_1
    

def number_of_colorful_edges(graph: BaseGraphEnvironment):
    '''
        The percentage of colorful edges, that is, 
        connections between vertices of different type.

        The number of coloful edges is equivalent to half of the sum of 
        diff_DOI_k (number instead of percentage) over all k.
    '''
    return np.sum(diff_degree_of_intergration(graph))*graph.num_vertices/graph.num_edges/2


def social_welfare(graph: BaseGraphEnvironment):
    '''
        Sum of utilities compared with the best and worst case
    '''
    utility_sum = np.zeros(len(DIVERSITY_UTILITIES))
    for v in graph:
        for i, util_method in enumerate(DIVERSITY_UTILITIES):
            utility_sum[i] += graph.compute_utility(v, util_method) / util_method.best_case(v) 
    return utility_sum/graph.num_vertices
