'''
    Simulation configurations.
'''
from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import TypeCountingDiversityUtility
from dynamics.swap import RandomSwapper, UtilityOrderedSwapper, INDIVIDUAL_NO_WORSE
from metrics.diversity_metrics import number_of_colorful_edges, degree_of_intergration, social_welfare
from metrics.metrics import social_welfare_metric


# METRICS = [social_welfare_metric, number_of_colorful_edges]
METRICS = [social_welfare, degree_of_intergration, number_of_colorful_edges]


def CIRCLE_WORLD(world_size:int=40, verbosity:int=1, **kwargs):
    return GridWorld([world_size], 
                     num_types=3,
                     neigh_radius=4,
                     vertex_degree=2, 
                     wrapped_indices=[True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def CYLINDER_WORLD(world_size:int=40, verbosity:int=1, **kwargs):
    return GridWorld([2, world_size], 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=3, 
                     wrapped_indices=[False, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def GRID_4DEG_WORLD(world_size:list=[20,20], verbosity:int=1, **kwargs):
    return GridWorld(world_size, 
                     num_types=3,
                     neigh_radius=1,
                     vertex_degree=4, 
                     wrapped_indices=[True, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)


def GRID_8DEG_WORLD(world_size:list=[20,20], verbosity:int=1, **kwargs):
    return GridWorld(world_size, 
                     num_types=6,
                     neigh_radius=1,
                     vertex_degree=8, 
                     wrapped_indices=[True, True],
                     utility=kwargs['utility']() if 'utility' in kwargs else TypeCountingDiversityUtility(),
                     metrics=METRICS,
                     dynamics=UtilityOrderedSwapper(INDIVIDUAL_NO_WORSE),
                     verbosity=verbosity)