import json

from configs import CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD

from graph_envs.grid_initializations import random_init, block_init
from utilities.neighborhood_vector_metrics import SchellingSegregationUtility
from dynamics.swap import UtilityOrderedSwapper, get_condition_name, INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
from utilities.neighborhood_vector_metrics import BinaryDiversityUtility, TypeCountingDiversityUtility, AntiSchellingSegregationUtility, EntropyDivertiyUtility


def schelling_segregation_init(env):
    '''
        Run Schelling segregation. 
    '''
    utility = env.utility
    dynamics = env.dynamics
    env.utility = SchellingSegregationUtility()
    env.dynamics = UtilityOrderedSwapper(INDIVIDUAL_GREATER)
    while env.step():
        pass
        # print(env.done)
    env.done = False
    env.utility = utility
    env.dynamics = dynamics


ROOT = 'results/'
# WORLDS = [CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
WORLDS = [GRID_4DEG_WORLD]
# UTILITIES = [BinaryDiversityUtility, TypeCountingDiversityUtility, AntiSchellingSegregationUtility, EntropyDivertiyUtility]
UTILITIES = [EntropyDivertiyUtility]
INITIALIZATION = ['random_init', 'block_init', 'shelling_init'][0]
SWAP_COND = [INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER][1]
NUM_RUNS = 10

for world_class in WORLDS:
    for utility in UTILITIES:
        results = {}
        for i in range(NUM_RUNS):
            kwargs = {
                 'utility': utility,
                 'swap_cond': SWAP_COND
            }
            if INITIALIZATION == 'block_init':
                kwargs['grid_init'] = block_init
            world = world_class(verbosity=0, **kwargs)
            print(world.world)
            # world.compute_metric_summary(print_results=True)
            if INITIALIZATION == 'shelling_init':
                schelling_segregation_init(world)
            results[i] = {
                'init': world.compute_metric_summary()
            }
            # world.visualize(200, '%s/schelling_init/%s_entropy_INDIVIDUAL_NO_WORSE_%d'%(ROOT, world_class.__name__, i))
            steps = 0
            while world.step():
                steps += 1
                #print(steps)
            # world.compute_metric_summary(print_results=True)
            results[i]['final'] = world.compute_metric_summary()
            results[i]['steps'] = steps
            # print(world_class.__name__, utility.__name__, i, results[i])
            # v = world.get_vertex([0,0])
            # v.neigh_type_vector = world.get_neighborhood_type_vector(v)
            # print(v)
            print('DONE!')

        # print(results)
        with open('%s/%s/%s/%s_%s_results_.json' % (ROOT, INITIALIZATION, 
                                                    get_condition_name(SWAP_COND), 
                                                    world_class.__name__, 
                                                    utility.__name__), 'w') as json_file:
            json.dump(results, json_file)
