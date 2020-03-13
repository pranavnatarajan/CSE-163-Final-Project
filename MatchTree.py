class MatchTree:

    def __init__(self, data=None, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_winner(self, data):
        team1, team2 = self.data
        team1_coefficient = data.loc[team1].squeeze()
        team2_coefficient = data.loc[team2].squeeze()
        if team1_coefficient > team2_coefficient:
            return team1
        elif team1_coefficient < team2_coefficient:
            return team2
        return team1

    def is_leaf_node(self):
        return self.left == None and self.right == None

    def __str__(self):
        if type(self.data) != str:
            return f'{self.data[0]}\nvs.\n{self.data[1]}'
        return self.data