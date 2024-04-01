from __future__ import annotations
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment


def random_init(env: BaseGraphEnvironment):
    '''
        Random type assignment in the world.
    '''
    return np.random.choice(env.num_types, env.world_size)


def block_init(env: BaseGraphEnvironment):
    '''
        Assign the types in blocks.
    '''
    block_size = env.world_size[0] // env.num_types
    world = np.zeros(env.world_size)
    current_type = 1
    for i in range(block_size, env.world_size[0], block_size):
        world[i:i+block_size] = current_type
        current_type += 1
    world[i:] = current_type - 1
    return world
    