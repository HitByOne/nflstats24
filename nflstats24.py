import streamlit as st
import pandas as pd
import os

# Enable wide mode
st.set_page_config(layout="wide")

# Define the URLs for each file
url_teams = 'https://docs.google.com/spreadsheets/d/1-N-hlWJdnkbF6ePO1zJuyCRa1qNCTtPH/export?format=xlsx'  # Change to xlsx
url_players = 'https://drive.google.com/uc?id=1091grMf7sehBHvp-DtuJhNGULjrzz1Dt&export=download'
url_offensive_log = 'https://drive.google.com/uc?id=105TH-yx4Bo-7z1adI_RSGI9dxyNqHWbc&export=download'
url_defensive_log = 'https://drive.google.com/uc?id=106CX2NVg5avHM4yYnqSC_jVqsNm18w-x&export=download'
url_team_defensive_info = 'https://drive.google.com/uc?id=10F1AU7FEYLWs64Ld3-C_S_-NeAhu1pk_&export=download'
# Load the Excel file for teams
df_teams = pd.read_excel(url_teams)

# Load the CSV files directly from the URLs
df_players = pd.read_csv(url_players)
offensive_log = pd.read_csv(url_offensive_log)
defensive_log = pd.read_csv(url_defensive_log)
team_defensive_info = pd.read_csv(url_team_defensive_info)

# Extract unique team names (example usage)
teams = df_teams["Team"].unique().tolist()

# Side-by-side layout for offense and defense selection
col1, col2 = st.columns(2)

# Offense Team selection
with col1:
    st.header("Offense")
    offense_team = st.selectbox("Select Offense Team", teams, key="offense_team")

# Defense Team selection
with col2:
    st.header("Defense")
    defense_team = st.selectbox("Select Defense Team", [team for team in teams if team != offense_team], key="defense_team")

# Add a long horizontal line separator
st.markdown("<hr>", unsafe_allow_html=True)

# Handling duplicates without renaming them (referencing by column index)
# New set of columns for Player Lines on the left and Team Defensive Information on the right for QBs
col7, col8 = st.columns([3, 2])

# Filter player_lines data from the CSV based on the selected team and position (QB)
filtered_player_lines_qb = df_players[
    (df_players['Team'] == offense_team) & 
    (df_players['Position'] == 'QB') &  
    (df_players['Prop'].isin([
        'Passing - Attempts', 'Passing - Completions', 'Passing - Yards', 
        'Passing - Touchdowns', 'Rushing - Attempts', 'Rushing - Yards', 
        'Passing - Interceptions'
    ]))
]

# Display the filtered table with the specified columns for QB, setting Prop as the index
with col7:
    if not filtered_player_lines_qb.empty:
        st.subheader(f"Player Lines for {offense_team} - QB")
        st.write(filtered_player_lines_qb.set_index('Prop')[['Player', 'Team', 'Position', 'Over ML', 
                                                             'Games', 'Over', 'Rank', 'Totals', 'Average', 'Line']])
    else:
        st.write(f"No data available for {offense_team}.")

# Team Defensive Information for selected defense
with col8:
    st.subheader("Team Defensive Information")

    # Filter the team_defensive_info based on the selected defensive team and relevant props
    filtered_team_defense = team_defensive_info[
        (team_defensive_info['Opponent'] == defense_team) & 
        (team_defensive_info['Prop'].isin([
            'Passing - Total Yards', 'Passing - Yards', 'Passing - Touchdowns', 
            'Passing - Interceptions', 'Passing - Sack'
        ]))
    ]

    # Display the filtered defensive stats, setting Prop as the index
    if not filtered_team_defense.empty:
        st.write(filtered_team_defense.set_index('Prop')[['Totals', 'Average', 'Rank']])
    else:
        st.write(f"No defensive data available for {defense_team}.")

# Layout for QB stats
col5, col6 = st.columns([3, 2])

# Handling duplicates using column index positions
# Offensive Quarterbacks Stats
with col5:
    st.subheader("Offensive Stats for Quarterbacks")
    qb_stats_offense = offensive_log[
        (offensive_log['Team'] == offense_team) & 
        (offensive_log['Position'] == 'QB')
    ]

    if not qb_stats_offense.empty:
        qb_stats_offense.set_index('Week', inplace=True)
        # Refer to columns by index to avoid naming issues
        st.write(qb_stats_offense.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]])  # Adjust the index numbers to match the columns you want
    else:
        st.write("No offensive stats available for quarterbacks on the selected team.")

# Defensive Quarterbacks Stats
with col6:
    st.subheader("Quarterback Played Against Opponent")
    qb_stats_defense = defensive_log[
        (defensive_log['Position'] == 'QB') & 
        (defensive_log['Opponent'] == defense_team)
    ]

    if not qb_stats_defense.empty:
        qb_stats_defense.set_index('Week', inplace=True)
        # Refer to columns by index to avoid naming issues
        st.write(qb_stats_defense.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]])  # Adjust the index numbers to match the columns you want
    else:
        st.write("No defensive stats available for quarterbacks against the selected defense.")


