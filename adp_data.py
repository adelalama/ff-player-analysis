import requests
import pandas as pd
from explore_data import seasons
from explore_data import fantasy_starters
from utils import clean_name, classify_draft_outcome
from explore_data import flex_players

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
starters_adp_merged = fantasy_starters.merge(adp_data, on=['clean_name', 'season'], how='left')

#adding full player depth for 15 round draft
flex_players['clean_name'] = flex_players['player_display_name'].apply(clean_name)
draft_adp_merged = flex_players.merge(adp_data, on=['clean_name', 'season'], how='left')

# print(draft_adp_merged.shape)
# print(draft_adp_merged['adp'].isna().sum())
missing_adp = draft_adp_merged[draft_adp_merged['adp'].isna()]
# print(missing_adp.groupby(['position', 'season']).size())


draft_adp_merged['draft_outcome'] = draft_adp_merged.apply(classify_draft_outcome, axis = 1)

# print(draft_adp_merged.head(20))
# print(draft_adp_merged[draft_adp_merged['position'] == 'QB']['draft_outcome'].value_counts())
# print(draft_adp_merged['draft_outcome'].value_counts())
# print(draft_adp_merged.groupby(['position', 'draft_outcome']).size())

# print(draft_adp_merged.head(15))
outcome_counts = (draft_adp_merged[draft_adp_merged['draft_outcome'].notna()].groupby(['position','draft_outcome'])
                  .size().reset_index(name = 'count'))

outcome_counts = outcome_counts.rename(columns = {'position': 'Position'})
#print(outcome_counts.head(25))