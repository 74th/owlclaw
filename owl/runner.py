import os
import subprocess
from typing import List, Union
import colored


class Result:
    def __init__(self, process: subprocess.CompletedProcess):
        self.process = process

    @property
    def ok(self) -> bool:
        return self.process.returncode == 0

    @property
    def failed(self) -> bool:
        return self.process.returncode != 0

    @property
    def stdout(self)->Union[str, None]:
        return self.process.stdout

    @property
    def stderr(self)->Union[str, None]:
        return self.process.stderr

    @property
    def stdout_lines(self)->List[str]:
        if self.process.stdout is None:
            return []
        stdout: str = self.process.stdout
        return stdout.splitlines()

    @property
    def stderr_lines(self)->List[str]:
        if self.process.stderr is None:
            return []
        stderr: str = self.process.stdout
        return stderr.splitlines()

class Runner:
    def __init__(
        self,
        cmd: Union[str, List[str]],
        cwd: List[str],
        base_cwd: str,
    ):
        self.base_cwd = base_cwd
        self.cmd = cmd
        self.cwd = cwd

    def __print_cmd(self):
        p = ""
        if self.cwd:
            p += "cd " + os.path.join(*self.cwd) + " && "
        if isinstance(self.cmd, str):
            p += self.cmd
        else:
            for arg in self.cmd:
                p += arg.replace('"', '\\"')
        print(colored.attr("bold") + p + colored.attr("reset"))

    def __get_cwd(self) -> str:
        return os.path.join(self.base_cwd, *self.cwd)

    def run(self)-> Result:

        self.__print_cmd()

        process = subprocess.run(
            args=self.cmd,
            cwd=self.__get_cwd(),
            check=True,
            text=True,
            capture_output=True,
            shell=True,
        )
        return Result(process)
