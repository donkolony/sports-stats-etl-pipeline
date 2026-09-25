## dbt Model Lineage

Our **dbt** project follows a layered dimensional modeling approach, transforming raw API data into clean, analytics-ready tables. 

### Model Lineage

```text
stg_standings ──────────► dim_teams 
                              │
                              ├──► fct_player_stats ◄── stg_players
                              │
                              └──► fct_match_results ◄── stg_matches