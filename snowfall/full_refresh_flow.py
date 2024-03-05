"""Full Refresh Flow."""
from prefect import flow

from snowfall.tasks.get_dbt_cli_profile import get_dbt_cli_profile
from snowfall.tasks.trigger_dbt_task import dbt_cli_task


@flow(name="Full_Refresh_Flow")
def run(
    env: str,
    is_run_transformations: bool = True,
    is_run_output_tests: bool = True,
) -> None:
    """Run the full refresh flow.

    Args:
        env (str): The environment.
        is_run_transformations (bool): Flag indicating whether to run transformations.
        is_run_output_tests (bool): Flag indicating whether to run output tests.
    """
    dbt_cli_profile = get_dbt_cli_profile(env)
    dbt_cli_task(dbt_cli_profile, "dbt deps")
    if is_run_transformations:
        dbt_cli_task(dbt_cli_profile, "dbt run --full-refresh")
    if is_run_output_tests:
        dbt_cli_task(dbt_cli_profile, 'dbt test --exclude tag:"source" tag:"business"')
        dbt_cli_task(dbt_cli_profile, "dbt test --select tag:business")