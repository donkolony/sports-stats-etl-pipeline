import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Sport Stats Pipeline")


@st.cache_resource
def get_db_connection(
    database_path: str = "data/warehouse/football_sports.db",
):
    # set read-only mode to prevent write/read conflicts with Airflow
    return duckdb.connect(database=database_path, read_only=True)


con = get_db_connection()

# fetch match history
df_matches = con.execute("SELECT * FROM main.fct_match_results").df()

st.header("Match History")

st.dataframe(data=df_matches, width="stretch")

if not df_matches.empty:
    fig_matches = px.bar(
        data_frame=df_matches,
        x="home_team",
        y="home_goals",
        title="Goals Scored by Home Teams",
        color="home_team",
    )

    st.plotly_chart(figure_or_data=fig_matches, width="stretch")
else:
    st.info(
        "No match data available yet. Ensure your Airflow pipeline has run successfully"
    )


st.divider()
st.header("Team Performance")

if not df_matches.empty:
    # aggregate goals scored as the Home Team
    home_goals = df_matches.groupby("home_team")["home_goals"].sum().reset_index()
    home_goals.rename(
        columns={"home_team": "team", "home_goals": "goals_scored"},
        inplace=True,
    )

    # aggregate goals scored as the Away Team
    away_goals = df_matches.groupby("away_team")["away_goals"].sum().reset_index()
    away_goals.rename(
        columns={"away_team": "team", "away_goals": "goals_scored"},
        inplace=True,
    )

    # combine both to get Total goals per team
    total_goals = (
        pd.concat([home_goals, away_goals])
        .groupby("team")["goals_scored"]
        .sum()
        .reset_index()
    )

    top_scoring_teams = total_goals.sort_values(
        by="goals_scored", ascending=False
    ).head(10)

    fig_teams = px.bar(
        data_frame=top_scoring_teams,
        x="team",
        y="goals_scored",
        title="Top 10 Higest Scoring Teams",
        color="team",
    )
    st.plotly_chart(figure_or_data=fig_teams, width="stretch")
else:
    st.info("No match data available yet to calculate team performance.")

# st.divider()
# st.header("Player Statistics")


# df_players = con.execute("SELECT * FROM main.fct_players_stats").df()
# st.dataframe(data=df_players, width="stretch")

# if not df_players.empty:
#     fig_players = px.bar(
#         data_frame=df_players,
#         x="player_name",
#         y="player_goals",
#         title="Top Player Performance",
#         color="blue",
#     )
#     st.plotly_chart(figure_or_data=fig_players, width="stretch")
