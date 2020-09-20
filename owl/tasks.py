from types import ModuleType
from typing import Callable, Dict, Union, List, Protocol, Any, Optional, TypeVar

from .context import Context

ARGS = TypeVar("ARGS", Context, str, int, float)


class Task:
    def __init__(self, task_function: Callable):
        self.__task_function = task_function

    def __call__(self, c: Context, *args, **kwargs):
        self.__task_function(c, *args, **kwargs)


class Collection:
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.collections: Dict[str, Collection] = {}


def load_module(name: str, module: ModuleType) -> Collection:
    c = Collection(name)
    for prop in dir(module):
        if isinstance(module.__dict__[prop], Task):
            c.tasks[prop] = module.__dict__[prop]
        if isinstance(module.__dict__[prop], Collection):
            c.collections[prop] = module.__dict__[prop]
    return c


def task(task_function: Callable, *depended_task: Callable) -> Callable:
    return Task(task_function)
