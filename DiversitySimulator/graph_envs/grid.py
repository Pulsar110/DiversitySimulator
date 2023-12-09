import numpy as np 
import matplotlib.pyplot as plt
import copy
from typing import Union

from graph_envs.base_simulator import BaseSimulator, Vertex
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

    def get_vertex_type(self, loc_idx: int|tuple|list):
        v_type = self.world
        for idx in loc_idx:
            v_type = v_type[idx]
        return v_type

    def set_vertex_type(self, given_type: int, loc_idx: int|tuple|list):
        v_type = self.world
        for idx in loc_idx[:-1]:
            v_type = v_type[idx]
        v_type[loc_idx[-1]] = given_type

    def sample_vertices(self, num_samples: int = 1):
        '''
            Sample vertices in 1D and convert locations into n-D
        '''
        chosen_location_1Ds = np.random.choice(self.num_vertices, num_samples, replace=False)
        loc_idx_list = [list(map(int, self.__get_index(location_1D))) 
                        for location_1D in chosen_location_1Ds] 
        return [
            Vertex(
                loc_idx=loc_idx,
                type=self.get_vertex_type(loc_idx)
            ) for loc_idx in loc_idx_list
        ]
    

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
            TODO: add window size and vertex degree
        '''
        loc_idx = vertex.loc_idx
        neigh_vector = [0]*self.num_types
        neigh_vector[vertex.type] += 1

        for i, idx in enumerate(loc_idx):
            cur_idx = copy.copy(loc_idx)
            cur_idx[i] += 1
            cur_idx = self._wraped_index(cur_idx)
            neigh_vector[self.get_vertex_type(cur_idx)] += 1

            cur_idx = copy.copy(loc_idx)
            cur_idx[i] -= 1
            cur_idx = self._wraped_index(cur_idx)
            neigh_vector[self.get_vertex_type(cur_idx)] += 1

        return neigh_vector
            
        
    def compute_metric_summary(self): # TODO
        pass

    def visualize(self): # TODO
        pass

    