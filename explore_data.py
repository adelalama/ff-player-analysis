import nfl_data_py as nfl

seasons = [2019, 2020, 2021, 2022, 2023]
#data = nfl.import_seasonal_data(seasons)
weekly = nfl.import_weekly_data(seasons)

# #season
# print(data['season'].unique())
# print(data.shape)
# print(data.columns.tolist())
# print(data.head())


# weekly
print(weekly['position'].unique())
print(weekly.columns.tolist())

# cmc = weekly['player_name'] == 'McCaffrey'
# print(cmc)
