import requests
import pandas as pd
import numpy as np
from explore_data import seasons, schedules
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

#cleaning dara for csv export

csv_draft_adp_merged = draft_adp_merged[['player_display_name', 'position', 'season', 'fantasy_points_ppr', 'adp_round', 'adp', 'rank', 'draft_outcome']]

csv_draft_adp_merged.to_csv('data/player_draft_analysis.csv', index=False)

#columns for table of value exports

draft_adp_merged['positional_adp_rank']= draft_adp_merged.groupby(['position', 'season'])['adp'].rank().fillna(99)
draft_adp_merged['adp_vs_finish'] = draft_adp_merged['positional_adp_rank'] - draft_adp_merged['rank']

drafted_only = draft_adp_merged[draft_adp_merged['positional_adp_rank'] != 99]
undrafted_only = draft_adp_merged[draft_adp_merged['positional_adp_rank'] == 99]

adp_vs_finish_player_value = drafted_only.groupby('position').apply(lambda x: x.nlargest(10, 'adp_vs_finish'))
adp_vs_finish_player_bust = drafted_only.groupby('position').apply(lambda x : x.nsmallest(10, 'adp_vs_finish'))

values_display = (adp_vs_finish_player_value[['player_display_name', 'position', 'season', 'positional_adp_rank', 'rank','adp_vs_finish', 'draft_outcome']]
                  .rename(columns={'player_display_name': 'Player', 'position':'Position', 'season':'Season',
                                   'positional_adp_rank': 'ADP by Position', 'rank': 'Seasonal Ranking', 'adp_vs_finish': 'Draft vs Finish','draft_outcome':'Seasonal Outcome' }))

busts_display = (adp_vs_finish_player_bust[['player_display_name', 'position', 'season', 'positional_adp_rank', 'rank','adp_vs_finish', 'draft_outcome']]
                  .rename(columns={'player_display_name': 'Player', 'position':'Position', 'season':'Season',
                                   'positional_adp_rank': 'ADP by Position', 'rank': 'Seasonal Ranking', 'adp_vs_finish': 'Draft vs Finish','draft_outcome':'Seasonal Outcome' }))

undrafted_display = (undrafted_only[['player_display_name', 'position', 'season', 'rank', 'fantasy_points_ppr', 'draft_outcome']]
                     .rename(columns={'player_display_name': 'Player', 'position':'Position', 'season':'Season', 'rank':'Seasonal Ranking',
                                      'fantasy_points_ppr':'Seasonal Fantasy Points', 'draft_outcome':'Seasonal Outcome' }))

with open('data/top_values_busts.md', 'w') as f:
    f.write(f"## Top 10 Values by Position (drafted players)\n\n")
    f.write(values_display[['Player', 'Position', 'Season', 'ADP by Position', 'Seasonal Ranking','Draft vs Finish', 'Seasonal Outcome']].to_markdown(index=False))
    f.write(f'\n\n## Top 10 Busts by Position (drafted players)\n\n')
    f.write(busts_display[['Player', 'Position', 'Season', 'ADP by Position', 'Seasonal Ranking','Draft vs Finish', 'Seasonal Outcome']].to_markdown(index=False))
    f.write(f'\n\n## Top 10 Undrafted Player Values by Position\n\n')
    f.write(undrafted_display[['Player', 'Position', 'Season', 'Seasonal Fantasy Points', 'Seasonal Outcome']].to_markdown(index=False))

#creating teams w/l ratio


home_team_perspective = schedules[['season', 'home_team', 'result']].rename(columns={'home_team': 'team'})


away_team_perspective = schedules[['season', 'away_team', 'result']].rename(columns={'away_team': 'team'})


away_team_perspective['result'] = away_team_perspective['result'] * -1

results_df = pd.concat([home_team_perspective, away_team_perspective])
results_df['win'] = np.where(results_df['result']>0, 1, 0)



team_wins = results_df.groupby(['team', 'season'])['win'].agg(['sum', 'count']).reset_index(drop = False)
team_wins = team_wins.rename(columns={'sum':'wins', 'count':'games_played'})
team_wins['wl_ratio'] = team_wins['wins'] / team_wins['games_played']

draft_adp_merged = pd.merge(draft_adp_merged, team_wins, on=['team', 'season'], how = 'left')
