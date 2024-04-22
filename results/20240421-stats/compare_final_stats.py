import json
import numpy as np
import csv

legend_label_map = {
    'social_welfare_0': 'soc. wel. (Binary)',
    'social_welfare_1': 'soc. wel. (TypeCount)',
    'social_welfare_2': 'soc. wel. (DiffCount)',
    'social_welfare_3': 'soc. wel. (Entropy)',
    'degree_of_intergration_0': 'DIO_1',
    'degree_of_intergration_1': 'DIO_2',
    'degree_of_intergration_2': 'DIO_3',
    'degree_of_intergration_3': 'DIO_4',
    'degree_of_intergration_4': 'DIO_5',
    'degree_of_intergration_5': 'DIO_6',
    'degree_of_intergration_6': 'DIO_7',
    'degree_of_intergration_7': 'DIO_8',
    'percentage_of_segregated_verticies': '% of seg. vertices',
    'number_of_colorful_edges': '# colorful edges'
}

ROOT = 'results'
TYPES = [3,6,7]
WORLDS = ['CIRCLE_WORLD', 'CYLINDER_WORLD', 'GRID_4DEG_WORLD', 'GRID_8DEG_WORLD']
# WORLDS = ['GRID_8DEG_WORLD']
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 'DifferenceCountDiversityUtility', 'EntropyDivertiyUtility']
INITIALIZATIONS = ['random_init', 'shelling_init'] #'block_init', 
SWAP_CONDS = ['individual_greater'] #, 'individual_no_worse', 'sum_greater']

focused_metrics = ['social_welfare_3', 'number_of_colorful_edges']
focused_metrics_is_max = list(map(lambda x: 'Is max (%s)' % x, focused_metrics))


def iter_graphs():
    for world in WORLDS:
        for num_type in TYPES:
            for initialization in INITIALIZATIONS:
                yield world, num_type, initialization
                # for utility in UTILITIES:
                #     for swap_cond in SWAP_CONDS:
                #         yield world, num_type, initialization, utility, swap_cond

results = {}

# for world, num_type, initialization, utility, swap_cond in iter_graphs():
for world, num_type, initialization in iter_graphs():
    for utility in UTILITIES:
        swap_cond = SWAP_CONDS[0]
        with open('%s/%d_types/%s_%s_%s_%s_results_.json' % (ROOT, 
                                                             num_type,
                                                             world, 
                                                             initialization, 
                                                             swap_cond, 
                                                             utility), 'r') as jsonfile:
            data = json.load(jsonfile)
        short_utility = utility.replace('DiversityUtility', '')
        metrics = {}
        for k in data['0']['final'].keys():
            k_label = k
            sub_data = []
            if isinstance(data['0']['final'][k], list):
                for i in range(len(data['0']['final'][k])):
                    if '%s_%d' % (k, i) in focused_metrics:
                        k_label = '%s_%d' % (k, i)
                        sub_data = np.array([d['final'][k][i] for d in data.values()])
            elif k in focused_metrics:
                sub_data = np.array([d['final'][k] for d in data.values()])
            if len(sub_data) == 0:
                continue
            mean_metrics = np.mean(sub_data, axis=0)
            metrics[k_label] = mean_metrics
        steps = np.mean([d['steps'] for d in data.values()])
        results[(world, num_type, initialization, utility)] = {'val': [str(metrics[k]) for k in focused_metrics],
                                                               'is_max': ['0' for _ in focused_metrics],
                                                               'steps': str(steps)}

    for i in range(len(focused_metrics)):
        vals = [results[(world, num_type, initialization, u)]['val'][i] for u in UTILITIES]
        arg_max = np.argmax(vals)
        results[(world, num_type, initialization, UTILITIES[arg_max])]['is_max'][i] = '1'


filename = '-AND-'.join(focused_metrics)
with open('%s/20240421-stats/%s.csv' % (ROOT, filename), 'w') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(['GRID DEGREE', 
                         'NUM TYPES', 
                         'INITIALIZATION',
                         'UTILITY',
                         # 'SWAP CONDITION',
                         'STEPS']+focused_metrics+focused_metrics_is_max)
    for world, num_type, initialization in iter_graphs():  
        for utility in UTILITIES:
            metrics = results[(world, num_type, initialization, utility)]['val']
            is_max = results[(world, num_type, initialization, utility)]['is_max']
            steps = results[(world, num_type, initialization, utility)]['steps']
            spamwriter.writerow([world, num_type, initialization] + [utility, steps] + metrics + is_max)





