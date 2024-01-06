''' 
    Utility function based on`vertex.neigh_type_vector` 
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
        0 otherwise (if everyone is the same type than itself)
    '''
    if vertex.neigh_type_vector[vertex.type] == np.sum(vertex.neigh_type_vector):
        return 0
    return 1


def count_diversity_utility(vertex: Vertex):
    '''
        Count the number of neighbours with different type than itself.
    '''
    count = 0
    for i, c in enumerate(vertex.neigh_type_vector):
        if i == vertex.type:
            continue
        count += c
    return count


def type_counting_diversity_utility(vertex: Vertex):
    '''
        Count the number of different types in the close neighborhood.
    '''
    neigh_type_vector = np.copy(vertex.neigh_type_vector)
    neigh_type_vector[vertex.type] += 1
    return len([i for i in neigh_type_vector if i > 0])


def schelling_segregation_utility(vertex: Vertex):
    '''
        1 if the fraction of its neighbours that are 
            the same type than itself is at least 0.5.
        0 otherwise.
    '''
    return int(vertex.neigh_type_vector[vertex.type]/np.sum(vertex.neigh_type_vector) >= 0.5)


def anti_shelling_diversity_utility(vertex: Vertex):
    '''
        0 if the fraction of its neighbours that are 
            the same type than itself is at least 0.5.
        1 otherwise.
    '''
    return 1 - schelling_segregation_utility(vertex)

