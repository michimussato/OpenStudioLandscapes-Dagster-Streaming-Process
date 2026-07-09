from typing import Union, List, Dict

from dagster import AssetExecutionContext, OpExecutionContext, get_dagster_logger

from OpenStudioLandscapes.DagsterCodeLocation.StreamingProcess.thread import _process_cmds

LOGGER = get_dagster_logger(__name__)


def submit_cmds(
    context: Union[OpExecutionContext, AssetExecutionContext],
    cmds: List[Dict[str, Union[List[str], Dict]]],
) -> List[str]:
    """
    Args:
        context: Union[OpExecutionContext, AssetExecutionContext]
        cmds: list of commands to execute

    Returns:
        list[str]: all collected records (stdout, stderr, return code)
    """

    records = []

    # Todo:
    #  - [ ] in case of exception, return `records` until that point
    #        instead of cashing and not returning anything

    for record in _process_cmds(
        context=context,
        cmds=cmds,
    ):
        context.log.info(record)
        records.append(record)

    return records