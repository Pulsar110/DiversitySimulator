import json
from pathlib import Path

from configs import CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD

from graph_envs.grid_initializations import random_init, block_init, schelling_segregation_init
from dynamics.swap import UtilityOrderedSwapper, get_condition_name, INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
from utilities.neighborhood_vector_metrics import BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, AntiSchellingSegregationUtility, EntropyDivertiyUtility, AvgDiffTypeCountingDiversityUtility


WORLDS = [CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
# WORLDS = [GRID_8DEG_WORLD]
UTILITIES = [BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, EntropyDivertiyUtility, AvgDiffTypeCountingDiversityUtility]
INITIALIZATIONS = ['random_init', 'schelling_init'] #'block_init',
SWAP_CONDS = [INDIVIDUAL_GREATER] #, INDIVIDUAL_NO_WORSE, SUM_GREATER]
NUM_RUNS = 100
NUM_TYPES = [2,3,4,5,6,7,8]
verbosity = 1

for NUM_TYPE in NUM_TYPES:
    ROOT = 'results/%d_types' % (NUM_TYPE)
    Path('%s/plots' % (ROOT)).mkdir(parents=True, exist_ok=True)
    Path('%s/step_plots' % (ROOT)).mkdir(parents=True, exist_ok=True)

    def get_combination():
        for initialization in INITIALIZATIONS:
            for utility in UTILITIES:
                for swap_cond in SWAP_CONDS:
                    yield initialization, utility, swap_cond
                    

    for world_class in WORLDS:
        for initialization, utility, swap_cond in get_combination():
            results = {}
            filename = '%s_%s_%s_%s' % (world_class.__name__, 
                                        initialization, 
                                        get_condition_name(swap_cond), 
                                        utility.__name__)
            for i in range(NUM_RUNS):
                kwargs = {
                     'utility': utility,
                     'swap_cond': swap_cond
                }
                if initialization == 'block_init':
                    kwargs['grid_init'] = block_init
                if initialization == 'schelling_init':
                    kwargs['grid_init'] = schelling_segregation_init
                world = world_class(num_types=NUM_TYPE, init_rand_seed=i, verbosity=verbosity, **kwargs)
                print(world.toArray())
                # world.compute_metric_summary(print_results=True)
                # if initialization == 'schelling_init':
                #     schelling_segregation_init(world)
                if i < 3:
                    world.save_snapshot(0, '%s/step_plots/%s_%s_run_%d_step_0' % (ROOT, 
                                        world_class.__name__, initialization, i))
                results[i] = {
                    'init': world.compute_metric_summary(),
                    'init_world': world.toArray().tolist(),
                    'step_world': {}
                }
                # world.visualize(200, '%s/schelling_init/%s_entropy_INDIVIDUAL_NO_WORSE_%d'%(ROOT, world_class.__name__, i))
                steps = 0
                while world.step():
                    results[i]['step_world'][steps] = world.toArray().tolist()
                    steps += 1
                    #print(steps)
                if i < 3:
                    world.save_snapshot(steps, '%s/step_plots/%s_run_%d_step_%d' % (ROOT, filename, i, steps))
                # world.compute_metric_summary(print_results=True)
                results[i]['final'] = world.compute_metric_summary()
                results[i]['steps'] = steps
                results[i]['final_world'] = world.toArray().tolist()
                # print(world_class.__name__, utility.__name__, i, results[i])
                # v = world.get_vertex([0,0])
                # v.neigh_type_vector = world.get_neighborhood_type_vector(v)
                # print(v)
                print('DONE!')

            # print(results)
            with open('%s/%s_results_.json' % (ROOT, filename), 'w') as json_file:
                json.dump(results, json_file)
