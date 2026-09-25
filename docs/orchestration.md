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
   [ fetch_matches ]         [ fetch_teams ]         [ fetch_standings ]
   (API -> JSON file)        (API -> JSON file)        (API -> JSON file)
           |                         |                         |
           v                         v                         v
   [ load_matches ]          [ load_teams ]          [ load_standings ]
 (partition overwrite)     (partition overwrite)     (partition overwrite)
           |                         |                         |
            \                        |                        /
             \                       v                       /
              \---------> [ dbt_build_staging ] <-----------/
               (stg_matches - stg_team - stg_standings)
                                     |
                                     v
                           [ dbt_build_marts ]
            (fct_match_results - fct_player_stats - dim_teams)
```