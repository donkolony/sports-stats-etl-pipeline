[![Live Demo](https://img.shields.io/badge/Demo-Video-red?style=for-the-badge\&logo=youtube)](youtube.com)
[![Backend](https://img.shields.io/badge/API-Documentation-green?style=for-the-badge)](linkhere)

# Sports Stats ETL Pipeline

An end-to-end data engineering pipeline that extracts Premier League football statistics from the Football-Data.org API, transforms the raw data into clean, analytics-ready models, and loads it into a local DuckDB data warehouse.

The transform data is consumed by the companion cloude project (`sports-stats-api-cloud`) and visulized through a Streamlit dashboard.

---

# Tech Stack

| Technology             | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| **Python**             | Extracts data from the Football-Data.org API      |
| **Apache Airflow**     | Orchestrates and schedules the ETL pipeline       |
| **DuckDB**             | Local analytical data warehouse                   |
| **dbt**                | Transforms raw data into staging and mart models  |
| **Streamlit + Plotly** | Interactive analytics dashboard                   |
| **pytest**             | Unit tests for ingestion and transformation logic |

# Pipeline Arhitecture

```text
Football-Data.org API
        ↓
Python Ingestion
        ↓
Raw JSON (data/raw/)
        ↓
DuckDB (raw schema)
        ↓
dbt Transformations
(staging → marts)
        ↓
DuckDB (analytics-ready marts)
        ↓
┌───────────────────────────────┐
│ Streamlit Dashboard           │
│ sports-stats-api-cloud        │
└───────────────────────────────┘
```

TODO 

# Local Setup

## Prerequisites

## 1. Clone the Repository

## 2. Create a Virtual Environment

## 3. Configure API Credentials

## 4. Run the Pipeline

# Documentation

**Verification Code:**
WTC-NTQUAPBD