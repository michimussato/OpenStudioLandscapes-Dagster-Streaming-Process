[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

---

<!-- TOC -->
* [OpenStudioLandscapes-Dagster-StreamingProcess](#openstudiolandscapes-dagster-streamingprocess)
  * [Brief](#brief)
  * [Usage](#usage)
<!-- TOC -->

---

# OpenStudioLandscapes-Dagster-StreamingProcess

> [!NOTE]
> 
> This package was scaffolded with `dagster==1.9.11`
> 
> ```shell
> dagster project scaffold --name OpenStudioLandscapes-StreamingProcess
> git -C ./OpenStudioLandscapes-StreamingProcess init --initial-branch main
> git -C ./OpenStudioLandscapes-StreamingProcess remote add origin https://github.com/michimussato/OpenStudioLandscapes-Dagster-StreamingProcess.git
> git -C ./OpenStudioLandscapes-StreamingProcess add *
> git -C ./OpenStudioLandscapes-StreamingProcess commit -a -m "initial commit"
> git -C ./OpenStudioLandscapes-StreamingProcess push -u origin main
> ```

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

from OpenStudioLandscapes.Dagster.StreamingProcess import submit_cmds

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
