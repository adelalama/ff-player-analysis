# ff-player-analysis
Season long point differential analysis by top scorers in each position

![Position Differential Chart](images/position_differential.png)

![FLEX Analysis Chart](images/flex_analysis.png)

## Data Limitations

- ADP data sourced from Fantasy Football Calculator API for QB, RB, WR and TE positions.
  Data gaps exist for some players in certain seasons, resulting in an approximate 88% match rate for starters and an 
  approximate 75% for the full draft pool.
- Missing ADP values are a mix of data gaps, undrafted players and rookies.
  

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