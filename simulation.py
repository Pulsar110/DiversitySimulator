import numpy as np 
import matplotlib.pyplot as plt
import copy

class Simulator:

### 
	def __init__(self, num_colors, world_size):
		self.world_size = world_size
		self.num_colors = num_colors
		self.world = np.random.choice(num_colors, world_size)
		self.swapped = 0

### location is a number in the world, the function gets its corresponding indices
	def __get_index(self, location):						
		l = len(self.world_size)
		loc_idx = np.zeros(l)

		for i in range(l-1):
			cur_size = np.prod( self.world_size[i+1:])
			loc_idx[i] = location // cur_size
			location = location % cur_size
		loc_idx[-1] = location
		return loc_idx


### randomly pick num_loc many locations
	def __random_pick_locations(self, num_loc):
		chosen_locations = np.random.choice(np.prod(self.world_size), num_loc, replace=False)
		return [list(map(int, self.__get_index(location))) for location in chosen_locations] 

### get the color of the location via loc_idx
	def __get_color(self, loc_idx):
		color = self.world
		for idx in loc_idx:
			color = color[idx]
		return color




### set given_color at loc_idx
	def __set_color(self, given_color, loc_idx):
		color = self.world
		for idx in loc_idx[:-1]:
			color = color[idx]
		color[loc_idx[-1]] = given_color




### calculate the array of colors in the open neighborhood of the location at loc_idx
	def __get_colors_in_open_nbhd(self, loc_idx):
		color_array = []
		for i, idx in enumerate(loc_idx):
			cur_idx = copy.copy(loc_idx)

			if idx + 1 == self.world_size[i]:
				cur_idx[i] = 0
			else: 
				cur_idx[i] = idx + 1

			color_array.append(self.__get_color(cur_idx))

			if idx == 0:
				cur_idx[i] = self.world_size[i] - 1
			else: 
				cur_idx[i] = idx - 1

			color_array.append(self.__get_color(cur_idx))

		return color_array
		





### calculate the utility at the location given by loc_idx with the given_color
### Def of utility:  distinct number of colors in the set consisting of the given_color and the colors in the open neighborhood of loc_idx.
	def __utility(self, loc_idx, given_color):
		color_array = self.__get_colors_in_open_nbhd(loc_idx)
		color_array.append(given_color)
		print('loc=', loc_idx, 'color=', given_color, 'color_array=', color_array, 'utility=', len(set(color_array)))
		return len(set(color_array))
		



### swap the colors at two locations if both improve their utilities
	def __swap(self, loc_1, loc_2):
		color_1 = self.__get_color(loc_1)
		color_2 = self.__get_color(loc_2)
		u_1_at_1 = self.__utility(loc_1, color_1)
		u_1_at_2 = self.__utility(loc_2, color_1)
		u_2_at_2 = self.__utility(loc_2, color_2)
		u_2_at_1 = self.__utility(loc_1, color_2)

		if (u_1_at_2 > u_1_at_1) and (u_2_at_1 > u_2_at_2):
			print('swaped!',loc_1, ' with ', loc_2)
			self.__set_color(color_1, loc_2)
			self.__set_color(color_2, loc_1)
			self.swapped = 1

		if self.swapped == 1:
			print('u_1_at_1 =', u_1_at_1)
			print('u_1_at_2 =', u_1_at_2)
			print('u_2_at_2 =', u_2_at_2)
			print('u_2_at_1 =', u_2_at_1)
			print(self.world)


	def run(self， steps):
		i=0
		while i < steps: 
			loc_idx_s = sim.__random_pick_locations(2)
			#print(loc_idx_s)
			self.__swap(loc_idx_s[0],loc_idx_s[1])
			i += 1
			if self.swapped == 1:
				break

	


if __name__ == '__main__':
	num_colors = 2
	world_size = [200]
	sim = Simulator(num_colors, world_size)
	print(sim.world)
	sim.run(100)