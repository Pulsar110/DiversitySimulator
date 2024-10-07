import json
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,5)

legend_label_map = {
    'social_welfare_0': 'DoI',
    'social_welfare_1': 'NV', 
    'number_of_colorful_edges': 'CE',
    'l2': 'EV'
}

ROOT = '..'
NUM_RUN = 50
TYPES = [2,3,4,5,6,7]
WORLDS = [
        # ('900', 'CIRCLE_WORLD'), 
        # ('2x450', 'CYLINDER_WORLD'),
          ('30x30','GRID_4DEG_WORLD'), 
          # ('20x20', 'GRID_8DEG_WORLD')
          ]
INITIALIZATIONS = [
    ('random_init', 'Random Input'), 
    ('schelling_random_init', 'Schelling Input'), 
    ]

UTILITIY_LABELS = {
    'BinaryDiversityUtility': 'Binary', 
    'DifferenceCountDiversityUtility': 'Difference-seeking', 
    'TypeCountingDiversityUtility': 'Variety-seeking', 
    'AvgDiffTypeCountingDiversityUtility': 'AvgDiffVarSeeking'
}

UTILITIY_MARKERS = {
    'BinaryDiversityUtility': 'o', 
    'DifferenceCountDiversityUtility': '^', 
    'TypeCountingDiversityUtility': '*', 
    'AvgDiffTypeCountingDiversityUtility': 's'
}

UTILITIY_NORMALIZE = {
    'BinaryDiversityUtility': False, 
    'DifferenceCountDiversityUtility': False, 
    'TypeCountingDiversityUtility': False, 
    'AvgDiffTypeCountingDiversityUtility': False
}

SWAP_CONDS = ['individual_greater']

if True: # plot avg
    focused_metrics = ['social_welfare_0', 
                       'number_of_colorful_edges', 
                       'social_welfare_1',
                       'l2']
    UTILITIES = ['BinaryDiversityUtility', 
                 'DifferenceCountDiversityUtility',
                 'TypeCountingDiversityUtility']

    def read_file(world, world_size, initialization, utility, state='final'):
        line_data = {}
        for num_type in TYPES:
            line_data[num_type] = {}
            swap_cond = SWAP_CONDS[0]
            with open('%s/%d_types/%s_%s_%s_%s_(%s)_results_.json' % (ROOT, 
                                                                 num_type,
                                                                 world,
                                                                 initialization, 
                                                                 swap_cond, 
                                                                 utility,
                                                                 world_size), 'r') as jsonfile:
                data = json.load(jsonfile)
            for metric in focused_metrics:
                if metric not in data['0'][state]:
                    orig_metric, axis = metric.rsplit('_', 1)
                    sub_data = np.array([data[str(d_i)][state][orig_metric][int(axis)] 
                                         for d_i in range(NUM_RUN)])
                else:
                    sub_data = np.array([data[str(d_i)][state][metric] for d_i in range(NUM_RUN)])
                mean_metrics = np.mean(sub_data, axis=0)
                if metric == 'social_welfare_1':
                    mean_metrics = mean_metrics*min(num_type-1,4) # FOR 4DEG
                line_data[num_type][metric] = mean_metrics
        return line_data

    def iter_line(world, world_size, initialization_pair):
        initialization, mod_initialization = initialization_pair
        for i, utility in enumerate(UTILITIES):
            short_utility = UTILITIY_LABELS[utility]
            line_data = read_file(world, world_size, initialization, utility)
            yield short_utility, UTILITIY_MARKERS[utility], line_data
        line_data = read_file(world, world_size, initialization, utility, state='init')
        yield initialization, mod_initialization, line_data

    y_min={m_i: 1 for m_i in range(len(focused_metrics))}
    y_max={m_i: -1 for m_i in range(len(focused_metrics))}
    for world_size, world in WORLDS: 
        short_world = world.replace('_WORLD', '')
        fig, ax = plt.subplots(len(INITIALIZATIONS),len(focused_metrics))
        for i, initialization_pair in enumerate(INITIALIZATIONS):
            for utility, utility_marker, line_data in iter_line(world, world_size, initialization_pair):
                for m_i, metric in enumerate(focused_metrics):
                    y = [line_data[x][metric] for x in TYPES]
                    y_min[m_i] = min(np.min(y), y_min[m_i])
                    y_max[m_i] = max(np.max(y), y_max[m_i])
                    if utility == 'random_init':
                        ax[i, m_i].plot(TYPES, y, '--', color='black', label=utility_marker, marker='+', markersize=10)
                        ax[1-i, m_i].plot(TYPES, y, '--', color='black', label=utility_marker, marker='+', markersize=10)
                    elif utility == 'schelling_random_init':
                        ax[i, m_i].plot(TYPES, y, '-.', color='red', label=utility_marker, marker='x', markersize=10)
                    else:
                        ax[i, m_i].plot(TYPES, y, label=utility, marker=utility_marker, markersize=10)
                    ax[i, m_i].set_xticks(TYPES)
                    ax[i, m_i].set_xticklabels(TYPES)
                    ax[i, m_i].grid(color='grey', linestyle='--', linewidth=1)
            for m_i, metric in enumerate(focused_metrics):
                ax[i, m_i].set_ylim((y_min[m_i], y_max[m_i]))
        for m_i, metric in enumerate(focused_metrics):
            ax[0, m_i].set_title('%s' % legend_label_map[metric])
            ax[1, m_i].set_xlabel('Number of types')
        for i, initialization_pair in enumerate(INITIALIZATIONS):
            # plt.gcf().text(0.02, [0.75,0.25][i], initialization_pair[1].replace(' ', '\n'), fontsize=12) 
            ax[i, 0].set_ylabel('Metric')
            # ax[i, 0].set_ylabel(initialization_pair[1])
            # box_0 = ax[i,0].get_position()
            # ax[i,0].set_position([box_0.x0 * 0.9, box_0.y0, box_0.width * 0.9, box_0.height])
            # for m_i in range(len(focused_metrics)-1):
            #     box_0 = ax[i,m_i].get_position()
            #     box_1 = ax[i,m_i+1].get_position()
            #     ax[i,m_i+1].set_position([box_0.x0+box_0.width*1.2, box_1.y0, box_1.width * 0.9, box_1.height])

        handles, labels = plt.gca().get_legend_handles_labels()
        order = [0,4,1,2,3]
        plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], ncol=5, bbox_to_anchor=(0.25, -0.25))
        # ax[-1,-1].legend([handles[idx] for idx in order],[labels[idx] for idx in order], title='Legend', bbox_to_anchor=(1.0, 0.8))
        # plt.suptitle('%s' % (short_world))
        plt.show()
        # plt.savefig('avg_plots/degree4_large.png')
        # plt.close()