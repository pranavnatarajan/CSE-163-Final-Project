"""
Alex Eidt- CSE 163 AC
Pranav Natarajan - CSE 163 AB

CSE 163 A
Final Project

Processes the parsed dataset to prepare it for
our analysis.
"""
import os
import pandas as pd
from gather import gather_data

# Information we will pull out of the dataset from GitHub
stats = [
    'Total_Matches',
    'Total_Matches_Reg', # Reg = Regulation
    'Home_Matches_Reg',
    'Home_Wins_Reg',
    'Home_Ties_Reg',
    'Away_Wins_Reg',
    'Away_Ties_Reg',
    'Home_Goals_Reg',
    'Home_Goals_Conceded_Reg',
    'Away_Goals_Reg',
    'Away_Goals_Conceded_Reg',
]


def filter_data():
    """
    Filters the Champions League Dataset.
    Returns
        A pandas DataFrame representing the filtered
        dataset.
    """
    df = gather_data()

    # All Champions League Seasons before 1994 were in a
    # different format than the curret competition.
    # Our analysis will therefore only look at matches
    # from 1994 to present.
    after_1994 = df['Season'] >= 1994
    # Our analysis focuses on which team will win the
    # Champions League once they are in the competition.
    # Qualifiers are not part of the competition itself,
    # they determine who gets to compete and therefore
    # will not be considered in our analysis.
    qualifiers = (df['round'] != 'Q-1') & \
                (df['round'] != 'Q-2') & \
                (df['round'] != 'Q-3') & \
                (df['round'] != 'Q-PO') & \
                (df['round'] != 'prelim') & \
                (df['round'] != 'PrelimF')
    
    return df[after_1994 & qualifiers]


def process_data(start=1994, end=2015):
    """
    Processes the dataset (from games within the range of
    start to end) to get calculated values for each
    team concerning win percentages, average goals scored,
    as well as Home/Away totals.
    Parameters
        start - The year to begin looking at match data (inclusive)
        end   - The year to end looking at match data (inclusive)
    Returns
        A pandas DataFrame representing the processed data.
    """
    data = {}

    df = filter_data()
    
    df = df[(df['Season'] >= start) & (df['Season'] <= end)]
    df = df[
        ['home', 'leg', 'visitor', 'hgoal', 'vgoal']
    ].to_dict(orient='records')

    for match in df:
        home = match['home'] # Home Team
        visitor = match['visitor'] # Visiting Team
        # stats contains all statistics we'll pull out of the DataSet
        # to use for our calculations
        if home not in data:
            data[home] = {stat: 0 for stat in stats}
        if visitor not in data:
            data[visitor] = {stat: 0 for stat in stats}

        hgoals = match['hgoal'] # Goals scored by home team
        vgoals = match['vgoal'] # Goals scored by visiting team
        
        data[home]['Total_Matches'] += 1
        data[visitor]['Total_Matches'] += 1
        data[home]['Home_Goals_Reg'] += hgoals
        data[home]['Home_Goals_Conceded_Reg'] += vgoals
        data[visitor]['Away_Goals_Reg'] += vgoals
        data[visitor]['Away_Goals_Conceded_Reg'] += hgoals

        if hgoals == vgoals:
            if match['leg'] == 'groups':
                # If the game is in the group stages, there is no added extra time
                # or penalties, the game ends as a tie.
                data[home]['Home_Ties_Reg'] += 1
                data[visitor]['Away_Ties_Reg'] += 1
                data[home]['Total_Matches_Reg'] += 1
                data[visitor]['Total_Matches_Reg'] += 1
                data[home]['Home_Matches_Reg'] += 1
            else:
                data[home]['Home_Ties_Reg'] += 1
                data[visitor]['Away_Ties_Reg'] += 1
        elif hgoals > vgoals:
            data[home]['Home_Wins_Reg'] += 1
            data[home]['Total_Matches_Reg'] += 1
            data[visitor]['Total_Matches_Reg'] += 1
            data[home]['Home_Matches_Reg'] += 1
        else:
            data[visitor]['Away_Wins_Reg'] += 1
            data[home]['Total_Matches_Reg'] += 1
            data[visitor]['Total_Matches_Reg'] += 1
            data[home]['Home_Matches_Reg'] += 1

    data = pd.DataFrame().from_dict(data, orient='index')
    data['Reg_Win_%'] = (data['Home_Wins_Reg'] + data['Away_Wins_Reg']) / data['Total_Matches_Reg']
    data['Reg_Tie_%'] = (data['Home_Ties_Reg'] + data['Away_Ties_Reg']) / data['Total_Matches_Reg']

    away_matches_reg = data['Total_Matches_Reg'] - data['Home_Matches_Reg']
    data['Away_Reg_Win_%'] = data['Away_Wins_Reg'] / away_matches_reg
    data['Home_Reg_Win_%'] = data['Home_Wins_Reg'] / data['Home_Matches_Reg']
    data['Away_Reg_Tie_%'] = data['Away_Ties_Reg'] / away_matches_reg
    data['Home_Reg_Tie_%'] = data['Home_Ties_Reg'] / data['Home_Matches_Reg']

    data['Avg_Home_Goals_Reg'] = data['Home_Goals_Reg'] / data['Home_Matches_Reg']
    data['Avg_Home_Goals_Conceded_Reg'] = data['Home_Goals_Conceded_Reg'] / data['Home_Matches_Reg']
    data['Avg_Away_Goals_Reg'] = data['Away_Goals_Reg'] / away_matches_reg
    data['Avg_Away_Goals_Conceded_Reg'] = data['Away_Goals_Conceded_Reg'] / away_matches_reg

    data.to_csv('Champions_League_Processed_Data.csv')
    return data


if __name__ == '__main__':
    df = process_data()