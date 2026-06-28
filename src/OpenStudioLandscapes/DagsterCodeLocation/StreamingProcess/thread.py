import threading
import queue
import subprocess
import shlex
from typing import Any, Generator, Union, List, Dict

from dagster import AssetExecutionContext, OpExecutionContext, get_dagster_logger

LOGGER = get_dagster_logger(__name__)


class OpenStudioLandscapesStreamingProcessException(Exception):
    pass


class _OutputReader(threading.Thread):
    def __init__(self, stream, output_queue):
        threading.Thread.__init__(self)
        self.stream = stream
        self.output_queue = output_queue

    def run(self):
        for line in iter(self.stream.readline, b""):
            self.output_queue.put(line.decode().strip())


def _execute_in_threads(
    command: str,
    env: Dict,
) -> Generator[str | Any, None, None]:
    """
    Usage


    :param command:
    :return:
    """

    # if env is None:
    #     env = {}

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    stdout_queue = queue.Queue()
    stderr_queue = queue.Queue()

    stdout_reader = _OutputReader(process.stdout, stdout_queue)
    stderr_reader = _OutputReader(process.stderr, stderr_queue)

    stdout_reader.start()
    stderr_reader.start()

    while True:
        # Todo:
        #  - [ ] could run in two threads
        while not stdout_queue.empty():
            stdout = "stdout: %s" % stdout_queue.get()
            yield stdout
        while not stderr_queue.empty():
            stderr = "stderr: %s" % stderr_queue.get()
            yield stderr

        returncode = process.poll()
        if returncode is not None:
            returncode_msg = "return code: %i" % returncode
            if returncode != 0:
                raise OpenStudioLandscapesStreamingProcessException(
                    f"Process not finished successfully. {returncode = }"
                )
            yield returncode_msg
            break


def _process_cmds(
    context: Union[OpExecutionContext, AssetExecutionContext],
    cmds: List[Dict[str, Union[List[str], Dict]]],
) -> Generator[str | Any, Any, None]:

    """
    cmds = [
        [cmd1],
        [cmd2],
    ]

    cmds = [
        {
            "cmd": [cmd1],
            "env": {},
        },
        {
            "cmd": [cmd2],
            "env": {},
        },
    ]
    """

    LOGGER.debug(f"Received cmds: {cmds}")

    cmd: Dict[str, Union[List[str], Dict]]
    for cmd in cmds:

        context.log.info(f"Processing command: \"{' '.join(cmd['cmd'])}\"")
        context.log.info(f"Environment: \"{' '.join(cmd['env'])}\"")

        for s in _execute_in_threads(
            command=shlex.join(cmd["cmd"]),
            env=cmd["env"],
        ):
            yield s
