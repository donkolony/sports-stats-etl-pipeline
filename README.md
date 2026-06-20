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

## Related Project

The transformed data stored in DuckDB is shared with `sports-stats-api-cloud`, which exposes it as a REST API deployed to the cloud.