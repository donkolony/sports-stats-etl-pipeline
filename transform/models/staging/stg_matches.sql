with source as (

    SELECT UNNEST(matches) as match_record
    FROM {{ source('football_data', 'raw_matches') }}

),

renamed as (

    SELECT
        match_record.id as match_id,

        match_record.homeTeam.id as home_team_id,
        match_record.awayTeam.id as away_team_id,
        
        match_record.utcDate as match_date,
        match_record.matchday,
        match_record.status as match_status,

        match_record.score.fullTime.home as home_goals,
        match_record.score.fullTime.away as away_goals

    FROM source

)

SELECT * FROM renamed