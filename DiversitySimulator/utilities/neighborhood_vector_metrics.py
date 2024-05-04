''' 
    Utility function based on`vertex.neigh_type_vector` 
    (a vector with each element counting the number
    of neighbours having a certain type).
'''
from __future__ import annotations
import numpy as np
from scipy.stats import entropy

from utilities.base_utility import BaseUtility
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import Vertex


class BinaryDiversityUtility(BaseUtility):
    '''
        1 if one of its neighbours is a different type than itself
        0 otherwise (if everyone is the same type than itself)
    '''
    def best_case(self, vertex: Vertex):
        return 1
    
    def compute(self, vertex: Vertex):
        if vertex.neigh_type_vector[vertex.type] == np.sum(vertex.neigh_type_vector):
            return 0
        return 1


class DifferenceCountDiversityUtility(BaseUtility):
    '''
        Count the number of neighbours with different type than itself.
    '''
    def best_case(self, vertex: Vertex):
        # degree
        return np.sum(vertex.neigh_type_vector)

    def compute(self, vertex: Vertex):
        count = 0
        for i, c in enumerate(vertex.neigh_type_vector):
            if i == vertex.type:
                continue
            count += c
        return count


class TypeCountingDiversityUtility(BaseUtility):
    '''
        Count the number of different types in the close neighborhood without counting its own type.
    '''
    def best_case(self, vertex: Vertex):
        # min(degree, type-1)
        return min(np.sum(vertex.neigh_type_vector),len(vertex.neigh_type_vector)-1)

    def compute(self, vertex: Vertex):
        neigh_type_vector = np.copy(vertex.neigh_type_vector)
        neigh_type_vector[vertex.type] = 0
        return len([i for i in neigh_type_vector if i > 0])


class AvgDiffTypeCountingDiversityUtility(BaseUtility):
    def __init__(self):
        self._diff_u = DifferenceCountDiversityUtility()
        self._type_u = TypeCountingDiversityUtility()

    def best_case(self, vertex: Vertex):
        return 1

    def compute(self, vertex: Vertex):
        avg = np.mean([self._diff_u.compute(vertex)/self._diff_u.best_case(vertex), 
                       self._type_u.compute(vertex)/self._type_u.best_case(vertex)])
        return avg


class SchellingSegregationUtility(BaseUtility):
    '''
        The fraction of its neighours that are the same type 
        than itself. 

        if thresh > 0:
            1 if the fraction of its neighbours that are 
                the same type than itself is at least thresh.
            0 otherwise.
    '''
    def best_case(self, vertex: Vertex):
        return 1

    def compute(self, vertex: Vertex, thresh: float = 0):
        utility = vertex.neigh_type_vector[vertex.type]/np.sum(vertex.neigh_type_vector)
        if thresh > 0:
            return int(utility >= thresh)
        return utility


class AntiSchellingSegregationUtility(SchellingSegregationUtility):
    '''
        The fraction of its neighours that are the same type 
        than itself. 

        if thresh > 0:
            0 if the fraction of its neighbours that are 
                the same type than itself is at least thresh.
            1 otherwise.
    '''
    def compute(self, vertex: Vertex, thresh: float = 0):
        return 1 - super().compute(vertex, thresh)


class EntropyDivertiyUtility(BaseUtility):
    '''
        The entropy of the neighbours type distribution.
    '''
    def best_case(self, vertex: Vertex):
        num_types = len(vertex.neigh_type_vector)
        graph_degree = int(np.sum(vertex.neigh_type_vector) + 1)
        best_vector = np.ones(min(num_types, graph_degree))
        j = 0
        for i in range(graph_degree - len(best_vector)):
            best_vector[j] += 1
            j += 1
            if j == len(best_vector):
                j = 0
        q = best_vector / np.sum(best_vector)
        return entropy(q)

        # return np.log(len(vertex.neigh_type_vector))

    def compute(self, vertex: Vertex):
        neigh_type_vector = np.copy(vertex.neigh_type_vector)
        neigh_type_vector[vertex.type] += 1

        num_types = len(vertex.neigh_type_vector)
        graph_degree = np.sum(vertex.neigh_type_vector)
        if graph_degree + 1 < num_types:
            to_remove = int(num_types - graph_degree - 1)
            neigh_type_vector = np.sort(neigh_type_vector)
            assert(np.sum(neigh_type_vector[:to_remove]) == 0, 
                    'Invalid entropy computation. %s type=%d, degree=%d' % (
                        str(vertex), num_types, graph_degree))
            neigh_type_vector = neigh_type_vector[to_remove:]
        
        q = neigh_type_vector / np.sum(neigh_type_vector)
        return entropy(q)
