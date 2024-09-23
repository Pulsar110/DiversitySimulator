import json
from pathlib import Path
import time

from configs import CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD

from graph_envs.grid_initializations import random_init, equitable_init, schelling_segregation_random_init, schelling_segregation_equitable_init
from dynamics.swap import UtilityOrderedSwapper, get_condition_name, INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
from utilities.neighborhood_vector_metrics import (
    BinaryDiversityUtility, 
    TypeCountingDiversityUtility, 
    DifferenceCountDiversityUtility, 
    AntiSchellingSegregationUtility, 
    EntropyDiversityUtility, 
    AvgDiffTypeCountingDiversityUtility,
    L2Utility
)


# WORLDS = [CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
WORLDS = [GRID_8DEG_WORLD]
UTILITIES = [
    BinaryDiversityUtility, 
    TypeCountingDiversityUtility, 
    DifferenceCountDiversityUtility, 
    # EntropyDiversityUtility
    ]
# UTILITIES = [AvgDiffTypeCountingDiversityUtility]
INITIALIZATIONS = [
    'random_init', 
    # 'equitable_init', 
    # 'schelling_random_init', 
    # 'schelling_equitable_init'
    ] #
SWAP_CONDS = [INDIVIDUAL_GREATER] #, INDIVIDUAL_NO_WORSE, SUM_GREATER]
NUM_RUNS = 50
NUM_TYPES = [7,8] # 3,4,5,6,
WORLD_SIZE = [
    [10,10], [20,20], [30,30], 
    [40,40]]
VERBOSE = 0

for NUM_TYPE in NUM_TYPES:
    ROOT = 'results/%d_types' % (NUM_TYPE)
    Path('%s/plots' % (ROOT)).mkdir(parents=True, exist_ok=True)
    Path('%s/step_plots' % (ROOT)).mkdir(parents=True, exist_ok=True)

    def get_combination():
        for initialization in INITIALIZATIONS:
            for utility in UTILITIES:
                for swap_cond in SWAP_CONDS:
                    for world_size in WORLD_SIZE:
                        yield initialization, utility, swap_cond, world_size
                    

    for world_class in WORLDS:
        for initialization, utility, swap_cond, world_size in get_combination():
            results = {}
            filename = '%s_%s_%s_%s_(%dx%d)' % (world_class.__name__, 
                                        initialization, 
                                        get_condition_name(swap_cond), 
                                        utility.__name__,
                                        world_size[0], world_size[1])
            print(filename)
            for i in range(NUM_RUNS):
                kwargs = {
                     'utility': utility,
                     'swap_cond': swap_cond
                }
                if initialization == 'equitable_init':
                    kwargs['grid_init'] = equitable_init
                if initialization == 'schelling_random_init':
                    kwargs['grid_init'] = schelling_segregation_random_init
                if initialization == 'schelling_equitable_init':
                    kwargs['grid_init'] = schelling_segregation_equitable_init

                world = world_class(world_size, num_types=NUM_TYPE, init_rand_seed=i, verbosity=VERBOSE, **kwargs)
                # world.compute_metric_summary(print_results=True)
                # if initialization == 'schelling_init':
                #     schelling_segregation_init(world)
                if i < 3:
                    world.save_snapshot(0, '%s/step_plots/%s_%s_(%dx%d)_run_%d_step_0' % (ROOT, 
                                        world_class.__name__, initialization,
                                        world_size[0], world_size[1], i))
                results[i] = {
                    'init': world.compute_metric_summary(),
                    'init_world': world.world.tolist(),
                    'step_world': {}
                }
                # world.visualize(200, '%s/schelling_init/%s_entropy_INDIVIDUAL_NO_WORSE_%d'%(ROOT, world_class.__name__, i))
                steps = 0
                start_time = time.time()
                while world.step():
                    results[i]['step_world'][steps] = world.world.tolist()
                    steps += 1
                    #print(steps)
                run_time = time.time() - start_time
                if i < 3:
                    world.save_snapshot(steps, '%s/step_plots/%s_run_%d_step_%d' % (ROOT, filename, i, steps))
                # world.compute_metric_summary(print_results=True)
                results[i]['final'] = world.compute_metric_summary()
                results[i]['steps'] = steps
                results[i]['final_world'] = world.world.tolist()
                results[i]['type_distribution'] = world.type_distribution()
                results[i]['rume_time'] = run_time
                
                print('Run %d/%d;' % (i, NUM_RUNS), 
                      'type distribution:', results[i]['type_distribution'], 
                      '(%.2f sec)'%(run_time))
                if VERBOSE > 0:               
                    print('DONE!')

            # print(results)
            with open('%s/%s_results_.json' % (ROOT, filename), 'w') as json_file:
                json.dump(results, json_file)
