"""Trigger DBT command task."""
from prefect_dbt.cli.commands import trigger_dbt_cli_command


def dbt_cli_task(dbt_cli_profile, command) -> None:  # noqa: ANN001
    """Run a dbt CLI command.

    Args:
        dbt_cli_profile: The dbt CLI profile.
        command: The dbt CLI command to run.
    """
    return trigger_dbt_cli_command(
        command=command,
        overwrite_profiles=True,
        profiles_dir="/app/data-warehouse/Prefect",
        project_dir="/app/data-warehouse/Bink",
        dbt_cli_profile=dbt_cli_profile,
    )
