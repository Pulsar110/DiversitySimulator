import json
import numpy as np
from pathlib import Path

from configs import CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD
from dynamics.swap import UtilityOrderedSwapper, get_condition_name, INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
from utilities.neighborhood_vector_metrics import BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, EntropyDivertiyUtility, AvgDiffTypeCountingDiversityUtility


# WORLDS = [CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
WORLDS = [CYLINDER_WORLD]
UTILITIES = [BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, EntropyDivertiyUtility, AvgDiffTypeCountingDiversityUtility]
INITIALIZATIONS = ['random_init', 'schelling_init'] #'block_init',
# INITIALIZATIONS_CORRECTION = {
#     'random_init': 'random_init' , 
#     'shelling_init': 'schelling_init'
# }
SWAP_CONDS = [INDIVIDUAL_GREATER] #, INDIVIDUAL_NO_WORSE, SUM_GREATER]
NUM_RUNS = 100
NUM_TYPES = [2,3,4,5,6,7,8]

for NUM_TYPE in NUM_TYPES:
    ROOT = 'results_14may_2024/%d_types' % (NUM_TYPE)
    Path('results/%d_types' % (NUM_TYPE)).mkdir(parents=True, exist_ok=True)


    def get_combination():
        for initialization in INITIALIZATIONS:
            for utility in UTILITIES:
                for swap_cond in SWAP_CONDS:
                    yield initialization, utility, swap_cond
                    

    for world_class in WORLDS:
        for initialization, utility, swap_cond in get_combination():
            filename = '%s_%s_%s_%s' % (world_class.__name__, 
                                        initialization, 
                                        get_condition_name(swap_cond), 
                                        utility.__name__)
            with open('%s/%s_results_.json' % (ROOT, filename), 'r') as json_file:
                results = json.load(json_file)


            for i in range(NUM_RUNS):
                kwargs = {
                     'utility': utility,
                     'swap_cond': swap_cond
                }
                world = world_class(num_types=NUM_TYPE, init_rand_seed=i, verbosity=0, **kwargs)
                world.world = np.array(results[str(i)]['init_world'])
                init_summary = world.compute_metric_summary()
                # print(results[str(i)]['init'])
                # print(init_summary)
                results[str(i)]['init'] = init_summary

                world.world = np.array(results[str(i)]['final_world'])
                final_summary = world.compute_metric_summary()
                # print(results[str(i)]['final'])
                # print(final_summary)
                results[str(i)]['final'] = final_summary

            filename = '%s_%s_%s_%s' % (world_class.__name__, 
                                        initialization,
                                        # INITIALIZATIONS_CORRECTION[initialization], 
                                        get_condition_name(swap_cond), 
                                        utility.__name__)
            with open('results/%d_types/%s_results_.json' % (NUM_TYPE, filename), 'w') as json_file:
                json.dump(results, json_file)

            
