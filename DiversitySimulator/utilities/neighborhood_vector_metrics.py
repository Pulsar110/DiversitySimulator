''' 
    Utility function based on`vertex.neigh_vector` 
    (a vector with each element counting the number
    of neighbours having a certain type).
'''
from __future__ import annotations
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import Vertex


def binary_diversity_utility(vertex: Vertex):
    '''
        1 if one of its neighbours is a different type than itself
        0 otherwise (if everyone is the say type than itself)
    '''
    if vertex.neigh_vector[vertex.type] == np.sum(vertex.neigh_vector):
        return 0
    return 1


def count_diversity_utility(vertex: Vertex):
    '''
        Count the number of neighbours with different type than itself.
    '''
    count = 0
    for i, c in enumerate(vertex.neigh_vector):
        if i == vertex.type:
            continue
        count += c
    return count


def type_counting_diversity_utility(vertex: Vertex):
    '''
        Count the number of different types in the open neighborhood.
    '''
    if binary_diversity_utility(vertex) == 0:
        return 0
    return len([i for i in vertex.neigh_vector if i > 0])


def schelling_segregation_utility(vertex: Vertex):
    '''
        The fraction of its neighbours that are the same type than itself.
    '''
    return vertex.neigh_vector[vertex.type]/np.sum(vertex.neigh_vector)


def anti_shelling_diversity_utility(vertex: Vertex):
    '''
        The fraction of its neighbours that are a different type than itself.
    '''
    return 1 - schelling_segregation_utility(vertex)

