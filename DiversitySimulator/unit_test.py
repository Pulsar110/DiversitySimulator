from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import TypeCountUtility
from dynamics.swap import RandomSwapper

world = GridWorld([5,5], 
                  num_types=4, 
                  utility_func=TypeCountUtility,
                  dynamics=RandomSwapper(),
                  verbosity=1)
print(world.world)

for i in range(100):
    changed = world.step()
    print('Swapped =', changed)