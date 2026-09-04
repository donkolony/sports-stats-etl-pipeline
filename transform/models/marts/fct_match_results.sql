SELECT
    matches.match_id,
    matches.match_status,
    home.team_name as home_team,
    away.team_name as away_team,
    matches.home_goals,
    matches.away_goals
FROM {{ ref('stg_matches') }} as matches -- table name
LEFT JOIN {{ ref('dim_teams') }} as home -- queryed table
    on matches.home_team_id = home.team_id
LEFT JOIN {{ ref('dim_teams') }} as away
    on matches.away_team_id = away.team_id