# Horizontal line separator at the bottom of previous content
st.markdown("<hr>", unsafe_allow_html=True)

# New set of columns for Player Lines and Team Defensive Information for RB at the bottom of the page
col9, col10 = st.columns([3, 2])

# Filter player_lines data from the CSV based on the selected team and position (RB)
filtered_player_lines_rb = df_players[
    (df_players['Team'] == offense_team) & 
    (df_players['Position'] == 'RB') &  
    (df_players['Prop'].isin([
        'Rushing - Attempts', 'Rushing - Yards', 'Rushing - Touchdowns', 
        'Receiving - Receptions', 'Receiving - Yards'
    ]))
]

# Display the filtered table with the specified columns for RB, setting Prop as the index
with col9:
    if not filtered_player_lines_rb.empty:
        st.subheader(f"Player Lines for {offense_team} - RB")
        st.write(filtered_player_lines_rb.set_index('Prop')[['Player', 'Team', 'Position', 'Over ML', 
                                                             'Games', 'Over', 'Rank', 'Totals', 'Average', 'Line']])
    else:
        st.write(f"No data available for {offense_team}.")

# Team Defensive Information for selected defense (RB-related props)
with col10:
    st.subheader(f"Team Defensive Information for {defense_team} - Rushing")

    # Filter the team_defensive_info based on the selected defensive team and RB-related props
    filtered_defensive_rushing = team_defensive_info[
        (team_defensive_info['Opponent'] == defense_team) & 
        (team_defensive_info['Prop'].isin([
            'Rushing - Attempts', 'Rushing - Yards', 'Rushing - Touchdowns', 'Rushing - Longest Rush Attempt'
        ]))
    ]

    # Display the filtered defensive stats for rushing, setting Prop as the index
    if not filtered_defensive_rushing.empty:
        st.write(filtered_defensive_rushing.set_index('Prop')[['Totals', 'Average', 'Rank']])
    else:
        st.write(f"No defensive rushing data available for {defense_team}.")



# Layout for RB stats
col3, col4 = st.columns([3, 2])

