[![Live Demo](https://img.shields.io/badge/Demo-Video-red?style=for-the-badge&logo=youtube)](youtube.com)
[![Backend](https://img.shields.io/badge/API-Documentation-green?style=for-the-badge)](linkhere)

# Sports Stats ETL Pipeline

An end-to-end data engineering pipeline that extracts Premier League football statistics from the Football-Data.org API, transforms the raw data into clean, analytics-ready models, and loads it into a local DuckDB data warehouse. The stored data is then consumed by the companion cloud project (`sports-stats-api-cloud`) and visualised through a Streamlit dashboard.

## Tech Stack

* **Python**: ingestion scripts to extract data from the API
* **Apache Airflow**: orchestrates and schedules the pipeline daily
* **DuckDB**: local analytical data warehouse (stores the transformed data)
* **dbt**: transforms raw data into clean staging and mart models
* **Streamlit + Plotly**: dashboard for visualising match results and standings
* **pytest**: unit tests for ingestion and transformation logic

## Communication Flow

```text
Football-Data.org API
        ↓
Ingestion (Python scripts)
        ↓
Raw JSON → data/raw/  (local data lake)
        ↓
DuckDB  (raw schema)
        ↓
dbt transforms  (staging → marts)
        ↓
DuckDB  (marts schema)
        ↓
Streamlit dashboard  ←  consumed locally
        ↓
sports-stats-api-cloud  ←  reads from DuckDB marts
```

## System Architecture

Our data pipeline is built around a lightweight, modern data stack for extracting, loading, and transforming Premier League football statistics. Rather than relying heavily on containers, we focus on simplicity, fast local development, and clean separation of responsibilities.

### 1. Orchestration & Execution

**Apache Airflow** orchestrates the entire ETL workflow by scheduling and managing daily pipeline runs.

Instead of running pipeline tasks inside Docker containers, Airflow executes our Python ingestion scripts and **dbt** transformations directly on the host machine. This approach avoids the complexity of Docker-in-Docker networking while keeping the workflow simple and efficient.

To ensure dependencies remain isolated and reproducible, each component is managed using **uv**, allowing separate virtual environments without the overhead of traditional environment management tools.

---

### 2. Local Data Lake

Raw data retrieved from the **Football-Data.org API** is stored locally in a structured data lake.

Rather than placing all files into a single directory, the data is partitioned by both entity and extraction date. For example:

```text
data/
└── raw/
    └── matches/
        └── YYYY/
            └── MM/
                └── DD/
```

This partitioning strategy offers several benefits:

- Makes historical backfills much easier.
- Simplifies debugging by isolating each extraction.
- Reduces the amount of data that needs to be scanned during downstream processing.

---

### 3. Data Warehouse & Concurrency

The transformed data is stored in **DuckDB**, which serves as the project's analytical data warehouse.

Since DuckDB is optimized for analytical workloads but generally permits only one writer at a time, the pipeline follows a simple concurrency strategy:

- The ETL pipeline (Python ingestion and dbt transformations) is responsible for writing data to DuckDB.
- Downstream applications, such as the **Streamlit dashboard**, connect using **read-only** mode (`read_only=True`), preventing accidental writes.
- Airflow schedules write operations during periods when dashboard usage is expected to be minimal, reducing the chance of write/read conflicts.

This approach provides excellent analytical performance while keeping the architecture lightweight and easy to maintain.

## Data Flow & Idempotency

The pipeline follows a clear, layered architecture where data progresses through a series of stages. Each layer has a specific responsibility, making the pipeline easier to understand, maintain, and debug.

### Data Flow

Data moves through the following layers in sequence:

```text
Football-Data.org API
          │
          ▼
 Raw JSON (Local Data Lake)
          │
          ▼
 DuckDB - Raw Schema
          │
          ▼
 DuckDB - Staging Schema
          │
          ▼
 DuckDB - Marts Schema
```

---

### Idempotency Strategy

To ensure the pipeline can be safely rerun without creating duplicate records, we use a **partition overwrite** (delete-and-insert) strategy.

For each execution:

1. The pipeline identifies the partition for the current run (for example, a specific `match_date`).
2. Any existing records for that date are removed using a `DELETE` statement.
3. The latest data is then inserted from the raw JSON files into DuckDB.

This approach offers several advantages:

- Prevents duplicate records when a job is rerun.
- Allows failed pipeline runs to be safely retried.
- Leaves historical data untouched.
- Avoids the overhead of rebuilding entire tables.

## Airflow DAG & Task Dependencies

Our Airflow **Directed Acyclic Graph (DAG)** orchestrates the pipeline by defining a clear sequence of tasks and their dependencies. 

### Task Execution Flow

#### Parallel Ingestion

The pipeline begins by extracting data for the three primary entities: Matches, Players, and Standings. Each extraction and loading process runs independently, allowing Airflow to execute them in parallel.

#### The Convergence Point

Before any transformations begin, Airflow waits for **all three datasets** to be successfully loaded into the DuckDB **Raw** schema. 

#### Transformation & Testing

Rather than running `dbt run` and `dbt test` as separate tasks, the pipeline uses the `dbt build` command. This approach combines model execution and testing into a single workflow.

```text
dbt build execution flow

[ dbt_build_staging ]
   ├─► Build: stg_matches (clean & format raw data)
   └─► Test:  stg_matches (check for nulls/duplicates)
               │
         (if tests pass)
               │
               ▼
[ dbt_build_marts ]
   ├─► Build: fct_match_results (join with dimensions)
   └─► Test:  fct_match_results (final QA check)
```

---

### DAG Structure Overview

```text
   [ fetch_matches ]         [ fetch_players ]         [ fetch_standings ]
   (API -> JSON file)        (API -> JSON file)        (API -> JSON file)
           |                         |                         |
           v                         v                         v
   [ load_matches ]          [ load_players ]          [ load_standings ]
 (partition overwrite)     (partition overwrite)     (partition overwrite)
           |                         |                         |
            \                        |                        /
             \                       v                       /
              \---------> [ dbt_build_staging ] <-----------/
               (stg_matches - stg_players - stg_standings)
                                     |
                                     v
                           [ dbt_build_marts ]
            (fct_match_results - fct_player_stats - dim_teams)
```

## dbt Model Lineage

Our **dbt** project follows a layered dimensional modeling approach, transforming raw API data into clean, analytics-ready tables. 

### Model Lineage

```text
stg_standings ──────────► dim_teams 
                              │
                              ├──► fct_player_stats ◄── stg_players
                              │
                              └──► fct_match_results ◄── stg_matches
```

## Related Project

The transformed data stored in DuckDB is shared with `sports-stats-api-cloud`, which exposes it as a REST API deployed to the cloud.