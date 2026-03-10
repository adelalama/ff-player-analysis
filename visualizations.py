import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from explore_data import fantasy_starters
from explore_data import flex_players
from explore_data import position_starters
from explore_data import flex_depth
from explore_data import seasons



overall_position_mean = fantasy_starters.groupby(['position'])['position_starter_mean'].mean()
flex_position_mean = flex_players[flex_players['rank']>24].groupby(['position'])['fantasy_points_ppr'].mean()
flex_data = flex_players[flex_players['position'].isin(['RB', 'WR'])]

#starters visualizations
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2,2, figsize=(14,10))
axes = axes.flatten()

for idx, positions in enumerate(position_starters):
    position_data = fantasy_starters[fantasy_starters['position'] == positions]
    sns.lineplot(data=position_data,x='rank',y='fantasy_points_ppr',hue='season_label', ax=axes[idx])
    axes[idx].set_title(f'{positions} Mean Differential by Rank 2019-2023')
    axes[idx].set_xlabel('Rank')
    axes[idx].set_ylabel('Fantasy PPR Points')
    axes[idx].axhline(y=overall_position_mean[positions], linewidth=1, color='red', linestyle='--',
                      label='Position Mean 2019-2023')
    axes[idx].legend()

fig.suptitle('Fantasy Football PPR Point Differential by Position 2019-2023',
             fontsize=14, fontweight='bold')
fig.text(.5, .9475, '12 Team League - Standard Roster (QB/RB/RB/WR/WR/TE/FLEX)', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('images/position_differential.png', dpi=150, bbox_inches='tight' )
plt.show()

#flex range visualizations

sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(3,2, figsize=(14,10))
axes = axes.flatten()

for idx, season in enumerate(seasons):
    season_data = flex_data[flex_data['season'] == season]
    sns.lineplot(data=season_data,x='rank', y='fantasy_points_ppr', hue = 'position', ax=axes[idx])
    axes[idx].set_title(f'FLEX PPR points for {season} Season')
    axes[idx].set_xlabel('Rank')
    axes[idx].set_ylabel('Fantasy PPR Points')
    axes[idx].axvline(x=24, linewidth=1, color='blue', linestyle='--')
    axes[idx].axhline(y=flex_position_mean['RB'], linewidth=1, color='red', linestyle='--', label='RB FLEX Mean')
    axes[idx].axhline(y=flex_position_mean['WR'], linewidth=1, color='green', linestyle='--', label='WR FLEX Mean')
    axes[idx].legend()

axes[5].set_visible(False)
fig.suptitle('WR vs RB FLEX Value in PPR Leagues (2019-2023)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('images/flex_analysis.png', dpi=150, bbox_inches='tight' )
plt.show()
