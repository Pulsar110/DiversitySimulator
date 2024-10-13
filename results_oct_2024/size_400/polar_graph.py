import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = '.'
TYPES = [2,3,4,5,6,7,8,9]
WORLDS = [('400', 'CIRCLE_WORLD'), ('2x200', 'CYLINDER_WORLD')]
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 
             'DifferenceCountDiversityUtility', 
             'AvgDiffTypeCountingDiversityUtility']
INITIALIZATIONS = [
    'random_init', 
    'equitable_init', 
    'schelling_random_init', 
    'schelling_equitable_init'
    ]
SWAP_CONDS = ['individual_greater'] #, 'individual_no_worse', 'sum_greater']
NUM_RUN = 30

COLORS = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple',
          'tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']

def iter_graphs():
    for world_size, world in WORLDS:
        for initialization in INITIALIZATIONS:
            for num_type in TYPES:
                yield world, world_size, initialization, num_type
                # for utility in UTILITIES:
                #     for swap_cond in SWAP_CONDS:
                #         yield world, world_size, initialization, utility, num_type, swap_cond

for world, world_size, initialization, num_type in iter_graphs():
    for run_i in range(3):
        plot_init = True
        for utility in UTILITIES:
            for swap_cond in SWAP_CONDS:
                with open('%s/%d_types/%s_%s_%s_%s_(%s)_results_.json' % (ROOT, 
                                                                     num_type,
                                                                     world, 
                                                                     initialization, 
                                                                     swap_cond, 
                                                                     utility,
                                                                     world_size), 'r') as jsonfile:
                    data = json.load(jsonfile)
                iterable_states = ['init_world', 'final_world']
                if not plot_init:
                    iterable_states = ['final_world']
                plot_init = False

                for state in iterable_states:
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
                        plt.savefig('%s/%d_types/step_plots/%s_%s_(%s)_run_%d_step_0.png' % (ROOT, num_type, 
                                                                                                    world, 
                                                                                                    initialization, 
                                                                                                    world_size, 
                                                                                                    run_i))
                    else:
                        steps = data[str(run_i)]['steps']
                        plt.title('step %d' % (steps))
                        plt.savefig('%s/%d_types/step_plots/%s_%s_%s_%s_(%s)_run_%d_step_%d.png'%(ROOT,num_type,
                                                                                                        world, 
                                                                                                        initialization, 
                                                                                                        swap_cond, 
                                                                                                        utility,
                                                                                                        world_size,
                                                                                                        run_i,
                                                                                                        steps))
                    plt.close()
