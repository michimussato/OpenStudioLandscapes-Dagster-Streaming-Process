![logo128.png](media/images/logo128.png)

---

<!-- TOC -->
* [OpenStudioLandscapes-Dagster-Streaming-Process](#openstudiolandscapes-dagster-streaming-process)
  * [Brief](#brief)
  * [Usage](#usage)
<!-- TOC -->

---

# OpenStudioLandscapes-Dagster-Streaming-Process

## Brief

A package to run a `subprocess` child process with output collection
(`stdout` and `stderr`) through a `queue.Queue` in Dagster.

## Usage

```python
from typing import Any, Generator, List, Union

from dagster import (
    OpExecutionContext,
    AssetExecutionContext
)

from OpenStudioLandscapes.Dagster.streaming_process import submit_cmds

dagster_execution_context: Union[OpExecutionContext, AssetExecutionContext]
tasks: List[List[str]] = [
  [
    "ls",
    "-al",
    "/dir/1",
  ],
]

log_records: List[str] = submit_cmds(
  context=dagster_execution_context,
  cmds=tasks,
)
```
