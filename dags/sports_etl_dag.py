import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "don_kolony",
    "retries": 1,
}

with DAG(
    dag_id="sports-stats-etl-pipeline",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 9, 7, tz="UTC"),
    schedule="@daily",
    catchup=False,
) as dag:
    fetch_matches = BashOperator(
        task_id="fetch_matches_task",
        bash_command="uv run -m src.ingestion.runner -c PL matches",
    )

    fetch_standings = BashOperator(
        task_id="fetch_standings_task",
        bash_command="uv run -m src.ingestion.runner -c PL standings",
    )

    fetch_teams = BashOperator(
        task_id="fetch_teams_task",
        bash_command="uv run -m src.ingestion.runner -c PL teams",
    )

    dbt_build = BashOperator(
        task_id="dbt_build_task",
        bash_command="uv run dbt build --project-dir transform --project-dir transform",
    )

    [fetch_matches, fetch_standings, fetch_teams] >> dbt_build
