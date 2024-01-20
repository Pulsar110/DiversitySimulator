from configs import CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD

from utilities.neighborhood_vector_metrics import schelling_segregation_utility
from dynamics.swap import UtilityOrderedSwapper, INDIVIDUAL_GREATER


def schelling_segregation_init(env):
    '''
        Run Schelling segregation. 
    '''
    utility_func = env.utility_func
    dynamics = env.dynamics
    env.utility_func = schelling_segregation_utility
    env.dynamics = UtilityOrderedSwapper(INDIVIDUAL_GREATER)
    while env.step():
        print(env.done)
    env.done = False
    env.utility_func = utility_func
    env.dynamics = dynamics

for i in range(10):
    world = CYLINDER_WORLD(40)
    # world = GRID_4DEG_WORLD([20,20], verbosity=1)
    print(world.world)
    world.compute_metric_summary(print_results=True)
    schelling_segregation_init(world)
    world.visualize(200, 'results/cylinder/CYLINDER_WORLD_40_type_counting_INDIVIDUAL_NO_WORSE_%d'%i)
    # for i in range(100):
    #     changed = world.step()
    #     if changed:
    #         print('Swapped =', changed)
    world.compute_metric_summary(print_results=True)
    v = world.get_vertex([0,0])
    v.neigh_type_vector = world.get_neighborhood_type_vector(v)
    print(v)

    print('DONE!')