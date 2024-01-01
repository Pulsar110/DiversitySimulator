from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import type_counting_diversity_utility
from dynamics.swap import RandomSwapper

world = GridWorld([10,4], 
                  num_types=3,
                  window_size=1,
                  vertex_degree=4, 
                  utility_func=type_counting_diversity_utility,
                  dynamics=RandomSwapper(),
                  verbosity=1)
print(world.world)

for i in range(100):
    changed = world.step()
    if changed:
        print('Swapped =', changed)

v = world.get_vertice([2,2])
print(world.get_neighborhood_vector(v))
