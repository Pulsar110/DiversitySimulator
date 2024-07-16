from __future__ import annotations
import numpy as np 
import copy
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from graph_envs.base_graph_env import BaseGraphEnvironment, Vertex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dynamics.base_dynamic import DynamicsOutput


class GridWorld(BaseGraphEnvironment):
    '''
        Grid world that can be representated as an n-dimensional array (np.ndarray).
        With all vertices having the same degree.
    '''

    def __init__(self, 
                 world_size:int|list, 
                 *args, 
                 vertex_degree:int=4, 
                 wrapped_indices:bool|list=True, 
                 **kwargs):
        '''
            Args:
                world_size: the size of the world (ndarray)
                vertex_degree: the degree of each vertex
        '''
        if isinstance(world_size, int):
            world_size = [world_size]
        self.world_size = world_size
        self.vertex_degree = vertex_degree
        if isinstance(wrapped_indices, bool):
            wrapped_indices = [wrapped_indices]*len(world_size)
        else:
            assert(len(wrapped_indices) == len(world_size))
        self.wrapped_indices = wrapped_indices
        num_vertices = np.prod(self.world_size)
        super().__init__(num_vertices, num_vertices*vertex_degree/2, *args, **kwargs)
        
    def __convert_index(self, location_1D):
        '''
            Convert 1D location index to n-D location index. 
        '''						
        l = len(self.world_size)
        if l == 1:
            return [location_1D]
        location_nD = np.zeros(l)

        for i in range(l-1):
            cur_size = np.prod(self.world_size[i+1:])
            location_nD[i] = int(location_1D // cur_size)
            location_1D = location_1D % cur_size
        location_nD[-1] = int(location_1D)
        return location_nD

    def _get_vertex(self, loc_idx: list):
        v = self.world
        for idx in loc_idx:
            v = v[idx]
        return v
    
    def get_vertex(self, loc_idx: int|list, init=True):
        if isinstance(loc_idx, int):
            loc_idx = self.__convert_index(loc_idx)
        v = self._get_vertex(loc_idx)
        if not isinstance(v, Vertex):
            v = Vertex(
                loc_idx=loc_idx,
                type=v
            )
            if init:
                self.compute_utility(v)
                location = self.world
                for idx in loc_idx[:-1]:
                    location = location[idx]
                location[loc_idx[-1]] = v
        return v

    def get_vertex_type(self, loc_idx: int|list):
        return self.get_vertex(loc_idx).type

    def set_vertex_type(self, given_type: int, loc_idx: int|list):
        v = self.get_vertex(loc_idx)
        v.type = given_type
        self.compute_utility(v)
        for n_v in self.get_immediate_neighbours(v):
            self.compute_utility(n_v)

    def toArray(self):
        return np.reshape([v.type for v in self], self.world_size)

    def get_max_degree(self):
        return self.vertex_degree

    def sample_vertices(self, num_samples: int = 1):
        '''
            Sample vertices in 1D and convert locations into n-D
        '''
        chosen_location_1Ds = np.random.choice(self.num_vertices, num_samples, replace=False)
        loc_idx_list = [list(map(int, self.__convert_index(location_1D))) 
                        for location_1D in chosen_location_1Ds] 
        return [self.get_vertex(loc_idx) for loc_idx in loc_idx_list]
    
    def _wraped_index(self, loc_idx: list):
        '''
            Wrap the location index. Return None if it not allowed to wrap if needed.
        '''
        for i in range(len(loc_idx)):
            if loc_idx[i] < 0:
                if not self.wrapped_indices[i]:
                    return None
                loc_idx[i] = self.world_size[i] + loc_idx[i]
            elif loc_idx[i] >= self.world_size[i]:
                if not self.wrapped_indices[i]:
                    return None
                loc_idx[i] = loc_idx[i] - self.world_size[i]
        return loc_idx
    
    def get_immediate_neighbours(self, vertex: Vertex, as_dict=False):
        '''
            Get the immediate neighbours of a vertex. 
            It will iterate through all possible neighbors
            until it reaches `vertex_degree` number of
            visited neighbors. 
            
            Args:
                vertex: reference vertex
                as_dict: (optional) return as a dictionary with key=loc_idx

            Return:
                list or dict of Vertex
            
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
            ```
        '''
        loc_idx = vertex.loc_idx
        num_idx = len(loc_idx)
        neigh_vertices = {}

        def __return_neigh_vertices():
            if as_dict:
                return neigh_vertices
            return neigh_vertices.values()
    
        def __add_vertex(cur_idx, degree):
            cur_idx = self._wraped_index(cur_idx)
            if cur_idx is not None:
                v = self.get_vertex(cur_idx, init=False)
                neigh_vertices[tuple(v.loc_idx)] = v
                degree += 1
            return degree

        degree = 0
        for w in range(1, np.min(self.world_size)):
            # the +-cross part
            for i in range(num_idx):
                for new_idx in [-w, w]:
                    cur_idx = copy.copy(loc_idx)
                    cur_idx[i] += new_idx
                    degree = __add_vertex(cur_idx, degree)
                    if degree == self.vertex_degree: 
                        return __return_neigh_vertices()
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
                            degree = __add_vertex(cur_idx.tolist(), degree)
                            if degree == self.vertex_degree: 
                                return __return_neigh_vertices()
    
        if degree < self.vertex_degree: 
            print('Warning! Only found %d degree for world size:' % degree, self.world_size)
        return __return_neigh_vertices()
    
    def save_snapshot(self, step_n, fig_name):
        fig, ax = plt.subplots()
        if len(self.world_size) == 1:
            grid_world = np.tile(self.toArray(), (2,1))
            ax.imshow(grid_world)
        else:
            ax.imshow(self.toArray())
        ax.set_title('Step: %d' % (step_n))
        plt.savefig(fig_name+'.png')

    def visualize(self, num_steps:int, name:str=None):
        assert len(self.world_size) == 2

        fig, ax = plt.subplots()
        self.viz_metrics = self.compute_metric_summary(to_str=True)
        self.save_snapshot(0, '%s_init'%(name))
        
        def step_visualize(i):
            print('Step', i)
            if i>0 and i<num_steps and self.step():
                self.viz_metrics = self.compute_metric_summary(to_str=True)
            ax.imshow(self.toArray())
            ax.set_title('Step: %d, %s' % (min(i, num_steps), self.viz_metrics))
            if i == num_steps:
                self.save_snapshot(i, '%s_final'%(name))
            return ax,

        ani = animation.FuncAnimation(fig, step_visualize, frames=num_steps+10, interval=1)
        # plt.show()

        # To save the animation using Pillow as a gif
        writer = animation.PillowWriter(fps=10,
                                        metadata=dict(artist='Diversity Simulator'),
                                        bitrate=1800)
        ani.save('%s_simulation.gif'%(name), writer=writer)