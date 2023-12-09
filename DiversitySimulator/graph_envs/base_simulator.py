from abc import ABC, abstractmethod 

from dynamics.base_dynamic import BaseDynamics, DynamicsOutput


class Vertex:
    '''
        A vertex in the world.
    '''
    loc_idx: tuple = None
    type: int = -1


class BaseSimulator(ABC):

    def __init__(self, 
                 num_vertices: int, 
                 num_types: int, 
                 utility_func: function,
                 dynamics: BaseDynamics,
                 window_size: int = 1,
                 verbosity: int = 0):
        '''
            Args:
                num_vertices: number of vertices in the world
                num_types: number of different types of vertices
                utility: utility metric
                dynamics: BaseDynamics object to model how the vectors move
                window_size: neighborhood degree considered for the utility metrics (default = 1)
                verbosity: for printing debug message (default 0)
        '''
        self.num_vertices = num_vertices
        self.num_types = num_types
        self._utility_func = utility_func
        self.dynamics = dynamics
        self.window_size = window_size
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
    def get_vertice(self, loc_idx: int|tuple|list):
        '''
            Get a vertice at some location in the world.

            Args:
                loc_idx: a location in the world.

            Return:
                The vertice at the correct location in the world.
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
    def get_vertex_type(self, loc_idx: int|tuple|list):
        '''
            Get the type of a vertex at loc_idx.

            Args:
                loc_idx: location idex of the vertex
        '''
        return None

    @abstractmethod
    def set_vertex_type(self, given_type: int|object, loc_idx: int|tuple|list):
        '''
            Set a type to a vertex at loc_idx.

            Args:
                given_type: given type to set
                loc_idx: location idex of the vertex
        '''
        pass

    @abstractmethod
    def get_neighborhood_vector(self, vertex: Vertex):
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
        return None
    
    def compute_utility(self, vertex: Vertex):
        '''
            Compute the utility mesure of a vertex. 
            This method is used for the dynamics. 
            Therefore, the input must be standardized.
        '''
        neigh_vector = self.get_neighborhood_vector(vertex)
        return self._utility_func(neigh_vector)
    
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
            if self.verbosity > 1:
                print('Moving vertex at', past_loc, 'to', new_loc, 'type=', to_type)
            self.set_vertex_type(new_loc, to_type)

    def step(self):
        '''
            Run the simulation for one step.

            Return:
                True if converged.
        '''
        response = self.dynamics.step(self)
        if response is not None:
            self.move_vertices(response)
            if self.verbosity > 0:
                print(self.world)
            return False
        
        if self.verbosity > 0:
            print('CONVERGED.')
        return True
        
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

    