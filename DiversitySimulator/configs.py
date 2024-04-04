'''
    Simulation configurations.
'''
from graph_envs.grid import GridWorld
from graph_envs.grid_initializations import random_init
from utilities.neighborhood_vector_metrics import TypeCountingDiversityUtility
from dynamics.swap import RandomSwapper, UtilityOrderedSwapper, INDIVIDUAL_NO_WORSE
from metrics.diversity_metrics import number_of_colorful_edges, degree_of_intergration, social_welfare, percentage_of_segregated_verticies
from metrics.metrics import social_welfare_metric


# METRICS = [social_welfare_metric, number_of_colorful_edges]
METRICS = [social_welfare, degree_of_intergration, number_of_colorful_edges]


def CIRCLE_WORLD(world_size:int=40, verbosity:int=1, **kwargs):
    return GridWorld([world_size], 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=2, 
                     wrapped_indices=[False],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(kwargs['swap_cond'] if 'swap_cond' in kwargs else INDIVIDUAL_NO_WORSE),
                     init_func=kwargs['grid_init'] if 'grid_init' in kwargs else random_init,
                     verbosity=verbosity)


def CYLINDER_WORLD(world_size:int=40, verbosity:int=1, **kwargs):
    return GridWorld([2, world_size], 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=3, 
                     wrapped_indices=[False, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(kwargs['swap_cond'] if 'swap_cond' in kwargs else INDIVIDUAL_NO_WORSE),
                     init_func=kwargs['grid_init'] if 'grid_init' in kwargs else random_init,
                     verbosity=verbosity)


def GRID_4DEG_WORLD(world_size:list=[20,20], verbosity:int=1, **kwargs):
    return GridWorld(world_size, 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=4, 
                     wrapped_indices=[True, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(kwargs['swap_cond'] if 'swap_cond' in kwargs else INDIVIDUAL_NO_WORSE),
                     init_func=kwargs['grid_init'] if 'grid_init' in kwargs else random_init,
                     verbosity=verbosity)


def GRID_8DEG_WORLD(world_size:list=[20,20], verbosity:int=1, **kwargs):
    return GridWorld(world_size, 
                     num_types=6,
                     neigh_radius=1,
                     vertex_degree=8, 
                     wrapped_indices=[True, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(kwargs['swap_cond'] if 'swap_cond' in kwargs else INDIVIDUAL_NO_WORSE),
                     init_func=kwargs['grid_init'] if 'grid_init' in kwargs else random_init,
                     verbosity=verbosity)