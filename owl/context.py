from __future__ import annotations

from subprocess import run
from typing import Union, List
import itertools
import os
from .runner import Runner, Result


class NoSuchDirectoryException(Exception):
    def __init__(self, path: str):
        super().__init__(self)
        self.path = path
        self.message = f"No such directory {path}"

    def __str__(self) -> str:
        return self.message


class context:

    def _exit_directory(self):
        pass

class EnterDirectoryContext:
    def __init__(self, c: context):
        self.context = c

    def __enter__(self)->EnterDirectoryContext:
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.context._exit_directory()


class Context(context):
    def __init__(self):
        self.__cwd = os.getcwd()
        self.__base_cwd = os.getcwd()
        self.__enter_directories: List[List[str]] = []

    @property
    def cwd(self):
        return self.__cwd

    def run(self, cmd: Union[str, List[str]]) -> Result:
        runner = Runner(
            cmd=cmd,
            cwd=list(itertools.chain.from_iterable(self.__enter_directories)),
            base_cwd=self.__base_cwd,
        )
        return runner.run()

    def cd(self, directory: Union[str, List[str]]) -> EnterDirectoryContext:
        if isinstance(directory, str):
            d = os.path.join(self.__cwd, directory)
        else:
            d = os.path.join(self.__cwd, *directory)
        if not os.path.exists(d):
            raise NoSuchDirectoryException(d)

        if isinstance(directory, str):
            self.__enter_directories.append([directory])
        else:
            self.__enter_directories.append(directory)

        self.__set_cwd()
        return EnterDirectoryContext(self)

    def __set_cwd(self):
        paths: List[str] = []
        for d in self.__enter_directories:
            if isinstance(d, str):
                paths.append(d)
            else:
                paths.append(*d)
        self.__cwd = os.path.join(self.__base_cwd, *paths)
        os.chdir(self.__cwd)

    def _exit_directory(self):
        self.__enter_directories.pop()
        self.__set_cwd()
