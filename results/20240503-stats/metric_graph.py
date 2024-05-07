import json
import numpy as np

import matplotlib.pyplot as plt

legend_label_map = {
    'social_welfare_0': 'soc. wel. (Binary)',
    'social_welfare_1': 'soc. wel. (TypeCount)',
    'social_welfare_2': 'soc. wel. (DiffCount)',
    'social_welfare_3': 'Entropy',
    'degree_of_intergration_0': 'DIO_1',
    'degree_of_intergration_1': 'DIO_2',
    'degree_of_intergration_2': 'DIO_3',
    'degree_of_intergration_3': 'DIO_4',
    'degree_of_intergration_4': 'DIO_5',
    'degree_of_intergration_5': 'DIO_6',
    'degree_of_intergration_6': 'DIO_7',
    'degree_of_intergration_7': 'DIO_8',
    'percentage_of_segregated_verticies': '% of seg. vertices',
    'number_of_colorful_edges': 'CE'
}

ROOT = 'results'
TYPES = [2,3,4,5,6,7,8]
WORLDS = ['CIRCLE_WORLD', 'CYLINDER_WORLD', 'GRID_4DEG_WORLD', 'GRID_8DEG_WORLD']
# WORLDS = ['GRID_8DEG_WORLD']
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 
             'DifferenceCountDiversityUtility', 'EntropyDivertiyUtility', 
             'AvgDiffTypeCountingDiversityUtility']
INITIALIZATIONS = ['random_init', 'schelling_init'] #'block_init', 
SWAP_CONDS = ['individual_greater'] #, 'individual_no_worse', 'sum_greater']

focused_metrics = ['social_welfare_3', 'number_of_colorful_edges']
focused_metrics_labels = list(map(lambda x: legend_label_map[x], focused_metrics)) +\
                         list(map(lambda x: 'Is max (%s)' % legend_label_map[x], focused_metrics))


def read_file(metric, world, initialization, utility):
    line_data = {}
    for num_type in TYPES:
        swap_cond = SWAP_CONDS[0]
        with open('%s/%d_types/%s_%s_%s_%s_results_.json' % (ROOT, 
                                                             num_type,
                                                             world, 
                                                             initialization, 
                                                             swap_cond, 
                                                             utility), 'r') as jsonfile:
            data = json.load(jsonfile)

        if metric not in data['0']['final']:
            orig_metric, axis = metric.rsplit('_', 1)
            sub_data = np.array([d['final'][orig_metric][int(axis)] for d in data.values()])
        else:
            sub_data = np.array([d['final'][metric] for d in data.values()])
        mean_metrics = np.mean(sub_data, axis=0)
        line_data[num_type] = mean_metrics
    return line_data

if True: # plot all utilities in each graph 
    def iter_graphs():
        for metric in focused_metrics:
            for world in WORLDS:
                for initialization in INITIALIZATIONS:
                    yield metric, world, initialization

    def iter_line(metric, world, initialization):
        for utility in UTILITIES:
            short_utility = utility.replace('DiversityUtility', '')
            short_utility = short_utility.replace('DivertiyUtility', '')
            line_data = read_file(metric, world, initialization, utility)
            yield short_utility, line_data

    for metric, world, initialization in iter_graphs():
        for utility, line_data in iter_line(metric, world, initialization):
            y = [line_data[x] for x in TYPES]
            plt.plot(TYPES, y, label=utility)
        world = world.replace('_WORLD', '')
        plt.xlabel('Number of types')
        plt.ylabel('Metric: %s' % legend_label_map[metric])
        plt.ylim((0.4,1))
        plt.title('%s, %s, %s' % (legend_label_map[metric], world, initialization.replace('sche', 'Sche')))
        plt.legend(title='Utility')
        plt.savefig('%s/20240503-stats/%s_%s_%s.png' % (ROOT, world, initialization, legend_label_map[metric]))
        plt.close()

if False: # plot PoA for each graph 
    def iter_graphs():
        for metric in focused_metrics:
            for utility in UTILITIES:
                for initialization in INITIALIZATIONS:
                    yield metric, utility, initialization

    def iter_line(metric, utility, initialization):
        for world in WORLDS:
            short_utility = utility.replace('DiversityUtility', '')
            short_utility = short_utility.replace('DivertiyUtility', '')
            line_data = read_file(metric, world, initialization, utility)
            yield world, short_utility, line_data

    for metric, utility, initialization in iter_graphs():
        for world, utility, line_data in iter_line(metric, utility, initialization):
            y = [1.0/line_data[x] for x in TYPES]
            world = world.replace('_WORLD', '')
            plt.plot(TYPES, y, label=world)
        plt.xlabel('Number of types')
        plt.ylabel('PoA: %s' % legend_label_map[metric])
        # plt.ylim((0.4,1))
        plt.title('%s, %s, %s' % (legend_label_map[metric], utility, initialization.replace('sche', 'Sche')))
        plt.legend(title='Graph degree')
        plt.savefig('%s/20240503-stats/PoA_%s_%s_%s.png' % (ROOT, legend_label_map[metric], utility, initialization))
        plt.close()

