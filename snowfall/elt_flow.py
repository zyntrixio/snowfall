"""ELT flow."""
from prefect import flow
from prefect.blocks.system import String
from prefect_airbyte.connections import trigger_sync
from prefect_dask.task_runners import DaskTaskRunner

from snowfall.tasks.get_dbt_cli_profile import get_dbt_cli_profile
from snowfall.tasks.trigger_dbt_task import dbt_cli_task


@flow(name="ELT_Extractions", task_runner=DaskTaskRunner)
def trigger_extractions() -> None:
    """Trigger the extractions."""
    copybot_output = trigger_sync.submit(
        airbyte_server_host=String.load("airbyte-ip").value,
        airbyte_server_port=String.load("airbyte-port").value,
        connection_id=String.load("airbyte-snowstorm-connection").value,
        poll_interval_s=3,
        status_updates=True,
    )
    trigger_sync.submit(
        airbyte_server_host=String.load("airbyte-ip").value,
        airbyte_server_port=String.load("airbyte-port").value,
        connection_id=String.load("airbyte-hermes-connection").value,
        poll_interval_s=3,
        status_updates=True,
        wait_for=[copybot_output],
    )
    trigger_sync.submit(
        airbyte_server_host=String.load("airbyte-ip").value,
        airbyte_server_port=String.load("airbyte-port").value,
        connection_id=String.load("airbyte-harmonia-connection").value,
        poll_interval_s=3,
        status_updates=True,
        wait_for=[copybot_output],
    )


@flow(name="ELT_Flow")
def run(
    env: str,
    is_trigger_extractions: bool = True,
    is_run_source_tests: bool = True,
    is_run_transformations: bool = True,
    is_run_output_tests: bool = True,
) -> None:
    """Run the ELT flow.

    Args:
        env (str): The environment.
        is_trigger_extractions (bool, optional): Whether to trigger extractions. Defaults to True.
        is_run_source_tests (bool, optional): Whether to run source tests. Defaults to True.
        is_run_transformations (bool, optional): Whether to run transformations. Defaults to True.
        is_run_output_tests (bool, optional): Whether to run output tests. Defaults to True.
    """
    if is_trigger_extractions:
        trigger_extractions()
    dbt_cli_profile = get_dbt_cli_profile(env)
    dbt_cli_task(dbt_cli_profile, "dbt deps")
    if is_run_source_tests:
        dbt_cli_task(dbt_cli_profile, "dbt test --select tag:source")
    if is_run_transformations:
        dbt_cli_task(dbt_cli_profile, "dbt run")
    if is_run_output_tests:
        dbt_cli_task(dbt_cli_profile, 'dbt test --exclude tag:"source" tag:"business"')
        dbt_cli_task(dbt_cli_profile, "dbt test --select tag:business")
