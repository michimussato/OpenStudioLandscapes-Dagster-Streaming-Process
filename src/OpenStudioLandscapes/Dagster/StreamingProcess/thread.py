import threading
import queue
import subprocess
import shlex
from typing import Any, Generator, Union, List

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
) -> Generator[str | Any, None, None]:
    """
    Usage


    :param command:
    :return:
    """

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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
    cmds: List[List[str]],
) -> Generator[str | Any, Any, None]:

    for cmd in cmds:

        context.log.info(f"Processing command: \"{' '.join(cmd)}\"")

        for s in _execute_in_threads(
            command=shlex.join(cmd),
        ):
            yield s
