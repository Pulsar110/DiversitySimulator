import json
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,5)


legend_label_map = {
    'social_welfare_0': 'soc. wel. (Binary)',
    'social_welfare_1': 'soc. wel. (TypeCount)',
    'social_welfare_2': 'soc. wel. (DiffCount)',
    'social_welfare_3': 'soc. wel. (Entropy)',
    'type_degree_of_intergration_-1': 'DIO_T (last)',
    'diff_degree_of_intergration_-1': 'DIO_C (last)',
    'percentage_of_segregated_verticies': '% of seg. vertices',
    'number_of_colorful_edges': '# colorful edges',
    'l2': 'evenness'
}

ROOT = '..'
NUM_RUN = 30
TYPES = [2,3,4,5,6,7,8,9]
WORLDS = [('400', 'CIRCLE_WORLD'), ('2x200', 'CYLINDER_WORLD'),
          ('20x20','GRID_4DEG_WORLD'), ('20x20', 'GRID_8DEG_WORLD')]
# WORLDS = [('20x20','GRID_4DEG_WORLD')]
INITIALIZATIONS = [
    'schelling_random_init', 
    'random_init', 
    # 'schelling_equitable_init',
    # 'equitable_init'
    ]

UTILITIY_LABELS = {
    'BinaryDiversityUtility': 'Binary', 
    'TypeCountingDiversityUtility': 'Variety-seeking', 
    'DifferenceCountDiversityUtility': 'Difference-seeking', 
    'AvgDiffTypeCountingDiversityUtility': 'AvgDiffVarSeeking',
    # 'L2Utility': 'Evenness-seeking'
}
SWAP_CONDS = ['individual_greater']

# focused_metrics = ['l2', 'number_of_colorful_edges']
focused_metrics = ['type_degree_of_intergration_-1', 'diff_degree_of_intergration_-1']



if True: # plot all utilities in each graph 
    UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 
                 'DifferenceCountDiversityUtility', 'AvgDiffTypeCountingDiversityUtility',
                 # 'L2Utility'
                 ]

    def read_file(metric, world, world_size, initialization, utility, state='final'):
        line_data = {}
        for num_type in TYPES:
            swap_cond = SWAP_CONDS[0]
            with open('%s/%d_types/%s_%s_%s_%s_(%s)_results_.json' % (ROOT, 
                                                                 num_type,
                                                                 world,
                                                                 initialization, 
                                                                 swap_cond, 
                                                                 utility,
                                                                 world_size), 'r') as jsonfile:
                data = json.load(jsonfile)

            if metric not in data['0'][state]:
                orig_metric, axis = metric.rsplit('_', 1)
                sub_data = np.array([data[str(d_i)][state][orig_metric][int(axis)] for d_i in range(NUM_RUN)])
            else:
                sub_data = np.array([data[str(d_i)][state][metric] for d_i in range(NUM_RUN)])
            mean_metrics = np.mean(sub_data, axis=0)
            line_data[num_type] = mean_metrics
        return line_data

    def iter_graphs():
        for metric in focused_metrics:
            for world_size, world in WORLDS:
                yield metric, world, world_size

    def iter_line(metric, world, world_size, initialization):
        for i, utility in enumerate(UTILITIES):
                
            short_utility = UTILITIY_LABELS[utility]
            line_data = read_file(metric, world, world_size, initialization, utility)
            yield short_utility, line_data
        line_data = read_file(metric, world, world_size, initialization, utility, state='init')
        yield 'init', line_data

    for metric, world, world_size in iter_graphs(): 
        short_world = world.replace('_WORLD', '')
        fig, ax = plt.subplots(1,2)
        y_min=1
        y_max=-1
        for i, initialization in enumerate(INITIALIZATIONS):
            for utility, line_data in iter_line(metric, world, world_size, initialization):
                mod_initialization = initialization.replace('_',' ').replace('sche', 'Sche').replace('rand', 'Rand')
                y = [line_data[x] for x in TYPES]
                y_min = min(np.min(y), y_min)
                y_max = max(np.max(y), y_max)
                if utility == 'init':
                    utility = mod_initialization
                    if i == 1:
                        ax[1].plot(TYPES, y, '--', color='black', label=utility)
                        ax[0].plot(TYPES, y, '--', color='black', label=utility)
                    else:
                        ax[1-i].plot(TYPES, y, '-.', color='red', label=utility)
                else:
                    ax[1-i].plot(TYPES, y, label=utility)
            ax[1-i].set_xlabel('Number of types')
            ax[1-i].set_ylabel('Metric: %s' % legend_label_map[metric])
            ax[1-i].set_title(mod_initialization)
        for i in range(2):
            ax[i].set_ylim((y_min, y_max))
        box_0 = ax[0].get_position()
        ax[0].set_position([box_0.x0, box_0.y0, box_0.width * 0.9, box_0.height])
        box_1 = ax[1].get_position()
        ax[1].set_position([box_1.x0-box_0.width * 0.1, box_1.y0, box_1.width * 0.9, box_1.height])
        ax[1].legend(title='Utility', bbox_to_anchor=(1.0, 0.5))
        plt.suptitle('%s, %s' % (legend_label_map[metric], short_world))
        # plt.show()
        plt.savefig('avg_plots/random_%s_%s.png' % (short_world, legend_label_map[metric]))
        plt.close()

