# Fantasy Football Draft Intelligence: A 5 Year PPR Analysis

## Overview

Fantasy football drafts are won and lost on research, the goal of this project is to turn five years of fantasy data into actionable insights you can use on your draft strategy. 

The data used for this project covers information from the 2019-2023 NFL seasons and was extracted from nflreadpy, a Python package that lets you extract information from the nflverse repositories.

This analysis lets you gain an edge by giving insights or answering the following questions:
- At what round does production drop off at each position?
- When is it worthwhile to reach for the top players of a position (QB/TE)?
- Which rounds provide the most value and highest bust risk?
- Which positions should be prioritized in early vs late round?
- Are there rounds where a specific position has had higher potential for values?
-How does an NFL team's win/loss ratio affect fantasy production for different positions?

By understanding these patters you will be able to make data driven decisions on draft day that can make the difference when it comes to winning your fantasy football league.

## Key Findings

- Understanding the QB position is instrumental to building a solid fantasy team. This position is the most highly 
correlated with an NFL teams win/loss ratio, and it's the position with the most consistent production among starting players. 
This indicates that the best recipe for selecting a QB is waiting for the later rounds and choosing QBs in efficient offenses,
or offenses with high potential (young players, changes to GM or head coach).


- Having an elite QB/TE is an incredible boost for any fantasy team, but given the draft capital required to get them
and the subtle drop off / high amount of sleepers at later rounds at both positions, its almost never worth the cost.


- A top 5 RB is one of the most valuable assets in a fantasy team, given our win/loss correlation analysis we can determine
that the difference between a top 12 RB and a top 5 RB is a NFL team with a strong offense and touchdown opportunities. 
Regardless of individual player talent, a RB needs touchdown opportunities to break the top 5 threshold. 


- For PPR leagues, the FLEX spot should almost always be a WR, the average difference between the RB and WR position in 
these ranges is approximately 35 ppr points per season, which could be weekly winning upside.


- The WR position provides the highest value opportunity. Many of the RB values in our data-set exist because
of the injury prone nature of the RB position. WR values tend to emerge from a breakout season, more opportunities resulting
from a strong offense, or good chemistry with the QB. Making this value more predictable and reliable.


- Round 7-8 are the pot of gold for season winners, with a total of ten players (RB and WR) drafted in these rounds that
had season winning upside.


- The riskiest rounds for drafting WRs is surprisingly round 2 and 3, with a total of 13 players that were categorized 
as big busts in these ranges. Also, surprisingly round 4 is the round with the highest occurrence of big values at the position.


- Season enders are a phenomenon almost exclusive to round 1 and 2, most of these are caused by injury. The most important
factors to consider when drafting in these rounds is to stray from older players, players who are changing teams or have 
a huge change in their offensive ecosystem(rookie QB, new Head Coach) and most importantly, injury prone players. 


- Regarding injury prone players, it is important to mention players like Christian McCaffrey are boom or bust, he was 
tagged as a season ender in 3 seasons, but on his only fully healthy season he was nearly 155 points over the second ranked RB.
This kind of advantage on a single player is season winning upside.


- The WR position is the one least affected by an NFL teams win/loss ratio. Garbage time and catch up game plans help offset
lack of points and touchdowns in inefficient offenses.
## Visualizations

### PPR Point Differential by Position (2019-2023)

placeholder

![Position Differential Chart](images/position_differential.png)

### Flex Analysis By Season

placeholder

![Flex Analysis By Season](images/flex_analysis.png)

### Draft Outcome By Position

placeholder

![Draft Outcome By Position](images/bust_value_by_position.png)

### Season Winners/Enders By Draft Capital

placeholder

![Season Winners/Enders By Draft Capital](images/season_enders_winners_by_draft_capital.png)

### Bust/Values By Round in Draft

placeholder

![Bust/Values By Round in Draft](images/bust_value_by_round_for_position.png)
## Data Sources

## Data Limitations

- ADP data sourced from Fantasy Football Calculator API for QB, RB, WR and TE positions.
  Data gaps exist for some players in certain seasons, resulting in an approximate 88% match rate for starters and an 
  approximate 75% for the full draft pool.
- Missing ADP values are a mix of data gaps, undrafted players and rookies.

## Methodology

## Setup and Installation

## Technologies Used

## Roadmap 

#Roadmap
v2 
build draft outcome classifier (value/bust)
bust by round visualization
value by round visualization
csv and Markdown of value/busts

v2.5 
positional draft composition by round (first 3, % of picks going to which position)
Trends: Does early TE/QB offer advantage?

v3
how does nfl team win/loss record correlate with fantasy performance
does a winning team = more fantasy points
does a winning team help RB or WR more

NOTES:
WR is a sketch and risky position to draft. HUGE amount of big busts in round 2 and 3 why there are a HUGE number of big values on round 4. Never draft a wr round 2-3 unless you are CERTAIN of production. Always take a risk in round 4 with wr.
In the same way drafting qb and te early is way to risky for the possible pay off you can get on both positions starting round 9ish. Thats on the big bust value side of things
On the bust and value side of things, ithere is an implicit risk while drafting in these middle rounds, having informed decisions on these rounds is the difference between drafting a usefull player and a dud