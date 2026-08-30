with source as (
    SELECT * FROM {{ source('football_data', 'raw_standings') }}
),

flatten_standings as (
    SELECT UNNEST(standings) as standing_record
    FROM source
),

flatten_table as (
    SELECT UNNEST(standing_record."table") as team_record
    FROM flatten_standings
),

renamed as (
    SELECT
        team_record.team.id as team_id,
        team_record.team.name as team_name,
        team_record.team.shortName as team_short_name,
        team_record.team.crest as team_crest_url,

        team_record.position as league_position,
        team_record.playedGames as games_played,
        team_record.form as form,
        team_record.won as won,
        team_record.draw as draw,
        team_record.lost as lost,
        team_record.points as points,
        team_record.goalsFor as goals_for,
        team_record.goalsAgainst as goals_against,
        team_record.goalDifference as goals_difference


    FROM flatten_table
)


SELECT * FROM renamed