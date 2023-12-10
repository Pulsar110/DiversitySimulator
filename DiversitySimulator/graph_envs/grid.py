from __future__ import annotations
import numpy as np 
import matplotlib.pyplot as plt
import copy
from itertools import combinations_with_replacement

from graph_envs.base_simulator import BaseSimulator, Vertex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dynamics.base_dynamic import DynamicsOutput


class GridWorld(BaseSimulator):
    '''
        Grid world that can be representated as an n-dimensional array (np.ndarray).
        With all vertices having the same degree.
    '''

    def __init__(self, world_size:int|list, *args, vertex_degree:int=4, **kwargs):
        '''
            Args:
                world_size: the size of the world (ndarray)
                vertex_degree: the degree of each vertex
        '''
        if isinstance(world_size, int):
            world_size = [world_size]
        self.world_size = world_size
        self.vertex_degree = vertex_degree
        super().__init__(np.prod(self.world_size), *args, **kwargs)
        
    def _init_world(self):
        return np.random.choice(self.num_types, self.world_size)

    def __convert_index(self, location_1D):
        '''
            Convert 1D location index to n-D location index. 
        '''						
        l = len(self.world_size)
        location_nD = np.zeros(l)

        for i in range(l-1):
            cur_size = np.prod(self.world_size[i+1:])
            location_nD[i] = location_1D // cur_size
            location_1D = location_1D % cur_size
        location_nD[-1] = location_1D
        return location_nD
    
    def get_vertice(self, loc_idx: list):
        return Vertex(
                loc_idx=loc_idx,
                type=self.get_vertex_type(loc_idx)
            )

    def get_vertex_type(self, loc_idx: list):
        v_type = self.world
        for idx in loc_idx:
            v_type = v_type[idx]
        return v_type

    def set_vertex_type(self, given_type: int, loc_idx: list):
        v_type = self.world
        for idx in loc_idx[:-1]:
            v_type = v_type[idx]
        v_type[loc_idx[-1]] = given_type

    def sample_vertices(self, num_samples: int = 1):
        '''
            Sample vertices in 1D and convert locations into n-D
        '''
        chosen_location_1Ds = np.random.choice(self.num_vertices, num_samples, replace=False)
        loc_idx_list = [list(map(int, self.__convert_index(location_1D))) 
                        for location_1D in chosen_location_1Ds] 
        return [self.get_vertice(loc_idx) for loc_idx in loc_idx_list]
    
    def _wraped_index(self, loc_idx):
        '''
            Wrap the location index. 
        '''
        for i in range(len(loc_idx)):
            if loc_idx[i] < 0:
                loc_idx[i] = self.world_size[i] + loc_idx[i]
            elif loc_idx[i] >= self.world_size[i]:
                loc_idx[i] = loc_idx[i] - self.world_size[i]
        return loc_idx
    
    def get_neighborhood_vector(self, vertex: Vertex):
        '''
            Calculate the array of types in the open neighborhood 
            of the vertex.
            It will iterate through all possible neighbors within the 
            `self.window_size` until it reaches `vertex_degree` number of
            visited neighbors. 

            Args:
                vertex: reference vertex

            Return:
                np.array of the count for each type
            
            =================
            
            Example:
            ```
                world = [[1 1 3 2 2]
                         [2 2 1 0 2]
                         [2 1 2 1 0]
                         [1 1 1 2 2]
                         [1 0 3 1 2]]
                vertex_degree = 24
                window_size = 2

                input vertex at location [2,2]
            ```
            The order of which the neighbors are visited is:
            ```
                [1, 2] # the +-cross at window_size=1
                [3, 2]
                [2, 1]
                [2, 3]

                [1, 1] # the x-cross at window_size=1
                [1, 3]
                [3, 1]
                [3, 3]

                [0, 2] # the +-cross at window_size=2
                [4, 2]
                [2, 0]
                [2, 4] 

                [0, 0] # the x-cross at window_size=2
                [0, 1]
                [0, 3]
                [0, 4]
                [4, 0]
                [4, 1]
                [4, 3]
                [4, 4]
                [1, 0]
                [3, 0]
                [1, 4]
                [3, 4]
                
                final output = [3, 10, 10, 2]
            ```
        '''
        loc_idx = vertex.loc_idx
        neigh_vector = [0]*self.num_types
        neigh_vector[vertex.type] += 1
        num_idx = len(loc_idx)

        degree = 0
        for w in range(1, self.window_size+1):
            # the +-cross part
            for i in range(num_idx):
                for new_idx in [-w, w]:
                    cur_idx = copy.copy(loc_idx)
                    cur_idx[i] += new_idx
                    cur_idx = self._wraped_index(cur_idx)
                    neigh_vector[self.get_vertex_type(cur_idx)] += 1
                    degree += 1
                    if degree == self.vertex_degree: 
                        return neigh_vector
            # the x-cross part
            for i in range(num_idx):
                # fix one index to -w or w
                for new_idx in [-w, w]:
                    # assign the left indices to numbers between [-w+1, w-1]
                    # assign the right indices to numbers between [-w, w]
                    left_numbs, right_numbs = [[]], [[]]
                    if w > 1 and i > 0:
                        left_numbs = np.stack(list(combinations_with_replacement(range(w*2-1), i))) - w+1
                    if num_idx-i > 1:
                        right_numbs = np.stack(list(combinations_with_replacement(range(w*2+1), num_idx-i-1))) - w
                    for l_idx in left_numbs:
                        for r_idx in right_numbs:
                            numbs = list(l_idx) + list(r_idx) 
                            if len(numbs) == 0:
                                continue
                            numbs = list(set(numbs))
                            if numbs[0] == 0 and len(numbs) == 1:
                                continue
                            cur_idx = np.array(list(l_idx) + [new_idx] + list(r_idx)) + np.array(vertex.loc_idx)
                            cur_idx = self._wraped_index(cur_idx.tolist())
                            neigh_vector[self.get_vertex_type(cur_idx)] += 1
                            degree += 1
                            if degree == self.vertex_degree: 
                                return neigh_vector
    
        return neigh_vector
            
    def compute_metric_summary(self): # TODO
        pass

    def visualize(self): # TODO
        pass

    