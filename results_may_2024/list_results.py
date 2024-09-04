import json
import numpy as np
import matplotlib.pyplot as plt

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
plt.rcParams['xtick.labelsize'] = 8

alpha_rate = 0.1

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

ROOT = 'results/6_types'
# WORLDS = ['CIRCLE_WORLD', 'CYLINDER_WORLD', 'GRID_4DEG_WORLD', 'GRID_8DEG_WORLD']
WORLDS = ['GRID_8DEG_WORLD']
UTILITIES = ['BinaryDiversityUtility', 'TypeCountingDiversityUtility', 'DifferenceCountDiversityUtility', 'EntropyDivertiyUtility']
INITIALIZATIONS = ['random_init', 'shelling_init'] #'block_init', 
SWAP_CONDS = ['individual_greater'] #, 'individual_no_worse', 'sum_greater']

print('Social welfare contains, in order: Binary, Type Counting, Difference Counting, Entropy')
print('Degree of intergration order: DIO_1, DIO_2, ...')

for world in WORLDS:
    print(world)
    for initialization in INITIALIZATIONS:
        for swap_cond in SWAP_CONDS:
            print('Initialization: %s; Swap Condition: %s' % (initialization, swap_cond))
            results = {'difference(final-init)': {}, 'final': {}, 'init':{}, 'steps': {}}
            dir_path = '%s_%s_%s' % (world, initialization, swap_cond)
            for utility in UTILITIES:
                short_label = utility.replace('DiversityUtility', '')
                results['difference(final-init)'][short_label] = {}
                results['final'][short_label] = {}
                results['init'][short_label] = {}
                with open('%s/%s_%s_results_.json' % (ROOT, dir_path, utility), 'r') as jsonfile:
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
                        results[label][short_label][k] = sub_data
                        mean_metrics = np.mean(sub_data, axis=0)
                        if isinstance(mean_metrics, np.ndarray):
                            mean_metrics = ','.join(list(map(str, mean_metrics)))
                        print('%s: %s' % (label, mean_metrics))
                # add percentage_of_segregated_verticies
                init = 1 - np.array([d['init']['degree_of_intergration'][0] for d in data.values()])
                final = 1 - np.array([d['final']['degree_of_intergration'][0] for d in data.values()])
                results['difference(final-init)'][short_label]['percentage_of_segregated_verticies'] = final - init
                results['final'][short_label]['percentage_of_segregated_verticies'] = final
                results['init'][short_label]['percentage_of_segregated_verticies'] = init
            
            # Plot graph 
            for label in ['difference(final-init)', 'final', 'init']:
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
                                    plt.scatter(x, y, c=colors[j], alpha=1-k*alpha_rate, s=10,
                                                label=legend_label_map['%s_%d' % (metric, k)])
                                else:
                                    plt.scatter(x, y, c=colors[j], alpha=1-k*alpha_rate, s=10)
                                plt.scatter([x[0]], [np.mean(y)], color=colors[j], alpha=1-k*alpha_rate, s=60)
                                min_y = min(np.min(y), min_y)
                                max_y = max(np.max(y), max_y)
                        else:
                            y = results[label][utility][metric]
                            x = [count] * len(y)
                            count += 1
                            if i == 0:
                                plt.scatter(x, y, c=colors[j], label=legend_label_map[metric], s=10)
                            else:
                                plt.scatter(x, y, c=colors[j], s=10)
                            plt.scatter([x[0]], [np.mean(y)], c=colors[j], s=60)
                            min_y = min(np.min(y), min_y)
                            max_y = max(np.max(y), max_y)
                    plt.vlines(count, min_y, max_y, color='black')
                    count += 1
                if label == 'init':
                    plt.legend()
                block = count//len(results[label])
                mean_steps = [np.mean(results['steps'][u]) for u in results[label].keys()]
                mean_steps = ', '.join(list(map(lambda x:'%.2f'%(x), mean_steps)))
                plt.title('%s %s %s\n%s, mean steps: %s' % (world, initialization, swap_cond, label, mean_steps))
                plt.xticks(range(block//2-1, count, block), results[label].keys())
                plt.savefig('%s/plots/%s_%s.png' % (ROOT, dir_path, label))
                plt.close()
