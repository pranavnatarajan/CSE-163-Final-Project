"""
Alex Eidt
Pranav Natarajan

CSE 163 AC
Final Project

Checks if the dataset required for the analysis is present in the
current directory. If not, data is parsed into a pandas DataFrame
and a csv file with the data is created in the current directory.
"""


import requests
import os
import pandas as pd
from bs4 import BeautifulSoup


def gather_data():
    """
    Checks if the Champions League Dataset necessary for the analysis is
    in the current directory. If not, the GitHub Page containing the
    data (https://github.com/jalapic/engsoccerdata/blob/master/data-raw/champs.csv)
    is parsed into a pandas DataFrame and a csv file with the data is
    created in the current directory.

    Raises an Exception if there is no Internet Connection.

    Returns
        A Pandas DataFrame representing the Champions League Dataset.
    """
    if 'champions_league_dataset.csv' not in os.listdir(os.getcwd()):
        # Get the html source code from the DataSet on GitHub
        try:
            champ_league = BeautifulSoup(
                requests.get('https://github.com/jalapic/engsoccerdata/blob/master/data-raw/champs.csv').text,
                features='lxml'
            )
        except Exception:
            raise Exception('No Internet Connection. Cannot access online data. ' + \
                            'Make sure Internet is connected. Data available at: ' + \
                            'https://github.com/jalapic/engsoccerdata/blob/master/data-raw/champs.csv')
        else:
            table = champ_league.find('table', class_='highlight tab-size js-file-line-container')
            data = []
            for tr in table.find_all('tr'):
                td = tr.find('td', class_='blob-code blob-code-inner js-file-line')
                data.append(td.get_text().replace('"', '').split(','))

            df = pd.DataFrame(data[1:-2], columns=data[0])
            df.to_csv('champions_league_dataset.csv')

    return pd.read_csv('champions_league_dataset.csv', na_values='NA')


if __name__ == '__main__':
    gather_data()