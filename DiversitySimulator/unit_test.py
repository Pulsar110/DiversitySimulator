from configs import CYLINDER_WORLD, GRID_4DEG_WORLD

# world = CYLINDER_WORLD(10)
world = GRID_4DEG_WORLD([20,20])
print(world.world)
world.compute_metric_summary(print_results=True)
world.visualize(200)
# for i in range(100):
#     changed = world.step()
#     if changed:
#         print('Swapped =', changed)
world.compute_metric_summary(print_results=True)

v = world.get_vertex([0,0])
v.neigh_type_vector = world.get_neighborhood_type_vector(v)
print(v)

print('DONE!')