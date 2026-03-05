import nflreadpy as nfl
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

seasons = [2019, 2020, 2021, 2022, 2023]
position_starters = {'QB': 12, 'RB': 24, 'WR': 24, 'TE': 12}

# Data loading
players = nfl.load_player_stats(seasons)
players = players.to_pandas()

# data cleaning
players_clean = players[players['season_type'] == "REG"]
players_clean = players_clean[['player_id', 'player_display_name', 'position', 'season',
                               'week', 'team', 'fantasy_points_ppr']]
position_filter = players_clean[players_clean['position'].isin(['QB', 'WR', 'RB', 'TE'])]

# Data transformation
season_totals = position_filter.groupby(['player_id', 'player_display_name', 'position', 'season', 'team'])[
    'fantasy_points_ppr'].sum().reset_index()

season_totals['rank'] = season_totals.groupby(['season', 'position'])['fantasy_points_ppr'].rank(ascending=False)

fantasy_starters = season_totals[season_totals['rank'] <= season_totals['position'].map(position_starters)]

yearly_position_mean =  fantasy_starters.groupby(['position', 'season'])['fantasy_points_ppr'].mean().reset_index()
yearly_position_mean = yearly_position_mean.rename(columns={'fantasy_points_ppr': 'position_starter_mean'})

fantasy_starters = fantasy_starters.merge(yearly_position_mean, on =['position', 'season'])
fantasy_starters['mean_differential'] = fantasy_starters['fantasy_points_ppr'] - fantasy_starters['position_starter_mean']
fantasy_starters = fantasy_starters.sort_values(by=['season', 'position', 'rank'])
fantasy_starters['rank'] = fantasy_starters['rank'].astype(int)
fantasy_starters = fantasy_starters[['rank', 'player_display_name', 'team', 'position', 'season', 'fantasy_points_ppr',
                                     'position_starter_mean', 'mean_differential']].reset_index(drop=True)
print(fantasy_starters.head(20))

