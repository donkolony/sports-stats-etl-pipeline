from datetime import datetime
from pathlib import Path

import duckdb


def load_raw_data(
    entity: str,
    execution_date: datetime,
    file_path: str,
    database: str = "data/warehouse/football_sports.db",
) -> None:
    """
    Loads raw JSON data from the data lake into DuckDB using an idempotent delete-insert strategy

    Args:
        entity (str): The data domain to load (e.g. "matches", "teams", "standings") used to locate the source
        JSON and name the  target table
        execution_date (datetime): The Airflow logical date identifying which partition to load and overwrite
        file_path (str): the file path to fetch the data to load into the db
        database (str, optional): Path to the DuckDB database file. Defaults to "data/warehouse/football_sports.db".
    """

    # SQL variables
    table_name: str = f"raw_{entity}"
    column_name: str = "ingestion_date"
    date_str: str = execution_date.strftime("%Y-%m-%d")

    print(f"Loading `{table_name}` data into DuckDB table `{table_name}`...")

    # Defensively ensure the database directory exists else create it
    db_dir = Path(database).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Connect to DuckDB and execute the database the transaction
    with duckdb.connect(database=database) as con:
        con.execute("Start Transaction")

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

        # Save the transaction
        con.execute("COMMIT")
        print(f"Successfully loaded '{entity}' data.")
