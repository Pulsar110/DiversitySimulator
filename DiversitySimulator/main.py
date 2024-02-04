import json

from configs import CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD

from utilities.neighborhood_vector_metrics import SchellingSegregationUtility
from dynamics.swap import UtilityOrderedSwapper, INDIVIDUAL_GREATER
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
WORLDS = [CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
UTILITIES = [BinaryDiversityUtility, TypeCountingDiversityUtility, AntiSchellingSegregationUtility, EntropyDivertiyUtility]
NUM_RUNS = 10

results = {}

for world_class in WORLDS:
    results[world_class.__name__] = {}
    for utility in UTILITIES:
        results[world_class.__name__][utility.__name__] = {}
        for i in range(NUM_RUNS):
            world = world_class(verbosity=0, utility=utility)
            print(world.world)
            # world.compute_metric_summary(print_results=True)
            results[world_class.__name__][utility.__name__][i] = {
                'init': world.compute_metric_summary()
            }
            schelling_segregation_init(world)
            # world.visualize(200, '%s/schelling_init/%s_type_counting_INDIVIDUAL_NO_WORSE_%d'%(ROOT, world_class.__name__, i))
            steps = 0
            while world.step():
                steps += 1
                print(steps)
            # world.compute_metric_summary(print_results=True)
            results[world_class.__name__][utility.__name__][i]['final'] = world.compute_metric_summary()
            results[world_class.__name__][utility.__name__][i]['steps'] = steps
            print(results[world_class.__name__][utility.__name__][i])
            # v = world.get_vertex([0,0])
            # v.neigh_type_vector = world.get_neighborhood_type_vector(v)
            # print(v)
            print('DONE!')

with open('%s/random_init/results_.json') as json_file:
    json.dump(results, json_file)