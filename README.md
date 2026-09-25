# ⚽ Sports Stats ETL Pipeline

An end-to-end **data engineering pipeline** that extracts Premier League football statistics from the [Football-Data.org](https://www.football-data.org/) API, transforms the raw data into clean, analytics-ready models, and loads it into a local **DuckDB data warehouse**.

The transformed data is consumed by the companion cloud project `sports-stats-api-cloud` and visualized through an interactive **Streamlit dashboard**.

[![Live Demo](https://img.shields.io/badge/Demo-Video-red?style=for-the-badge\&logo=youtube)](youtube.com)
[![Backend](https://img.shields.io/badge/API-Documentation-green?style=for-the-badge)](linkhere)

---

## 🏗️ Pipeline Architecture

```text
Football-Data.org API
        │
        ▼
Python Ingestion
        │
        ▼
Raw JSON (data/raw/)
        │
        ▼
DuckDB (raw schema)
        │
        ▼
dbt Transformations
(staging → marts)
        │
        ▼
DuckDB
(analytics-ready marts)
        │
        ├──────────────────────┐
        ▼                      ▼
Streamlit Dashboard     sports-stats-api-cloud
```

---

## 🛠️ Tech Stack

| Technology             | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| **Python**             | Extracts data from the Football-Data.org API      |
| **Apache Airflow**     | Orchestrates and schedules the ETL pipeline       |
| **DuckDB**             | Local analytical data warehouse                   |
| **dbt**                | Transforms raw data into staging and mart models  |
| **Streamlit + Plotly** | Interactive analytics dashboard                   |
| **pytest**             | Unit tests for ingestion and transformation logic |
| **uv**                 | Fast Python package and environment manager       |
| **Make**               | Command runner for simplified execution           |

---

## 📊 Data Pipeline

The pipeline follows a traditional **Extract → Load → Transform** workflow:

### 1. Extract

Python retrieves football data from the Football-Data.org API.

Currently supported entities include:

* Match results
* League standings
* Teams

### 2. Load

The raw API responses are stored as JSON and loaded into DuckDB.

Raw data follows a partitioned structure:

```text
data/raw/
└── entity/
    └── YYYY/
        └── MM/
            └── DD/
```

### 3. Transform

**dbt** transforms the raw DuckDB data into analytics-ready models:

```text
Raw Data
   │
   ▼
Staging Models
   │
   ▼
Dimension & Fact Models
```

Example models include:

* `dim_teams`
* `fct_match_results`
* `fct_player_stats`

### 4. Visualize

The resulting analytical tables are consumed by the Streamlit dashboard to provide insights such as:

* Match histories
* Goal distributions
* Team performance
* League statistics

---

# 🚀 Local Setup

## Prerequisites

Before getting started, make sure you have the following installed:

* Python **3.10+**
* [uv](https://docs.astral.sh/uv/)
* Make
* A free [Football-Data.org](https://www.football-data.org/) API key

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Make

**macOS**

Make is usually pre-installed. Alternatively:

```bash
brew install make
```

**Linux**

```bash
sudo apt install make
```

**Windows**

Use GNU Make or WSL.

---

# 📥 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/donkolony/sports-stats-etl-pipeline.git

cd sports-stats-etl-pipeline
```

## 2. Create a Virtual Environment

Using `uv`:

```bash
uv venv
```

Activate the environment:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
uv pip install -r pyproject.toml
```

---

# 🔑 Configuration

The pipeline requires an API key from Football-Data.org.

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API key:

```env
FOOTBALL_DATA_API_KEY="your_actual_key_here"
```

> **Important:** Never commit your `.env` file or API key to Git.

Make sure `.env` is included in your `.gitignore`.

---

# ▶️ Running the Pipeline

There are two ways to run the pipeline.

## Option A - Using Make

The recommended approach is to use the included `Makefile`.

### Run the complete pipeline

```bash
make run-all
```

This runs the complete workflow:

```text
API
 ↓
Data Ingestion
 ↓
DuckDB
 ↓
dbt Transformations
 ↓
Data Quality Tests
```

### Clean the DuckDB warehouse

```bash
make clean
```

This removes the local DuckDB warehouse so the pipeline can be started from a clean state.

---

## Option B - Manual Execution

You can also run each component individually for debugging or development.

### 1. Data Ingestion

Extract and load Premier League data:

```bash
uv run -m src.ingestion.runner -c PL matches
```

```bash
uv run -m src.ingestion.runner -c PL standings
```

```bash
uv run -m src.ingestion.runner -c PL teams
```

> **Note:** The competition code (PL) can be replaced with any of the supported competition codes defined in `config.py`.

Where:

* `PL` = Premier League competition code
* `matches` = Match data
* `standings` = League standings
* `teams` = Team information

---

### 2. Run dbt Transformations

Build the staging and mart models:

```bash
uv run dbt build --project-dir transform --profiles-dir transform
```

This command also executes the configured dbt data quality tests.

---

# 📈 Visualizing the Data

After the DuckDB mart tables have been successfully created, launch the Streamlit dashboard:

```bash
uv run streamlit run dashboard/app.py
```

The dashboard provides an interactive interface for exploring the transformed football data.

Example insights include:

* Match histories
* Goal distributions
* Team performance
* League statistics

---

# 🧪 Testing

The project uses **pytest** for testing ingestion and transformation logic.

Run the test suite with:

```bash
uv run -m pytest tests -v
```

dbt tests can be executed as part of:

```bash
uv run dbt build --project-dir transform --profiles-dir transform
```

---

# 🔄 Data Engineering Design

## Clean Architecture

The ingestion layer separates responsibilities between individual components:

```text
src/
└── ingestion/
    ├── config.py
    ├── api_client.py
    ├── local_storage.py
    └── runner.py
```

### `config.py`

Responsible for configuration and API credentials.

### `api_client.py`

Handles communication with the Football-Data.org API.

### `local_storage.py`

Manages local storage and raw data partitions.

### `runner.py`

Acts as the orchestration layer that coordinates the ingestion process while keeping individual components decoupled.

---

## 🗄️ Data Warehouse

**DuckDB** is used as the shared analytical data layer.

Downstream applications connect to the database using:

```python
read_only = True
```

This helps prevent file-locking conflicts when multiple applications access the analytical data.

---

## 🔁 Idempotency

The pipeline uses a:

```sql
CREATE OR REPLACE TABLE
```

strategy when loading data.

This ensures that repeated runs replace stale records instead of continuously creating duplicate records.

The approach is similar to a **partition overwrite strategy**, making the pipeline safe to run repeatedly.

---

# 🧬 dbt Model Lineage

The dbt transformation layer follows a staging-to-mart architecture:

```text
Raw API Data
      │
      ▼
Staging Models
      │
      ├───────────────┐
      ▼               ▼
Dimensions          Facts
      │               │
      ▼               ▼
dim_teams       fct_match_results
                fct_player_stats
```

### Dimension Models

```text
dim_teams
```

Contains descriptive information about teams.

### Fact Models

```text
fct_match_results
fct_player_stats
```

Contain measurable football events and statistics used for analysis.

---

# ☁️ Related Projects

The transformed data is designed to work with the companion cloud project:

```text
sports-stats-api-cloud
```

The architecture separates the **data engineering pipeline** from the **cloud/API consumption layer**, allowing the analytical data to be reused by downstream applications.

---

# 📁 Project Structure

```text
sports-stats-etl-pipeline/
│
├── data/
│   └── raw/
│   └── warehouse/
│
├── dags/
│   └── sports_etl_dag.py
|
├── dashboard/
│   └── app.py
|
├── docs/
│   └── architecture.md
│   └── data_modeling.md
│   └── ingestion.md
│   └── orchestration.md
│
├── src/
│   └── ingestion/
│       ├── config.py
│       ├── api_client.py
│       ├── local_storage.py
│       └── runner.py
│
├── transform/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
│   └── profiles.yml
│
├── tests/
│   └── test_api_client.py
│   └── test_local_storage.py
│   └── test_runner.py
│
├── .env
├── Makefile
├── License
├── pyproject.toml
└── README.md
└── Requirements.txt
└── uv.lock
```

---

# 🎯 Project Goals

This project was built to demonstrate practical data engineering concepts including:

* API data ingestion
* ETL pipeline design
* Data warehousing
* Dimensional modelling
* Fact and dimension tables
* dbt transformations
* Data quality testing
* Pipeline idempotency
* Workflow orchestration
* Analytical SQL
* DuckDB
* Data visualization
* Reusable data architecture

---

> Verification Code: WTC-NTQUAPBD