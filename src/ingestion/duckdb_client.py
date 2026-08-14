from datetime import datetime
from pathlib import Path

import duckdb


def load_raw_data(
    entity: str,
    execution_date: datetime,
    database: str = "storage/warehouse/football_sports.db",
) -> None:
    """
    Loads raw JSON data from the data lake into DuckDB using an idempotent delete-insert strategy

    Args:
        entity (str): The data domain to load (e.g. "matches", "teams", "standings") used to locate the source
        JSON and name the  target table

        execution_date (datetime): The Airflow logical date identifying which partition to load and overwrite

        database (str, optional): Path to the DuckDB database file. Defaults to "storage/warehouse/football_sports.db".
    """

    year: str = execution_date.strftime("%Y")
    month: str = execution_date.strftime("%m")
    day: str = execution_date.strftime("%d")

    file_path: Path = (
        Path("storage") / "raw" / entity / year / month / day / "data.json"
    )

    # SQL variables
    table_name: str = f"raw_{entity.split('/')[-1]}"
    column_name: str = "ingestion_date"

    date_str: str = execution_date.strftime("%Y-%m-%d")

    print(f"Loading `{table_name}` data into DuckDB table `{table_name}`...")

    # Defensively ensure the database directory exists else create it
    db_dir = Path(database).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Connect to DuckDB and execute the database the transaction
    with duckdb.connect(database=database) as con:
        # 1. Create table
        con.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS
            SELECT *, '{date_str}' AS {column_name}
            FROM read_json_auto('{file_path}')
            """
        )

        # 2. Delete existing partition
        con.sql(
            f"""
            DELETE FROM {table_name}
            WHERE {column_name} = '{date_str}'
            """
        )

        # 3. Insert fresh data
        con.sql(
            f"""
            INSERT INTO {table_name}
            SELECT *, '{date_str}' AS {column_name}
            FROM read_json_auto('{file_path}')
            """
        )

    print(f"Successfully loaded '{entity}' data.")
