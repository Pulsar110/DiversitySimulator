from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass 
import numpy as np

from typing import TYPE_CHECKING, Callable, Any
if TYPE_CHECKING:
    from dynamics.base_dynamic import BaseDynamics, DynamicsOutput

@dataclass
class Vertex:
    '''
        A vertex in the graph environment.
        Args:
            loc_idx: location indices of the vertex in the graph
            type: the type of the vertex
            neigh_type_vector: neighbourhood-type vector (the number 
                               of vertex for each type in the vertex's open neighbourhood, 
                               i.e.: excluding itself)
    '''
    loc_idx: Any = None
    type: Any = None
    neigh_type_vector: np.array = None


class BaseGraphEnvironment(ABC):
    '''
        This is the base class for an arbitrary graph environment. 

        Vertices are the agents in the environment and the edges
        are indicate their immediate neighbour. 
        A vertex's neighbourhood consist of all its immediate neighbours (if neigh_radius=1), 
        and the immediate meighbours of their immediate neighbours (if neigh_radius=2),
        etc (similar pattern for neigh_radius>=3)
    '''

    def __init__(self, 
                 num_vertices: int, 
                 num_types: int, 
                 utility_func: Callable,
                 dynamics: BaseDynamics,
                 neigh_radius: int = 1,
                 verbosity: int = 0):
        '''
            Args:
                num_vertices: number of vertices in the world
                num_types: number of different types of vertices
                utility: utility metric
                dynamics: BaseDynamics object to model how the vectors move
                neigh_radius: neighbourhood radius, used for the utility metrics (default = 1)
                verbosity: for printing debug message (default 0)
        '''
        self.num_vertices = num_vertices
        self.num_types = num_types
        self._utility_func = utility_func
        self.dynamics = dynamics
        self.neigh_radius = neigh_radius
        self.verbosity = verbosity

        self.world = self._init_world()

    @abstractmethod
    def _init_world(self):
        '''
            World initialization function. 

            Return:
                Object for self.world.
        '''
        return None

    @abstractmethod
    def get_vertex(self, loc_idx: Any):
        '''
            Get a vertex at some location in the world.

            Args:
                loc_idx: a location in the world.

            Return:
                The vertex at the correct location in the world.
        '''
        return None

    def sample_vertices(self, num_samples: int = 1):
        '''
            Randomly sample vertices. This method is used for the dynamics of the world.
            Therefore, the output must be standardized.

            Args:
                num_samples: number of samples (default = 1)

            Return:
                A list of vertices of type Vertex.
        '''
        return None
    
    @abstractmethod
    def get_vertex_type(self, loc_idx: Any):
        '''
            Get the type of a vertex at loc_idx.

            Args:
                loc_idx: location idex of the vertex (must support 
                         int type to support interating over all vertices)
        '''
        return None

    @abstractmethod
    def set_vertex_type(self, given_type: Any, loc_idx: Any):
        '''
            Set a type to a vertex at loc_idx.

            Args:
                given_type: given type to set
                loc_idx: location idex of the vertex
        '''
        pass

    @abstractmethod
    def get_max_degree(self):
        '''
            Get the max degree in the graph

            Return:
                max degree 
        '''
        return None

    ### Support iteration over all vertices
    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self): 
        if self.__current >= self.num_vertices:
            raise StopIteration
        else:
            v = self.get_vertice(self.__current)
            self.__current += 1
            return v
    ### end
    
    @abstractmethod
    def get_immediate_neighbours(self, vertex: Vertex, as_dict=False):
        '''
            Get the immediate neighbours of a vertex. 

            Args:
                vertex: reference vertex
                as_dict: (optional) return as a dictionary with key=loc_idx

            Return:
                list or dict of Vertex
        '''
        return None

    def get_neighborhood_type_vector(self, vertex: Vertex):
        '''
            Calculate the array of types in the open neighborhood 
            of the vertex.
            This method is used for the utilities. 
            Therefore, the input and output must be standardized.

            Args:
                vertex: reference vertex

            Return:
                np.array of the count for each type
        '''
        neigh_type_vector = np.zeros(self.num_types)
        neigh_vertices = self.get_immediate_neighbours(vertex, as_dict=True)
        for n_v in neigh_vertices.values():
            neigh_type_vector[n_v.type] += 1
        ref_v_loc = tuple(vertex.loc_idx)
        
        neigh_loc = list(neigh_vertices.keys())
        for _ in range(1, self.neigh_radius):
            additional_neigh_loc = {}
            for i in neigh_loc:
                additional_neigh_vertices = self.get_immediate_neighbours(neigh_vertices[i], as_dict=True)
                for nn_v in additional_neigh_vertices.keys():
                    if nn_v not in neigh_vertices and nn_v != ref_v_loc:
                        neigh_vertices[nn_v] = additional_neigh_vertices[nn_v]
                        neigh_type_vector[neigh_vertices[nn_v].type] += 1
                        additional_neigh_loc[nn_v] = None
            neigh_loc = additional_neigh_loc.keys()
        return neigh_type_vector
    
    def compute_utility(self, vertex: Vertex, utility_func: Callable = None):
        '''
            Compute the utility mesure of a vertex. 
            This method is used for the dynamics. 
            Therefore, the input must be standardized.

            Args:
                vertex: reference vertex
                utility_func: (optional) the utility function to use
                              if None, use `self._utility_func`

            Return:
                the scalar utility measure
        '''
        if vertex.neigh_vector is None:
            vertex.neigh_vector = self.get_neighborhood_type_vector(vertex)
        if utility_func is None:
            return self._utility_func(vertex)
        return utility_func(vertex)
    
    def move_vertices(self, dynamic_output: DynamicsOutput):
        '''
            Logic to move the vertices. 
            Set the type of the vertex at the new location 
            to be the type of the vertex at the old locations.

            Args:
                dynamic_output: the output message of the world dynamic engine
        '''
        type_list = [self.get_vertex_type(loc_idx) for loc_idx in dynamic_output.past_locations]
        for new_loc, past_loc, to_type in zip(dynamic_output.new_locations, dynamic_output.past_locations, type_list):
            if self.verbosity == 1:
                print('Moving vertex at', past_loc, 'to', new_loc, 'type=', to_type)
            self.set_vertex_type(to_type, new_loc)

    def step(self):
        '''
            Run the simulation for one step.

            Return:
                True changed.
        '''
        response = self.dynamics.step(self)
        if response is not None:
            self.move_vertices(response)
            if self.verbosity > 0:
                print(self.world)
            return True
        return False
        
    @abstractmethod
    def compute_metric_summary(self):
        '''
            Get a summary of all metrics for the current time step.
        '''
        pass

    @abstractmethod
    def visualize(self):
        '''
            Visualization function 
        '''
        pass

    