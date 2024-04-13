from __future__ import annotations
import os.path 
import json
import copy
import numpy as np

from utilities.neighborhood_vector_metrics import SchellingSegregationUtility

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment

ROOT = 'DiversitySimulator/graph_envs/graph_inits'
GRAPH = {}
FILE_PATH = ''


def _get_init_file_path(env: BaseGraphEnvironment):
    world_size = env.world_size
    if isinstance(world_size, int):
        world_size = (world_size,)
    file_path = '%s/%d-types_size-%s.json' % (ROOT, env.num_types, 
                                              '-'.join(list(map(str, world_size))))
    return file_path


def _load_init(env: BaseGraphEnvironment, init_type:str, rs:int):
    global GRAPH
    global FILE_PATH
    file_path = _get_init_file_path(env)
    if FILE_PATH != file_path:
        FILE_PATH = file_path
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r') as json_data:
                GRAPH = json.load(json_data)
        else:
            GRAPH = {}

    if rs in GRAPH:
        if init_type in GRAPH[rs]:
            env.world = np.array(copy.deepcopy(GRAPH[rs][init_type]))
            return True
    return False


def _save_init(env: BaseGraphEnvironment, init_type:str, rs:int):
    '''
        Should always be called after _load_init.
    '''
    if rs not in GRAPH:
        GRAPH[rs] = {}
    if init_type not in GRAPH[rs]:
        GRAPH[rs][init_type] = copy.deepcopy(env.world.tolist())
        with open(FILE_PATH, 'w') as json_data:
            json.dump(GRAPH, json_data)


def random_init(env: BaseGraphEnvironment, rs:int =-1):
    '''
        Random type assignment in the world.
    '''

    def init_func(): 
        env.world = np.random.choice(env.num_types, env.world_size)

    if rs >= 0:
        loaded_world = _load_init(env, 'random_init', rs)
        if not loaded_world:
            np.random.seed(seed=rs)
            init_func()
            _save_init(env, 'random_init', rs)
    else:
        init_func()


def block_init(env: BaseGraphEnvironment, rs:int = -1):
    '''
        Assign the types in blocks.

        NOT WORKING!
    '''
    def init_func():
        block_size = env.world_size[0] // env.num_types
        world = np.zeros(env.world_size, dtype=int)
        current_type = 1
        for i in range(block_size, env.world_size[0]-block_size, block_size):
            world[i:i+block_size] = current_type
            current_type += 1
        world[i:] = current_type - 1
        env.world = world

    loaded_world = _load_init(env, 'block_init', 0)
    if not loaded_world:
        init_func()
        _save_init(env, 'block_init', 0)


def schelling_segregation_init(env: BaseGraphEnvironment, rs:int = -1):
    '''
        Run Schelling segregation. 
    '''

    def init_func():
        random_init(env, rs)
        utility = env.utility
        # dynamics = env.dynamics
        env.utility = SchellingSegregationUtility()
        # env.dynamics = UtilityOrderedSwapper(INDIVIDUAL_GREATER)
        while env.step():
            pass
            # print(env.done)
        env.done = False
        env.utility = utility
        # env.dynamics = dynamics
        
    if rs >= 0:
        loaded_world = _load_init(env, 'schelling_segregation_init', rs)
        if not loaded_world:
            init_func()
            _save_init(env, 'schelling_segregation_init', rs)
    else:
        init_func()
