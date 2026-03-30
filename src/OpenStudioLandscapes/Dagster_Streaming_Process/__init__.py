from typing import Union, List

from dagster import AssetExecutionContext, OpExecutionContext, get_dagster_logger

from OpenStudioLandscapes.Dagster_Streaming_Process.thread import _process_cmds

LOGGER = get_dagster_logger(__name__)


def submit_cmds(
    context: Union[OpExecutionContext, AssetExecutionContext],
    cmds: List[List[str]],
) -> List[str]:
    """
    Args:
        context: Union[OpExecutionContext, AssetExecutionContext]
        cmds: list of commands to execute

    Returns:
        list[str]: all collected records (stdout, stderr, return code)
    """

    records = []

    for record in _process_cmds(
        context=context,
        cmds=cmds,
    ):
        context.log.info(record)
        records.append(record)

    return records