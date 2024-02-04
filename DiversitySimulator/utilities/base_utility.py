from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph_envs.base_graph_env import Vertex


class BaseUtility(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def best_case(self, vertex: Vertex):
        pass

    @abstractmethod
    def compute(self, vertex: Vertex):
        pass