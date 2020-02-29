
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# Get the html source code from the DataSet on GitHub
champ_league = BeautifulSoup(
    requests.get('https://github.com/jalapic/engsoccerdata/blob/master/data-raw/champs.csv').text,
    features='lxml'
)

table = champ_league.find('table', class_='highlight tab-size js-file-line-container')
data = []
for tr in table.find_all('tr'):
    td = tr.find('td', class_='blob-code blob-code-inner js-file-line')
    data.append(td.get_text().replace('"', '').split(','))

df = pd.DataFrame(data[1:-2], columns=data[0])
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, yearfirst=True, errors='ignore')
print(df)
