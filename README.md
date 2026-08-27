[![Live Demo](https://img.shields.io/badge/Demo-Video-red?style=for-the-badge&logo=youtube)](youtube.com)
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

---

# Local Setup

## Prerequisites

Before getting started, ensure you have:

- Python 3.10+
- `uv` (optional but recommended)

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 1. Clone the Repository

```bash
git clone https://github.com/donkolony/sports-stats-etl-pipeline.git
cd sports-stats-etl-pipeline
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option B - Using uv

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

---

## 3. Configure API Credentials

Obtain a free API key from Football-Data.org.

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API key:

```text
FOOTBALL_DATA_API_KEY="your_actual_key_here" # ref .env.example
```

---

## 4. Run the Pipeline

```bash
uv run -m src.ingestion,runner -c PL matches

PL: competition code (Premier League)
matches: entity
```

# Documentation

- Python Ingestion

> Verification Code: WTC-NTQUAPBD
