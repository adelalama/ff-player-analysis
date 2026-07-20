import nflreadpy as nfl
import pandas as pd
from utils import build_player_pool

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

seasons = [2019, 2020, 2021, 2022, 2023]
position_starters = {'QB': 12, 'RB': 24, 'WR': 24, 'TE': 12}
flex_depth = {'QB': 24, 'RB': 60, 'WR': 60, 'TE': 24}

# data loading
players = nfl.load_player_stats(seasons)
players = players.to_pandas()
schedules = nfl.load_schedules(seasons).to_pandas()
schedules = schedules[schedules['game_type'] == 'REG']

# data cleaning
players_clean = players[players['season_type'] == "REG"]
players_clean = players_clean[['player_id', 'player_display_name', 'position', 'season',
                               'week', 'team', 'fantasy_points_ppr']]
players_clean = players_clean[players_clean['position'].isin(['QB', 'WR', 'RB', 'TE'])]

# data transformation
season_totals = players_clean.groupby(['player_id', 'player_display_name', 'position', 'season', 'team'])[
    'fantasy_points_ppr'].sum().reset_index()

season_totals['rank'] = season_totals.groupby(['season', 'position'])['fantasy_points_ppr'].rank(ascending=False)

fantasy_starters = build_player_pool(season_totals, position_starters, position_starters)
flex_players = build_player_pool(season_totals, flex_depth, position_starters)



