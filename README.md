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

## Related Project

The transformed data stored in DuckDB is shared with `sports-stats-api-cloud`, which exposes it as a REST API deployed to the cloud.