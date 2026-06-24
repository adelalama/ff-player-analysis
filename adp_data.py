import requests
import pandas as pd
import numpy as np
from explore_data import seasons
from explore_data import fantasy_starters
from utils import clean_name, classify_draft_outcome
from explore_data import flex_players

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

starters_adp_merged = fantasy_starters.merge(adp_data, on=['clean_name', 'season'], how='left')

#adding full player depth for 15 round draft
flex_players['clean_name'] = flex_players['player_display_name'].apply(clean_name)
draft_adp_merged = flex_players.merge(adp_data, on=['clean_name', 'season'], how='left')

missing_adp = draft_adp_merged[draft_adp_merged['adp'].isna()]

draft_adp_merged['draft_outcome'] = draft_adp_merged.apply(classify_draft_outcome, axis = 1)

outcome_counts = (draft_adp_merged[draft_adp_merged['draft_outcome'].notna()].groupby(['position','draft_outcome'])
                  .size().reset_index(name = 'count'))

outcome_counts = outcome_counts.rename(columns = {'position': 'Position'})

draft_adp_merged['adp_round'] = pd.to_numeric(draft_adp_merged['adp_formatted'].str.split('.').str[0], errors='coerce')

draft_adp_merged['adp_round'] = np.where((draft_adp_merged['adp_round'].isna()) & (draft_adp_merged['draft_outcome'].notna()), 16, draft_adp_merged['adp_round'])

outcome_by_round = (draft_adp_merged[draft_adp_merged['draft_outcome'].notna()].groupby(['position', 'draft_outcome', 'adp_round'])
                    .size().reset_index(name = 'count'))


season_enders = outcome_by_round[outcome_by_round['draft_outcome'] == 'Season Ender']
season_winners = outcome_by_round[outcome_by_round['draft_outcome'] == 'Season Winner']
busts_by_round = outcome_by_round[outcome_by_round['draft_outcome'].isin(['Big Bust', 'Bust'])]
values_by_round = outcome_by_round[outcome_by_round['draft_outcome'].isin(['Big Value', 'Value'])]


#adding name tags to season enders
se_list = ("List of Season Enders: \nRB R1: Conner ('19), Johnson ('19), CMC ('20), \nCMC ('21), CMC ('22), Taylor ('22), Ekeler ('23)\n"
            "RB R2: Mixon ('20)\n"
            "WR R1: Jefferson ('23), Kupp ('23)\n"
            "WR R2: Hill ('19)")



#print(draft_adp_merged[draft_adp_merged['draft_outcome'] == 'Season Ender'][['player_display_name', 'position', 'season', 'adp_round']])
# print(season_winners[season_winners['adp_round'] == 16])
# print(draft_adp_merged[(draft_adp_merged['position'] == 'RB') & (draft_adp_merged['adp_round']>=4) & (draft_adp_merged['adp_round']<=6) & (draft_adp_merged['rank']<18)].shape)
# print(draft_adp_merged['draft_outcome'].value_counts())
# print(draft_adp_merged[draft_adp_merged['draft_outcome'] == 'Value'].groupby('position'))
#print(outcome_by_round[outcome_by_round['draft_outcome'].isin(['Season Winner', 'Season Ender'])])
#print(draft_adp_merged[(draft_adp_merged['rank'] >= 30) & (draft_adp_merged['adp']< 18)].shape)
# print(draft_adp_merged[draft_adp_merged['adp_round'] == 16])
# print(draft_adp_merged[(draft_adp_merged['adp_round'] == 16) & (draft_adp_merged['position'].isin(['QB', 'TE']))]['draft_outcome'].value_counts())