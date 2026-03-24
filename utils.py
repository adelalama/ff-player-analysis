import pandas as pd

def build_player_pool(season_totals, pool_dict, mean_dict):
    player_pool = season_totals[season_totals['rank']<= season_totals['position'].map(pool_dict)]
    starter_pool = season_totals[season_totals['rank']<= season_totals['position'].map(mean_dict)]

    yearly_position_mean = starter_pool.groupby(['position', 'season'])['fantasy_points_ppr'].mean().reset_index()
    yearly_position_mean = yearly_position_mean.rename(columns={'fantasy_points_ppr':'position_starter_mean'})

    player_pool = player_pool.merge(yearly_position_mean, on= ['position', 'season'])
    player_pool['mean_differential'] = player_pool['fantasy_points_ppr'] - player_pool['position_starter_mean']
    player_pool = player_pool.sort_values(by=['season', 'position', 'rank'])
    player_pool['rank'] = player_pool['rank'].astype(int)
    player_pool = player_pool[['rank', 'player_display_name', 'team', 'position', 'season', 'fantasy_points_ppr',
                               'position_starter_mean', 'mean_differential']].reset_index(drop=True)
    player_pool['season_label'] = player_pool['season'].astype(str) + ' Season'

    return player_pool

def clean_name (name):
    suffixes = ['Jr.', 'Sr.', 'III', 'II', 'IV']
    special_chars = ["'",'-', '.']

    for suffix in suffixes:
        name = name.replace(suffix, '')

    for special_char in special_chars:
        name = name.replace(special_char, '')

    name = name.lower()
    name = name.strip()

    return name

def classify_draft_outcome(row):
    position = row['position']
    rank = row['rank']
    adp_formatted = row['adp_formatted']
    adp = row['adp']

    if pd.isna(adp_formatted):
        if position in ['RB', 'WR'] and rank <= 12:
            return 'Season Winner'
        elif position in ['RB', 'WR'] and rank <= 24:
            return 'Big Value'
        elif position == 'QB' and rank <= 6:
            return 'Big Value'
        elif position == 'TE' and rank <= 6:
            return 'Big Value'
        return None

    round_number = int(adp_formatted.split('.')[0])

    if position == 'QB':
        if round_number <= 5 and rank > 8:
            return 'Big Bust'
        elif round_number >= 9 and rank <= 6:
            return 'Big Value'

    elif position == 'TE':
        if round_number <= 4 and rank > 6:
            return 'Big Bust'
        elif round_number >= 9 and rank <= 6:
            return 'Big Value'

    elif position in ['RB', 'WR']:
        if (adp <= 8 and rank > 24) or (9 <= adp <=14 and rank > 30):
            return 'Season Ender'
        elif 9 <= adp <= 36 and rank > 24:
            return 'Big Bust'
        elif adp >= 74 and rank <= 12:
            return 'Season Winner'
        elif (37 <= adp <= 72 and rank <= 12) or (adp >= 74 and 13 <= rank <= 24):
            return 'Big Value'
        elif 37<= adp <= 72  and 13<= rank <= 20:
            return 'Value'
        elif 37 <= adp <= 72 and rank > 36:
            return 'Bust'

    return None



