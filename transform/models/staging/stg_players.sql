with source as(
    SELECT * FROM {{ source('football_data', 'raw_teams')}}
),

flatten_teams as (
    SELECT UNNEST(teams) as team_record
    FROM source
),

flatten_squad as (
    SELECT 
        team_record.id as team_id,
        UNNEST(team_record.squad) as player_record
    FROM flatten_teams
),

renamed as (
    SELECT
        player_record.id as player_id,
        player_record.name as player_name,
        player_record.position as player_positions,

        player_record.dateOfBirth::DATE as date_of_birth,
        player_record.nationality,

        team_id

    FROM flatten_squad
)

SELECT * FROM renamed