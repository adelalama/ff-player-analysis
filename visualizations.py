import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from explore_data import fantasy_starters
from explore_data import position_starters
from explore_data import position_depth


overall_position_mean = fantasy_starters.groupby(['position'])['position_starter_mean'].mean()

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

