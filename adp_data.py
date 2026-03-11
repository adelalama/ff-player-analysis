import requests
import pandas as pd
from explore_data import seasons
from explore_data import fantasy_starters
from utils import clean_name

# response = requests.get('https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year=2019').json()

# print(type(response))
# print(response.keys())
# print(response['players'][0])

# adp_2019 = pd.DataFrame(response['players'])
# print(adp_2019.head(20))

all_adp = []

for season in seasons:
    response = requests.get(f'https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year={season}').json()
    response = pd.DataFrame(response['players'])
    response['season'] = season
    all_adp.append(response)

adp_data = pd.concat(all_adp)
adp_data = adp_data[['name', 'position', 'adp','adp_formatted','season']]
adp_data = adp_data[adp_data['position'].isin(['QB', 'RB', 'WR', 'TE'])]
adp_data = adp_data.drop(columns=['position'])


#name cleaning for merge
fantasy_starters['clean_name'] = fantasy_starters['player_display_name'].apply(clean_name)
adp_data['clean_name'] = adp_data['name'].apply(clean_name)

# print(fantasy_starters.head(30))
# print(adp_data.head(15))
#
adp_merged = fantasy_starters.merge(adp_data, on=['clean_name', 'season'], how='left')

#print(adp_merged.head(15))
# print(adp_data[adp_data['clean_name'] == 'aaron jones'])
# print(fantasy_starters[fantasy_starters['clean_name'] == 'aaron jones'])

# print(adp_merged[adp_merged['adp'].isna()][['player_display_name', 'position', 'season']])
# print(adp_merged['adp'].isna().sum())
print(adp_data[adp_data['clean_name'].str.contains('kirk')])
print(adp_data[adp_data['season'] == 2020]['clean_name'].str.contains('kirk').sum())