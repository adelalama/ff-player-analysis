import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from explore_data import fantasy_starters
from explore_data import flex_players
from explore_data import position_starters
from explore_data import flex_depth
from explore_data import seasons
from adp_data import outcome_counts, se_list, draft_adp_merged
from adp_data import busts_by_round, values_by_round, season_winners, season_enders



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

#bust/value visualizations

sns.set_theme(style="darkgrid")

sns.barplot(outcome_counts, x = 'draft_outcome' , y = 'count', hue = 'Position', order= ['Season Winner', 'Big Value', 'Value',
                                                                                         'Season Ender', 'Big Bust', 'Bust'] )
plt.title('Draft Value/Bust by position 2019-2023', fontsize=14, fontweight='bold')
plt.xlabel('Draft Outcome')
plt.ylabel('Count')

plt.tight_layout()
plt.savefig('images/bust_value_by_position.png', dpi=150, bbox_inches='tight' )
plt.show()

#season winners enders by round

sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(1,2, figsize=(12,8))

for idx, (data, title) in enumerate(zip([season_enders, season_winners], ['Season Enders 2019-2023', 'Season Winners 2019-2023'])):
    sns.barplot(data, x = 'adp_round', y = 'count', hue = 'position', ax=axes[idx], errorbar= None)

    axes[idx].set_title(title)
    axes[idx].set_xlabel('Round')
    axes[idx].set_ylabel('Count')
    axes[idx].legend()
    current_labels = axes[idx].get_xticklabels()
    axes[idx].set_xticks(axes[idx].get_xticks())
    labels = ['Undrafted' if label.get_text() == '16.0' else int(float(label.get_text())) for label in current_labels]
    axes[idx].set_xticklabels(labels)


axes[0].text(.285, 5.65, s=se_list, fontsize=10, bbox={'facecolor': '#EAEAF2', 'edgecolor': '#CCCCCC', 'boxstyle': 'round'})
print(axes[0].get_xlim())
print(axes[0].get_ylim())


fig.suptitle('Season Enders & Winners by Draft Capital (2019-2023)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('images/season_enders_winners_by_draft_capital.png', dpi=150, bbox_inches='tight' )
plt.show()

#busts/values by round

sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2,2, figsize=(14,12))
axes = axes.flatten()

for idx, (data, title) in enumerate(zip([busts_by_round[busts_by_round['draft_outcome'] == 'Big Bust'],
                                         values_by_round[values_by_round['draft_outcome'] == 'Big Value'],
                                         busts_by_round[busts_by_round['draft_outcome'] == 'Bust'],
                                         values_by_round[values_by_round['draft_outcome'] =='Value']],
                                        ['Big Bust by Round', 'Big Value by Round', 'Bust by Round','Value by Round'])):
    sns.barplot(data, x = 'adp_round', y = 'count', hue = 'position', ax=axes[idx], errorbar= None)

    axes[idx].set_title(title)
    axes[idx].set_xlabel('Round')
    axes[idx].set_ylabel('Count')
    axes[idx].legend()


fig.suptitle('Bust/Value by Round for each position (2019-2023)',
             fontsize=14, fontweight='bold')
plt.savefig('images/bust_value_by_round_for_position.png', dpi=150, bbox_inches='tight' )
plt.tight_layout(pad = 3)
plt.show()

#winning team correlation to fantasy points
sns.set_theme(style="darkgrid")
s_plot = sns.lmplot(data = draft_adp_merged, x= 'wl_ratio', y= 'fantasy_points_ppr', hue = 'position',
                    scatter_kws={'alpha': .5}, height=8, aspect= 1.5)
s_plot.figure.suptitle('Winning Team Correlation to Fantasy Points by Position (2019-2023)',
             fontsize=14, fontweight='bold')
s_plot.set_xlabels('Win/loss Ratio')
s_plot.set_ylabels('Fantasy Points PPR')
s_plot.legend.set_bbox_to_anchor((.975, .9))
s_plot._legend.set_title('Position')
s_plot.ax.axvline(x =.5, color = 'red', linestyle = 'dashed', linewidth = 1, label='.500 Win Rate', alpha = 0.5)

plt.savefig('images/winning_team_correlation_to_fp_by_position.png', dpi=150, bbox_inches='tight' )
plt.tight_layout()
plt.show()