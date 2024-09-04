from __future__ import annotations
import os.path 
from pathlib import Path
import json
import copy
import numpy as np

from utilities.neighborhood_vector_metrics import SchellingSegregationUtility

from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from graph_envs.base_graph_env import BaseGraphEnvironment

ROOT = 'graph_envs/graph_inits'
Path(ROOT).mkdir(parents=True, exist_ok=True)
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


def _initialize_func(env:BaseGraphEnvironment,    
                     rs:int,
                     init_name:str,
                     init_func:Callable):
    if rs >= 0:
        loaded_world = _load_init(env, init_name, rs)
        if not loaded_world:
            np.random.seed(seed=rs)
            init_func()
            _save_init(env, init_name, rs)
    else:
        init_func()


def random_init(env:BaseGraphEnvironment, rs:int =-1):
    '''
        Random type assignment in the world.
    '''

    def init_func(): 
        env.world = np.random.choice(env.num_types, env.world_size)
    _initialize_func(env, rs, 'random_init', init_func)
    # if rs >= 0:
    #     loaded_world = _load_init(env, 'random_init', rs)
    #     if not loaded_world:
    #         np.random.seed(seed=rs)
    #         init_func()
    #         _save_init(env, 'random_init', rs)
    # else:
    #     init_func()


def equitable_init(env: BaseGraphEnvironment, rs:int = -1):
    '''
        Equitable initialization of the type in the world.
    '''
    def init_func(): 
        world_size = np.prod(env.world_size)
        world = np.zeros(world_size, dtype=int)
        loc_order = np.random.permutation(np.arange(world_size))
        current_type = 0
        for loc in loc_order:
            world[loc] = current_type
            if current_type == env.num_types - 1:
                current_type = 0
            else:
                current_type += 1
        env.world = np.reshape(world, env.world_size)
    _initialize_func(env, rs, 'equitable_init', init_func)


def _schelling_segregation_init(env: BaseGraphEnvironment, rs:int, 
                                rand_func:Callable):
    def init_func():
        rand_func(env, rs)
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
    _initialize_func(env, rs, 'schelling_segregation_%s'%rand_func.__name__, init_func)
    
    # if rs >= 0:
    #     loaded_world = _load_init(env, 'schelling_segregation_init', rs)
    #     if not loaded_world:
    #         init_func()
    #         _save_init(env, 'schelling_segregation_init', rs)
    # else:
    #     init_func()


def schelling_segregation_random_init(env: BaseGraphEnvironment, rs:int=-1):
    '''
        Schelling segregation initialization with randomly assigned type. 
    '''
    return _schelling_segregation_init(env, rs, random_init)


def schelling_segregation_equitable_init(env: BaseGraphEnvironment, rs:int=-1):
    '''
        Schelling segregation initialization with randomly assigned type. 
    '''
    return _schelling_segregation_init(env, rs, equitable_init)