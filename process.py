"""
Alex Eidt
Pranav Natarajan

CSE 163 AC
Final Project

Processes the dataset to prepare it for our analysis.
"""


import os
import pandas as pd
from gather import gather_data

# Information we will pull out of the dataset from GitHub
stats = [
    'Total_Matches',
    'Total_Matches_Reg', # Reg = Regulation
    'Home_Matches_Reg',
    'Total_Matches_AET', # AET = Added Extra Time
    'Home_Matches_AET',
    'Total_Matches_Pens', # Pens = Penalty Kicks
    'Home_Matches_Pens',
    'Home_Wins_Reg',
    'Home_Ties_Reg',
    'Away_Wins_Reg',
    'Away_Ties_Reg',
    'Home_Goals_Reg',
    'Home_Goals_Conceded_Reg',
    'Away_Goals_Reg',
    'Away_Goals_Conceded_Reg',
    'Home_Wins_AET',
    'Home_Ties_AET',
    'Away_Wins_AET',
    'Away_Ties_AET',
    'Home_Goals_AET',
    'Home_Goals_Conceded_AET',
    'Away_Goals_AET',
    'Away_Goals_Conceded_AET',
    'Home_Wins_Pens',
    'Away_Wins_Pens',
    'Home_Goals_Pens',
    'Home_Goals_Conceded_Pens',
    'Away_Goals_Pens',
    'Away_Goals_Conceded_Pens'
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


def process_data():
    """
    Processes the dataset to get calculated values for each
    team concerning win percentages, average goals scored,
    as well as Home/Away totals.

    Returns
        A pandas DataFrame representing the processed data.
    """
    data = {}

    df = filter_data()[
        ['home', 'leg', 'visitor', 'hgoal', 'vgoal', 'aethgoal', 'aetvgoal', 'pens']
    ].to_dict(orient='records')

    if 'Champions_League_Processed.csv' not in os.listdir(os.getcwd()):
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
            aethgoals = match['aethgoal'] # Goals scored by home team in added extra time (aet)
            aetvgoals = match['aetvgoal'] # Goals scored by visiting team in added extra time (aet)
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
                    if aethgoals == aetvgoals:
                        # If the game is not decided in Regulation or Added Extra Time
                        # the penalty score determines the winner.
                        data[home]['Home_Ties_AET'] += 1
                        data[visitor]['Away_Ties_AET'] += 1
                        # In the Champions League, Knock out rounds have both teams play two
                        # game (one home game for each) and whoever has the highest aggregate score
                        # over both these games wins the tie and moves on in the competition.
                        # Away goals are more valuable than home goals, therefore, at tie between
                        # two teams can end as a tie, but there can still be a winner.
                        # If Teams A and B tied 4-4 on aggregate and the score of the first match
                        # was A: 2, B: 3 and the score of the second match was B: 1, A: 2, B would
                        # advance because B has 3 away goals, while A has 2.
                        if match['pens'] != 'away goals':
                            home_pens, away_pens = match['pens'].split('-')
                            home_pens = int(home_pens)
                            away_pens = int(away_pens)
                            if home_pens > away_pens:
                                data[home]['Home_Wins_Pens'] += 1
                            else:
                                data[home]['Away_Wins_Pens'] += 1
                            data[home]['Home_Goals_Pens'] += home_pens
                            data[home]['Home_Goals_Conceded_Pens'] += away_pens
                            data[visitor]['Away_Goals_Pens'] += away_pens
                            data[visitor]['Away_Goals_Conceded_Pens'] += home_pens
                            data[home]['Home_Matches_Pens'] += 1
                            data[home]['Total_Matches_Pens'] += 1
                            data[visitor]['Total_Matches_Pens'] += 1
                    elif aethgoals > aetvgoals:
                        data[home]['Home_Wins_AET'] += 1
                    else:
                        data[visitor]['Away_Wins_AET'] += 1
                    data[home]['Total_Matches_AET'] += 1
                    data[visitor]['Total_Matches_AET'] += 1
                    data[home]['Home_Ties_Reg'] += 1
                    data[visitor]['Away_Ties_Reg'] += 1
                    data[home]['Home_Goals_AET'] += aethgoals - hgoals
                    data[home]['Home_Goals_Conceded_AET'] += aetvgoals - vgoals
                    data[visitor]['Away_Goals_AET'] += aetvgoals - vgoals
                    data[visitor]['Away_Goals_Conceded_AET'] += aethgoals - hgoals
                    data[home]['Home_Matches_AET'] += 1
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
        data['AET_Win_%'] = (data['Home_Wins_AET'] + data['Away_Wins_AET']) / data['Total_Matches_AET']
        data['AET_Tie_%'] = (data['Home_Ties_AET'] + data['Away_Ties_AET']) / data['Total_Matches_AET']
        data['Pens_Win_%'] = (data['Home_Wins_Pens'] + data['Away_Wins_Pens']) / data['Total_Matches_Pens']

        away_matches_reg = data['Total_Matches_Reg'] - data['Home_Matches_Reg']
        data['Away_Reg_Win_%'] = data['Away_Wins_Reg'] / away_matches_reg
        data['Home_Reg_Win_%'] = data['Home_Wins_Reg'] / data['Home_Matches_Reg']
        data['Away_Reg_Tie_%'] = data['Away_Ties_Reg'] / away_matches_reg
        data['Home_Reg_Tie_%'] = data['Home_Ties_Reg'] / data['Home_Matches_Reg']

        away_matches_AET = data['Total_Matches_AET'] - data['Home_Matches_AET']
        data['Away_AET_Win_%'] = data['Away_Wins_AET'] / away_matches_AET
        data['Home_AET_Win_%'] = data['Home_Wins_AET'] / data['Home_Matches_AET']
        data['Away_AET_Tie_%'] = data['Away_Ties_AET'] / away_matches_AET
        data['Home_AET_Tie_%'] = data['Home_Ties_AET'] / data['Home_Matches_AET']

        away_matches_pens = data['Total_Matches_Pens'] - data['Home_Matches_Pens']
        data['Away_Pens_Win_%'] = data['Away_Wins_Pens'] / away_matches_pens
        data['Home_Pens_Win_%'] = data['Home_Wins_Pens'] / data['Home_Matches_Pens']

        data['Avg_Home_Goals_Reg'] = data['Home_Goals_Reg'] / data['Home_Matches_Reg']
        data['Avg_Home_Goals_Conceded_Reg'] = data['Home_Goals_Conceded_Reg'] / data['Home_Matches_Reg']
        data['Avg_Away_Goals_Reg'] = data['Away_Goals_Reg'] / away_matches_reg
        data['Avg_Away_Goals_Conceded_Reg'] = data['Away_Goals_Conceded_Reg'] / away_matches_reg

        data['Avg_Home_Goals_AET'] = data['Home_Goals_AET'] / data['Home_Matches_AET']
        data['Avg_Home_Goals_Conceded_AET'] = data['Home_Goals_Conceded_AET'] / data['Home_Matches_AET']
        data['Avg_Away_Goals_AET'] = data['Away_Goals_Conceded_AET'] / away_matches_AET
        data['Avg_Away_Goals_Conceded_AET'] = data['Away_Goals_Conceded_AET'] / away_matches_AET

        data['Avg_Home_Goals_Pens'] = data['Home_Goals_Pens'] / data['Home_Matches_Pens']
        data['Avg_Home_Goals_Conceded_Pens'] = data['Home_Goals_Conceded_Pens'] / data['Home_Matches_Pens']
        data['Avg_Away_Goals_Pens'] = data['Away_Goals_Pens'] / away_matches_pens
        data['Avg_Away_Goals_Conceded_Pens'] = data['Away_Goals_Conceded_Pens'] / away_matches_pens

        data.to_csv('Champions_League_Processed.csv')

    return pd.read_csv('Champions_League_Processed.csv')


if __name__ == '__main__':
    process_data()