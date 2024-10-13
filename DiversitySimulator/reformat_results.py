import glob
import json 
# from zipfile import ZipFile


for filename in glob.glob('..\\results_oct_2024\\size_*\\*_types\\*_results_.json'):
	print(filename.split('\\')[-1].replace('.json', ''))
	with open(filename, 'r') as json_file:
		data = json.load(json_file)

	step_data = {}
	for i in range(len(data)):
		step_data[i] = data[str(i)]['step_world']
		del data[str(i)]['step_world']

	with open(filename.replace('_results_.json', '_results.json'), 'w') as json_file:
		json.dump(data, json_file)
	# with open(filename.replace('_results_.json', '_steps_.json'), 'w') as json_file:
	# 	json.dump(step_data, json_file)
	# with ZipFile(filename.replace('_results_.json', '_steps_.zip'), 'w') as zip_object:
	#    zip_object.write(filename.replace('_results_.json', '_steps.json'))
	# exit()