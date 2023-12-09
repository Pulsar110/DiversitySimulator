from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import TypeCountUtility
from dynamics.swap import RandomSwapper

world = GridWorld([5,5], 
                  num_types=3, 
                  utility_func=TypeCountUtility,
                  dynamics=RandomSwapper())

for i in range(15):
    world.step()