if True: # plot PoA for each graph 
    UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 
                 'DifferenceCountDiversityUtility']
    UTILITY_SW_MAP = {
        'BinaryDiversityUtility': 0, 
        'TypeCountingDiversityUtility': 1, 
        'DifferenceCountDiversityUtility': 2
    }

    def iter_graphs():
        for utility in UTILITIES:
            for initialization in INITIALIZATIONS:
                yield utility, initialization

    def read_file(world, world_size, initialization, utility):
        line_data = {}
        for num_type in TYPES:
            swap_cond = SWAP_CONDS[0]
            with open('%s/%d_types/%s_%s_%s_%s_(%s)_results_.json' % (ROOT, 
                                                                     num_type,
                                                                     world,
                                                                     initialization, 
                                                                     swap_cond, 
                                                                     utility,
                                                                     world_size), 'r') as jsonfile:
                data = json.load(jsonfile)

            ce = np.array([d['final']['number_of_colorful_edges'] for d in data.values()])
            poa = np.array([d['final']['social_welfare'][UTILITY_SW_MAP[utility]] for d in data.values()])
            line_data[num_type] = {'PoA(CE)': np.mean(ce, axis=0),
                                   'PoA(SW)': np.mean(poa, axis=0)}

        return line_data

    def iter_line(utility, initialization):
        for world_size, world in WORLDS:
            short_utility = UTILITIY_LABELS[utility]
            line_data = read_file(world, world_size, initialization, utility)
            yield world, short_utility, line_data

    for utility, initialization in iter_graphs():
        mod_initialization = initialization.replace('_',' ').replace('sche', 'Sche').replace('rand', 'Rand')
        fig, ax = plt.subplots(1,2)
        y_max = 1
        for world, utility, line_data in iter_line(utility, initialization):
            for i, sub_title in enumerate(['PoA(CE)', 'PoA(SW)']):
                y = [1.0/line_data[x][sub_title] for x in TYPES]
                world = world.replace('_WORLD', '')
                ax[i].plot(TYPES, y, label=world)
                y_max = max(np.max(y), y_max)
        for i, sub_title in enumerate(['PoA(CE)', 'PoA(SW)']):
            ax[i].set_xlabel('Number of types')
            ax[i].set_ylabel(sub_title)
            ax[i].legend(title='Graph')
        plt.suptitle('%s, %s' % (utility, mod_initialization))
        plt.savefig('poa_plots/PoA_%s_%s.png' % (utility, initialization))
        plt.close()