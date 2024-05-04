import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = 'results'
TYPES = [2,3,4,5,6,7,8]
WORLDS = ['CIRCLE_WORLD', 'CYLINDER_WORLD']
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 
             'DifferenceCountDiversityUtility', 'EntropyDivertiyUtility', 
             'AvgDiffTypeCountingDiversityUtility']
INITIALIZATIONS = ['random_init', 'schelling_init'] #'block_init', 
SWAP_CONDS = ['individual_greater'] #, 'individual_no_worse', 'sum_greater']

COLORS = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple',
          'tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']

for num_type in TYPES:
    Path('%s/20240503-stats/polar_plots/%d_types/' % (ROOT, num_type)).mkdir(parents=True, exist_ok=True)


def iter_graphs():
    for world in WORLDS:
        for initialization in INITIALIZATIONS:
            for utility in UTILITIES:
                for num_type in TYPES:
                    for swap_cond in SWAP_CONDS:
                        yield world, initialization, utility, num_type, swap_cond

for world, initialization, utility, num_type, swap_cond in iter_graphs():
    with open('%s/%d_types/%s_%s_%s_%s_results_.json' % (ROOT, 
                                                         num_type,
                                                         world, 
                                                         initialization, 
                                                         swap_cond, 
                                                         utility), 'r') as jsonfile:
        data = json.load(jsonfile)
    for run_i in range(3):
        for state in ['init_world', 'final_world']:
            plt.subplot(111, polar=True)
            grid = np.array(data[str(run_i)][state])
            if len(grid.shape) == 1:
                grid = grid.reshape((1,grid.shape[0]))
            bar_width = 2*np.pi/grid.shape[-1]
            for h in range(grid.shape[0]):
                for type_i in range(num_type):
                    x = [i*bar_width for i in range(grid.shape[-1]) if grid[h][i] == type_i]
                    plt.bar(x=x, height=1, width=bar_width, bottom=h+2, color=COLORS[type_i])
            plt.xticks([], '')
            plt.yticks([], '')
            plt.ylim((0, grid.shape[0]+2))
            if state == 'init_world':
                plt.title('step 0')
                plt.savefig('%s/20240503-stats/polar_plots/%d_types/%s_%s_run_%d_step_0.png'%(ROOT,num_type,world, 
                                                                                              initialization, 
                                                                                              run_i))
            else:
                steps = data[str(run_i)]['steps']
                plt.title('step %d' % (steps))
                plt.savefig('%s/20240503-stats/polar_plots/%d_types/%s_%s_%s_%s_run_%d_step_%d.png'%(ROOT,num_type,world, 
                                                                                                     initialization, 
                                                                                                     swap_cond, 
                                                                                                     utility,
                                                                                                     run_i,
                                                                                                     steps))


                # 'CIRCLE_WORLD_random_init_individual_greater_AvgDiffTypeCountingDiversityUtility_run_0_step_49')

