'''
    Simulation configurations.
'''
from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import type_counting_diversity_utility
from dynamics.swap import RandomSwapper, INDIVIDUAL_NO_WORSE
from metrics.diversity_metrics import number_of_colorful_edges
from metrics.metrics import social_welfare_metric


METRICS = [social_welfare_metric, number_of_colorful_edges]


def CIRCLE_WORLD(world_size:int, verbosity:int=1):
    return GridWorld([world_size], 
                     num_types=3,
                     neigh_radius=4,
                     vertex_degree=2, 
                     wrapped_indices=[True],
                     utility_func=type_counting_diversity_utility,
                     metrics=METRICS,
                     dynamics=RandomSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def CYLINDER_WORLD(world_size:int, verbosity:int=1):
    return GridWorld([2, world_size], 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=3, 
                     wrapped_indices=[False, True],
                     utility_func=type_counting_diversity_utility,
                     metrics=METRICS,
                     dynamics=RandomSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def GRID_4DEG_WORLD(world_size:list, verbosity:int=1):
    return GridWorld(world_size, 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=4, 
                     wrapped_indices=[True, True],
                     utility_func=type_counting_diversity_utility,
                     metrics=METRICS,
                     dynamics=RandomSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def GRID_8DEG_WORLD(world_size:list, verbosity:int=1):
    return GridWorld(world_size, 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=8, 
                     wrapped_indices=[True, True],
                     utility_func=type_counting_diversity_utility,
                     metrics=METRICS,
                     dynamics=RandomSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)