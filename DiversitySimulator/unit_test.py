from graph_envs.grid import GridWorld
from utilities.neighborhood_vector_metrics import type_counting_diversity_utility
from dynamics.swap import RandomSwapper

world = GridWorld([13,13], 
                  num_types=3,
                  neigh_radius=2,
                  vertex_degree=4, 
                  wrapped_indices=[True, True],
                  utility_func=type_counting_diversity_utility,
                  dynamics=RandomSwapper(),
                  verbosity=1)
print(world.world)

# for i in range(100):
#     changed = world.step()
#     if changed:
#         print('Swapped =', changed)

v = world.get_vertex([0,0])
v.neigh_type_vector = world.get_neighborhood_type_vector(v)
print(v)
