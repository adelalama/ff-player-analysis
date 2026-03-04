import nflreadpy as nfl

seasons = [2019, 2020, 2021, 2022, 2023]

players = nfl.load_player_stats(seasons)
players = players.to_pandas()

# print(players.shape)
# print(players.head())
# print(players.columns)
# # print(players['season'])
# # # solid_players = players['fantasy_points'] > 25
# # # print(solid_players)
# #
# print(players[players['fantasy_points']>25])

# print(players['season'].unique())

# print(players.columns)
# print(players['season_type'].head())


players_clean = players[players['season_type'] == "REG"]
players_clean = players_clean[['player_id', 'player_display_name', 'position', 'season',
                               'week', 'team', 'fantasy_points_ppr']]

# print(players_clean.shape)
# print(players_clean.head())

position_filter = players_clean[players_clean['position'].isin(['QB', 'K', 'WR', 'RB', 'TE'])]

season_totals = position_filter.groupby(['player_id', 'player_display_name', 'position', 'season', 'team'])[
    'fantasy_points_ppr'].sum().reset_index()

print(season_totals.head())
