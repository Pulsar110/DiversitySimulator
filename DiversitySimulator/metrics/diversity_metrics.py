''' 
    Global diversity mesures
    taking input the final type assigment 
    from the graph environment (`BaseGraphEnvironment`). 
    Normalized between 0 and 1.
'''
from __future__ import annotations
import numpy as np

from utilities.neighborhood_vector_metrics import CountDiversityUtility
from utilities.neighborhood_vector_metrics import BinaryDiversityUtility, TypeCountingDiversityUtility, AntiSchellingSegregationUtility, EntropyDivertiyUtility

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import BaseGraphEnvironment


COUNT_DIV_UTILITY = CountDiversityUtility()
DIVERSITY_UTILITIES = [BinaryDiversityUtility(), TypeCountingDiversityUtility(), AntiSchellingSegregationUtility(), EntropyDivertiyUtility()]


def degree_of_intergration(graph: BaseGraphEnvironment):
    '''
        DOI_k, the percentage of vertices with at least k neighbouring 
        vertices of a different type to itself.

        Return:
            vector of DOI_k from k = 1 to max degree in the graph
    '''
    doi = np.zeros(graph.get_max_degree())
    for v in graph:
        count = int(graph.compute_utility(v, COUNT_DIV_UTILITY))
        doi[:count] += 1
    return doi/graph.num_vertices


def percentage_of_segregated_verticies(graph: BaseGraphEnvironment, doi_1: float =-1):
    '''
        Percentage of vertices in the graph with no neighbour of different type.
        This can be computed by 1 - DOI_1.

        Return:
            float 
    '''
    if doi_1 < 0:
        doi_1 = degree_of_intergration(graph)[0]
    return 1 - doi_1
    

def number_of_colorful_edges(graph: BaseGraphEnvironment):
    '''
        The percentage of colorful edges, that is, 
        connections between vertices of different type.

        The number of coloful edges is equivalent to half of the sum of 
        DOI_k (number instead of percentage) over all k.
    '''
    return np.sum(degree_of_intergration(graph))*graph.num_vertices/graph.num_edges/2


def social_welfare(graph: BaseGraphEnvironment):
    '''
        Sum of utilities compared with the best and worst case
    '''
    utility_sum = np.zeros(len(DIVERSITY_UTILITIES))
    for v in graph:
        for i, util_method in enumerate(DIVERSITY_UTILITIES):
            utility_sum[i] += graph.compute_utility(v, util_method) / util_method.best_case(v) 
    return utility_sum/graph.num_vertices
