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

        -- some status returns a date timestamp (e.g., '2026-10-24 13:00:00Z) instead of a string
        -- rename the date timestamp to prevent downstream test failures
        CASE
            WHEN match_record.status LIKE '202%' THEN 'TIMED'
            ELSE match_record.status
        END as match_status,

        -- match_record.status as match_status,

        match_record.score.fullTime.home as home_goals,
        match_record.score.fullTime.away as away_goals

    FROM source

)

SELECT * FROM renamed