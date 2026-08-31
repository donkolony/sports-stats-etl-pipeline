SELECT DISTINCT
    team_id,
    team_name,
    team_short_name,
    team_crest_url
FROM {{ ref('stg_standings') }}
WHERE team_id is NOT NULL