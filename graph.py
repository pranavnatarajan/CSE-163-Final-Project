"""
Alex Eidt- CSE 163 AC
Pranav Natarajan - CSE 163 AB

CSE 163 A
Final Project

Creates the UEFA Champions League Bracket using GraphViz and
stores it as a png file in the current directory.
"""
import os
import random
import pandas as pd
from graphviz import Digraph
from MatchTree import MatchTree
from analysis import get_data, calculate_coefficient


def create_tree_helper(tree, node):
    """
    Parameters
        tree - The Graphviz tree being built up.
        node - The MatchTree root node to build the match bracket
               tree from.
    """
    if not node.is_leaf_node():
        tree.attr('edge', arrowhead='normal', arrowsize='1.1')
        tree.attr('node', shape='box', style='rounded', color='gray90')
        tree.edge(str(node.left), str(node))
        tree.edge(str(node.right), str(node))
        create_tree_helper(tree, node.left)
        create_tree_helper(tree, node.right)


def create_tree(data, league, year):
    """
    Parameters
        data   - Pandas DataFrame mapping team names to predicted coefficients
                 from our Machine Learning Model.
        league - List of tuples showing Round of 16 Matchups for a given Champions
                 League season.
        year   - The year of the Champions League season being simulated.  

    Creates a bracket showing the winners of each round of the Champions League starting
    with the round of 16 to the final. Winners determined by who has the higher coefficient.
    """
    # Build up the MatchTree to represent the tournament simulation based on the
    # coefficients from our Machine Learning Model

    # Round of 16
    R16 = []
    for i in range(8):
        R16.append(MatchTree(data=league[i]))
    
    # Quarter finals (Round of 8)
    QF = []
    for i in range(0, 8, 2):
        QF.append(
            MatchTree(
                data=(R16[i].get_winner(data), R16[i + 1].get_winner(data)),
                left=R16[i], right=R16[i + 1]
            )
        )

    # Semi final (Round of 4)
    SF = []
    for i in range(0, 4, 2):
        SF.append(
            MatchTree(
                data=(QF[i].get_winner(data), QF[i + 1].get_winner(data)),
                left=QF[i], right=QF[i + 1]
            )
        )

    # Final (Round of 2)
    final = MatchTree(
        data=(SF[0].get_winner(data), SF[1].get_winner(data)),
        left=SF[0], right=SF[1]
    )

    # Winner of the Tournament
    winner = MatchTree(data=final.get_winner(data), left=final)

    tree = Digraph(
        graph_attr = {'rankdir':'BT', 'splines':'curved', 'overlap':'scale'},
        edge_attr = {'arrowhead': 'normal'}
    )

    winning_team = str(winner)
    tree.node(winning_team, winning_team)
    tree.attr('node', shape='box', style='rounded', color='gray90')
    tree.attr('edge', arrowhead='normal', arrowsize='1.1')
    tree.edge(str(winner.left), winning_team)
    create_tree_helper(tree, winner.left)

    tree.render(f'Champions_League_Bracket_{year}', view=False, format='png')


def main():
    # 2017-18 Champions League Round of 16 Matchups
    league_2017 = [
        ('Sevilla', 'Manchester United'),
        ('Besiktas', 'Bayern Munich'),
        ('Tottenham Hotspur', 'Juventus'),
        ('Real Madrid', 'Paris Saint-Germain'),
        ('Liverpool', 'FC Porto'),
        ('Basel', 'Manchester City'),
        ('Chelsea', 'Barcelona'),
        ('Shakhtar Donetsk', 'AS Roma')
    ]
    # 2018-19 Champions League Round of 16 Matchups
    league_2018 = [
        ('Schalke 04', 'Manchester City'),
        ('Atletico Madrid', 'Juventus'),
        ('Manchester United', 'Paris Saint-Germain'),
        ('Tottenham Hotspur', 'Borussia Dortmund'),
        ('Olympique Lyon', 'Barcelona'),
        ('AS Roma', 'FC Porto'),
        ('AFC Ajax', 'Real Madrid'),
        ('Liverpool', 'Bayern Munich')
    ]

    df = calculate_coefficient(get_data())
    df = pd.DataFrame(df['coefficient']).to_dict(orient='split')
    df = pd.DataFrame(list(zip(df['index'], df['data'])), columns=['team', 'coefficient'])
    df.set_index('team', inplace=True)
    df['coefficient'] = df['coefficient'].apply(pd.Series)
    
    # Create GraphViz Trees
    create_tree(df, league_2017, 2017)
    create_tree(df, league_2018, 2018)


if __name__ == '__main__':
    main()