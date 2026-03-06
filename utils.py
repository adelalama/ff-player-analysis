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

