from dataclasses import dataclass
from typing import List, Dict, Optional
import sys
from owl.tasks import load_module


@dataclass
class Params:
    positional: List[str] = []
    named: Dict[str, str] = {}


def parse_args(argv: List[str]):
    params = Params()
    named_arg: Optional[str] = None
    for arg in argv:
        if not arg.startswith("--"):
            params.positional.append(arg)


def load_tasks():
    import tasks

    cl = load_module("tasks", tasks)
