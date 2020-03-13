
import os
import random
import pandas as pd
from graphviz import Digraph
from MatchTree import MatchTree

# Change PATH setup for Graphviz folder here:
# --------------------------GRAPHVIZ PATH SETUP------------------------- #
os.environ['PATH'] += os.pathsep + 'C:\\Graphviz\\bin'
# ---------------------------------------------------------------------- #

def create_tree(tree, node):
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
        create_tree(tree, node.left)
        create_tree(tree, node.right)


def main(data, league):
    """
    Parameters
        data -   Pandas DataFrame mapping team names to predicted coefficients
                 from our Machine Learning Model.
        league - List of tuples showing Round of 16 Matchups for a given Champions
                 League season.

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
    create_tree(tree, winner.left)

    tree.render('Champions_League_Bracket', view=False, format='png')


if __name__ == '__main__':
    # 2018-19 Champions League Round of 16 Matchups
    league = [
        ('Schalke 04', 'Manchester City'),
        ('Atletico Madrid', 'Juventus'),
        ('Manchester United', 'Paris Saint-Germain'),
        ('Tottenham Hotspur', 'Borussia Dortmund'),
        ('Olympique Lyon', 'Barcelona'),
        ('AS Roma', 'FC Porto'),
        ('AFC Ajax', 'Real Madrid'),
        ('Liverpool', 'Bayern Munich')
    ]
    teams = []
    for x, y in league:
        teams.append(x)
        teams.append(y)
    coefficients = []
    for team in teams:
        coefficients.append([team, random.random() * (random.random() + (5 * random.random()))])
    coefficients = pd.DataFrame(coefficients, columns=['team', 'coefficient'])
    coefficients.set_index('team', inplace=True)
    main(coefficients, league)