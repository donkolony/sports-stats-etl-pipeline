SELECT
    players.*,
    teams.team_name
FROM {{ ref('stg_teams') }} as players
LEFT JOIN {{ ref('dim_teams') }} as teams
    on players.team_id = teams.team_id