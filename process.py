"""
Alex Eidt
Pranav Natarajan

CSE 163 AC
Final Project

Processes the dataset to prepare it for our
calculations and analysis.
"""


from gather import gather_data


def process_data():
    """
    Processes the Champions League Dataset.

    Returns
        A pandas DataFrame representing the filtered
        dataset.
    """
    df = gather_data()

    # All Champions League Seasons before 1994 were in a
    # different format than the curret competition.
    # Our analysis will therefore only look at matches
    # from 1992 to present.
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


if __name__ == '__main__':
    process_data()

