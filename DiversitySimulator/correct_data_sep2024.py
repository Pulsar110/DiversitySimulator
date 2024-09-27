import json
import numpy as np
from pathlib import Path

from configs import CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD
from dynamics.swap import UtilityOrderedSwapper, get_condition_name, INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
from utilities.neighborhood_vector_metrics import BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, AvgDiffTypeCountingDiversityUtility


WORLDS = [('400', CIRCLE_WORLD), ('2x200', CYLINDER_WORLD), 
			('20x20',GRID_4DEG_WORLD), ('20x20', GRID_8DEG_WORLD)]
# WORLDS = [('20x20', GRID_8DEG_WORLD)]
UTILITIES = [BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility, AvgDiffTypeCountingDiversityUtility]
INITIALIZATIONS = ['random_init', 'schelling_random_init', 'equitable_init', 'schelling_equitable_init'] 
SWAP_CONDS = [INDIVIDUAL_GREATER] #, INDIVIDUAL_NO_WORSE, SUM_GREATER]
NUM_RUNS = 30
NUM_TYPES = [2]

for NUM_TYPE in NUM_TYPES:
    ROOT = 'results/%d_types' % (NUM_TYPE)
    # ROOT = '../results_may_2024/corrected_%d_types/%d_types' % (NUM_TYPE, NUM_TYPE)
    # Path('results/%d_types' % (NUM_TYPE)).mkdir(parents=True, exist_ok=True)


    def get_combination():
        for initialization in INITIALIZATIONS:
            for utility in UTILITIES:
                for swap_cond in SWAP_CONDS:
                    yield initialization, utility, swap_cond
                    

    for world_size, world_class in WORLDS:
        for initialization, utility, swap_cond in get_combination():
            print(world_class, initialization, utility)
            filename = '%s_%s_%s_%s' % (world_class.__name__, 
                                        initialization, 
                                        get_condition_name(swap_cond), 
                                        utility.__name__)
            with open('%s/%s_(%s)_results_.json' % (ROOT, filename, world_size), 'r') as json_file:
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

            if 'schelling_init' == initialization:
                filename.replace('schelling_init', 'schelling_random_init')
                
            with open('results/%d_types/%s_(%s)_results_.json' % (NUM_TYPE, filename, world_size), 'w') as json_file:
                json.dump(results, json_file)            