# Offensive Running Backs Stats
with col3:
    st.subheader("Offensive Stats for All Running Backs")
    all_rb_stats = offensive_log[
        (offensive_log['Team'] == offense_team) & 
        (offensive_log['Position'] == 'RB') & 
        (offensive_log['Rushing - Attempts'] > 0)
    ]

    if not all_rb_stats.empty:
        all_rb_stats.set_index('Week', inplace=True)
        st.write(all_rb_stats[['Player', 'Opponent', 'Rushing - Attempts', 'Rushing - Yards', 'Rushing - Touchdowns',
                               'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No offensive stats available for running backs on the selected team.")

# Defensive Running Backs Stats
with col4:
    st.subheader("Running Back Played Against Opponent")
    defensive_stats_rb = defensive_log[
        (defensive_log['Position'] == 'RB') & 
        (defensive_log['Opponent'] == defense_team) & 
        (defensive_log['Rushing - Attempts'] > 0)
    ]

    if not defensive_stats_rb.empty:
        defensive_stats_rb.set_index('Week', inplace=True)
        st.write(defensive_stats_rb[['Player', 'Team', 'Rushing - Attempts', 'Rushing - Yards', 'Rushing - Touchdowns',
                                     'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No defensive stats available for running backs against the selected defense.")

# Horizontal line separator at the bottom of previous content
st.markdown("<hr>", unsafe_allow_html=True)

# Wide Receiver Section
# New set of columns for Player Lines and Team Defensive Information for WR
col9, col10 = st.columns([3, 2])

# Filter player_lines data from the CSV based on the selected team and position (WR)
filtered_player_lines_wr = df_players[
    (df_players['Team'] == offense_team) & 
    (df_players['Position'] == 'WR') &  
    (df_players['Prop'].isin([
        'Rushing - Touchdowns', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns'
    ]))
]

# Display the filtered table with the specified columns for WR, setting Prop as the index
with col9:
    if not filtered_player_lines_wr.empty:
        st.subheader(f"Player Lines for {offense_team} - WR")
        st.write(filtered_player_lines_wr.set_index('Prop')[['Player', 'Team', 'Position', 'Over ML', 
                                                             'Games', 'Over', 'Rank', 'Totals', 'Average', 'Line']])
    else:
        st.write(f"No data available for {offense_team}.")

# Team Defensive Information for selected defense (WR-related props)
with col10:
    st.subheader(f"Team Defensive Information for {defense_team} - WR Receiving")

    # Filter the team_defensive_info based on the selected defensive team and WR-related props
    filtered_defensive_receiving = team_defensive_info[
        (team_defensive_info['Opponent'] == defense_team) & 
        (team_defensive_info['Prop'].isin([
            'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns', 'Receiving - Longest Gain'
        ]))
    ]

    # Display the filtered defensive stats for receiving, setting Prop as the index
    if not filtered_defensive_receiving.empty:
        st.write(filtered_defensive_receiving.set_index('Prop')[['Totals', 'Average', 'Rank']])
    else:
        st.write(f"No defensive receiving data available for {defense_team}.")

# Layout for Offensive Stats for Wide Receivers and Tight Ends
col13, col14 = st.columns([3, 2])

# Offensive Wide Receivers Stats
with col13:
    st.subheader("Offensive Stats for All Wide Receivers")
    all_wr_stats = offensive_log[
        (offensive_log['Team'] == offense_team) & 
        (offensive_log['Position'] == 'WR') & 
        (offensive_log['Receiving - Receptions'] > 0)
    ]

    if not all_wr_stats.empty:
        all_wr_stats.set_index('Week', inplace=True)
        st.write(all_wr_stats[['Player', 'Opponent', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No offensive stats available for wide receivers on the selected team.")

# Defensive Wide Receivers Stats
with col14:
    st.subheader("Wide Receivers Played Against Opponent")
    defensive_stats_wr = defensive_log[
        (defensive_log['Position'] == 'WR') & 
        (defensive_log['Opponent'] == defense_team) & 
        (defensive_log['Receiving - Receptions'] > 0)
    ]

    if not defensive_stats_wr.empty:
        defensive_stats_wr.set_index('Week', inplace=True)
        st.write(defensive_stats_wr[['Player', 'Team', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No defensive stats available for wide receivers against the selected defense.")

# Horizontal line separator at the bottom of WR stats
st.markdown("<hr>", unsafe_allow_html=True)


# Tight End Section
# New set of columns for Player Lines and Team Defensive Information for TE
col11, col12 = st.columns([3, 2])

# Filter player_lines data from the CSV based on the selected team and position (TE)
filtered_player_lines_te = df_players[
    (df_players['Team'] == offense_team) & 
    (df_players['Position'] == 'TE') &  
    (df_players['Prop'].isin([
        'Rushing - Touchdowns', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns'
    ]))
]

# Display the filtered table with the specified columns for TE, setting Prop as the index
with col11:
    if not filtered_player_lines_te.empty:
        st.subheader(f"Player Lines for {offense_team} - TE")
        st.write(filtered_player_lines_te.set_index('Prop')[['Player', 'Team', 'Position', 'Over ML', 
                                                             'Games', 'Over', 'Rank', 'Totals', 'Average', 'Line']])
    else:
        st.write(f"No data available for {offense_team}.")


# Team Defensive Information for selected defense (TE-related props)
with col12:
    st.subheader(f"Team Defensive Information for {defense_team} - TE Receiving")

    # Filter the team_defensive_info based on the selected defensive team and TE-related props
    filtered_defensive_te = team_defensive_info[
        (team_defensive_info['Opponent'] == defense_team) & 
        (team_defensive_info['Prop'].isin([
            'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns', 'Receiving - Longest Gain'
        ]))
    ]

    # Display the filtered defensive stats for TE receiving, setting Prop as the index
    if not filtered_defensive_te.empty:
        st.write(filtered_defensive_te.set_index('Prop')[['Totals', 'Average', 'Rank']])
    else:
        st.write(f"No defensive receiving data available for {defense_team}.")


# Layout for Offensive Stats for Tight Ends
col15, col16 = st.columns([3, 2])

# Offensive Tight Ends Stats
with col15:
    st.subheader("Offensive Stats for All Tight Ends")
    all_te_stats = offensive_log[
        (offensive_log['Team'] == offense_team) & 
        (offensive_log['Position'] == 'TE') & 
        (offensive_log['Receiving - Receptions'] > 0)
    ]

    if not all_te_stats.empty:
        all_te_stats.set_index('Week', inplace=True)
        st.write(all_te_stats[['Player', 'Opponent', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No offensive stats available for tight ends on the selected team.")

# Defensive Tight Ends Stats
with col16:
    st.subheader("Tight Ends Played Against Opponent")
    defensive_stats_te = defensive_log[
        (defensive_log['Position'] == 'TE') & 
        (defensive_log['Opponent'] == defense_team) & 
        (defensive_log['Receiving - Receptions'] > 0)
    ]

    if not defensive_stats_te.empty:
        defensive_stats_te.set_index('Week', inplace=True)
        st.write(defensive_stats_te[['Player', 'Team', 'Receiving - Receptions', 'Receiving - Yards', 'Receiving - Touchdowns']])
    else:
        st.write("No defensive stats available for tight ends against the selected defense.")

# Horizontal line separator at the bottom of TE stats
st.markdown("<hr>", unsafe_allow_html=True)
