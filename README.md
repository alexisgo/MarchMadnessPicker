# March Madness Challenge (2017)

Python project to select teams for a March Madness bracket.

## Background

Members of Hear Me Code (DC) and Code Like a Girl (Syracuse) are participating in a friendly competition to see who can programatically create the best March Madness bracket with python.

### Project

`init_team_data.py` creates the CSV file used by `build_bracekts.py`. It
builds up the list of teams, odds, win and loss history from a CBS sports website.

`build_brackets.py` is what generates predictions (currently only for the first round). Currently, it generates them simply by choosing the team with greater wins.