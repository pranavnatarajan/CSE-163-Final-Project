"""
Alex Eidt- CSE 163 AC
Pranav Natarajan - CSE 163 AB

CSE 163 A
Final Project

This class represents a Data Structure used to build up the bracket
of the UEFA Champions League to create the bracket graphics.
"""
import random


class MatchTree:
    """
    Data Structure used to represent a full bracket of the UEFA Champions
    League with every node representing a game.
    """
    def __init__(self, data=None, left=None, right=None):
        """
        Initializes the MatchTree class with a left and right MatchTree Node,
        and a 'data' field which stores the String representing the teams
        facing off in that Match.
        """
        self.left = left
        self.right = right
        self.data = data

    def get_winner(self, data):
        """
        Determines the winner of a Match in the MatchTree node based
        on the coefficient data in 'data'.

        Parameter
            data - Pandas DataFrame representing coefficients for every
                   team in the MatchTree bracket.

        Returns
            The winning team as a String based on whose coefficient is greater.
            If both coefficients are exactly the same, this is equivalent to
            the match going to penalty kicks to be decided. Penalty kicks have little to
            do with a teams strength (and thus coefficient). Penalty kicks are about
            who can make the big shots in the big moments and comes down to mostly
            luck. This behavior is simulated by randomly choosing one team if both
            coefficients are exactly the same.
        """
        team1, team2 = self.data
        team1_coefficient = data.loc[team1].squeeze()
        team2_coefficient = data.loc[team2].squeeze()
        if team1_coefficient > team2_coefficient:
            return team1
        elif team1_coefficient < team2_coefficient:
            return team2
        return random.choice(self.data)

    def is_leaf_node(self):
        """
        Returns
            True if the current MatchTree node is a leaf node (no children).
            Otherwise returns False.
        """
        return self.left == None and self.right == None

    def __str__(self):
        """
        Returns
            A String representation of the data in the MatchTree node.
            If the data is a tuple, this represents a match and a String
            of the format "Team A vs. Team B" is returned.
            If the data is a String, this represents the winner of the
            bracket and so this value is simply returned.
        """
        if type(self.data) != str:
            return f'{self.data[0]}\nvs.\n{self.data[1]}'
        return str(self.data)