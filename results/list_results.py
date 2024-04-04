import json
import numpy as np
import matplotlib.pyplot as plt

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
plt.rcParams['xtick.labelsize'] = 8

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

ROOT = 'results/'
# WORLDS = [CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD]
WORLDS = ['CIRCLE_WORLD']
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 'DifferenceCountDiversityUtility', 'EntropyDivertiyUtility']
#UTILITIES = [EntropyDivertiyUtility]
INITIALIZATIONS = ['random_init', 'block_init', 'shelling_init']
SWAP_CONDS = ['individual_greater', 'individual_no_worse', 'sum_greater']

print('Social welfare contains, in order: Binary, Type Counting, Difference Counting, Entropy')
print('Degree of intergration order: DIO_1, DIO_2, ...')

for world in WORLDS:
    print(world)
    for initialization in INITIALIZATIONS:
        for swap_cond in SWAP_CONDS:
            print('Initialization: %s; Swap Condition: %s' % (initialization, swap_cond))
            results = {'difference(final-init)': {}, 'final': {}, 'steps': {}}
            dir_path = '%s/%s/%s' % (ROOT, initialization, swap_cond)
            for utility in UTILITIES:
                short_label = utility.replace('DiversityUtility', '')
                results['difference(final-init)'][short_label] = {}
                results['final'][short_label] = {}
                with open('%s/%s_%s_results_.json' % (dir_path, world, utility), 'r') as jsonfile:
                    data = json.load(jsonfile)
                results['steps'][short_label] = [d['steps'] for d in data.values()]
                mean_steps = np.mean([d['steps'] for d in data.values()])
                print('Average number of steps until conversion:', mean_steps)
                for k in data['0']['init'].keys():
                    print('Metric', k)
                    for label in ['final', 'init']:
                        sub_data = np.array([d[label][k] for d in data.values()])
                        if label == 'init':
                            results['difference(final-init)'][short_label][k] = (results['final'][short_label][k] - sub_data)
                        else:
                            results[label][short_label][k] = sub_data
                        mean_metrics = np.mean(sub_data, axis=0)
                        if isinstance(mean_metrics, np.ndarray):
                            mean_metrics = ','.join(list(map(str, mean_metrics)))
                        print('%s: %s' % (label, mean_metrics))
                # add percentage_of_segregated_verticies
                init = np.array([d['init']['degree_of_intergration'][0] for d in data.values()])
                final = np.array([d['final']['degree_of_intergration'][0] for d in data.values()])
                results['difference(final-init)'][short_label]['percentage_of_segregated_verticies'] = final - init
                results['final'][short_label]['percentage_of_segregated_verticies'] = final
            
            # Plot graph 
            for label in ['difference(final-init)', 'final']:
                count = 0
                min_y = 0
                max_y = 1
                for i, utility in enumerate(results[label].keys()): 
                    for j, metric in enumerate(results[label][utility].keys()):
                        if len(results[label][utility][metric].shape) > 1:
                            for k in range(results[label][utility][metric].shape[-1]):
                                y = results[label][utility][metric][:,k]
                                x = [count] * len(y)
                                count += 1
                                if i == 0:
                                    plt.scatter(x, y, c=colors[j], alpha=1-k*0.2, 
                                                label=legend_label_map['%s_%d' % (metric, k)])
                                else:
                                    plt.scatter(x, y, c=colors[j], alpha=1-k*0.2)
                                min_y = min(np.min(y), min_y)
                                max_y = max(np.max(y), max_y)
                        else:
                            y = results[label][utility][metric]
                            x = [count] * len(y)
                            count += 1
                            if i == 0:
                                plt.scatter(x, y, c=colors[j], label=legend_label_map[metric])
                            else:
                                plt.scatter(x, y, c=colors[j])
                            min_y = min(np.min(y), min_y)
                            max_y = max(np.max(y), max_y)
                    plt.vlines(count, min_y, max_y, color='black')
                    count += 1
                plt.legend()
                block = count//len(results[label])
                plt.title('%s %s %s\n%s, mean steps: %.2f' % (world, initialization, swap_cond, label, 
                                                              np.mean(results['steps'][utility])))
                plt.xticks(range(block//2-1, count, block), results[label].keys())
                plt.savefig('%s/%s_%s_%s_%s.png' % (dir_path, world, initialization, swap_cond, label))
                plt.close()