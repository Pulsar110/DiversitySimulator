import json
import glob
import numpy as np
import matplotlib.pyplot as plt

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
plt.rcParams['xtick.labelsize'] = 8

results = {}
for result_file in glob.glob('results/*/*.json'):
    world = result_file.split('_WORLD')[0]
    utility = result_file.split('WORLD')[1].split('_')[1].split('Div')[0].split('Uti')[0]
    if world not in results:
        results[world] = {}
    with open(result_file, 'r') as data_file:
        results[world][utility] = json.load(data_file)

for world in results.keys():
    count = 0
    for i, utility in enumerate(results[world].keys()):
        for j, metric in enumerate(results[world][utility]["0"]['final'].keys()):
            if isinstance(results[world][utility]["0"]['final'][metric], list):
                for k in range(len(results[world][utility]["0"]['final'][metric])):
                    y = [results[world][utility][str(run)]['final'][metric][k] for run in range(10)]
                    x = [count] * len(y)
                    count += 1
                    if i == 0:
                        plt.scatter(x, y, c=colors[j], alpha=1-k*0.2, label='%s_%d' % (metric, k))
                    else:
                        plt.scatter(x, y, c=colors[j], alpha=1-k*0.2)
            else:
                y = [results[world][utility][str(run)]['final'][metric] for run in range(10)]
                x = [count] * len(y)
                count += 1
                if i == 0:
                    plt.scatter(x, y, c=colors[j], label=metric)
                else:
                    plt.scatter(x, y, c=colors[j])
        plt.vlines(count, 0, 1, color='black')
        count += 1
    plt.legend()
    block = count//len(results[world])
    plt.xticks(range(block//2-1, count, block), results[world].keys())
    plt.savefig('%s.png' % world)
    plt.close()