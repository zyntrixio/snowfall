"""DBT CLI profile task."""
from prefect import task
from prefect_dbt.cli.configs import SnowflakeTargetConfigs
from prefect_dbt.cli.credentials import DbtCliProfile
from prefect_snowflake.credentials import SnowflakeCredentials
from prefect_snowflake.database import SnowflakeConnector


@task
def get_dbt_cli_profile(env: str) -> DbtCliProfile:  # noqa: ARG001
    """Get the dbt CLI profile.

    Args:
        env: The environment.

    Returns:
        DbtCliProfile: The dbt CLI profile.
    """
    dbt_connector = SnowflakeConnector(
        schema="BINK",
        database="SANDBOX",
        warehouse="ENGINEERING",
        credentials=SnowflakeCredentials.load("snowflake-transform-user"),
    )
    return DbtCliProfile(
        name="Bink_New",
        target="target",
        target_configs=SnowflakeTargetConfigs(connector=dbt_connector),
    )
