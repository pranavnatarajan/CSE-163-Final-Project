# Champions League Data Analysis Project
## Alex Eidt and Pranav Natarajan

[To view the presentation slides, plese look at `UEFA Champions League Data Analysis Project.pdf`]

Data Specification:
***

Key | Description
--- | ---
Reg | Regulation. If something has this tag, that means that there was a winner after 90 mins (Regulation).
AET | Added Extra Time. If something has this tag, that means there was a winner after 120 mins (Added Extra Time). This means that there was a tie during regulation.
Pens | Penalty Kicks. If something has this tag, that means the game was decided on penalty kicks and therefore implies that the game was tied at the end of AET.

***

This is all the data we have for EVERY team.

Column Name | Description
--- | ---
Total_Matches | Total Matches
Total_Matches_Reg | Total Matches that ended in Regulation. (If a game ended in AET, this does not increment the **Total_Matches_Reg**)
Home_Matches_Reg | Total Home matches that ended in Regulation. 
Home_Wins_Reg | Home wins during regulation.
Home_Ties_Reg | Home ties during regulation. If a game goes into AET, then this counts as a tie during regulation.
Away_Wins_Reg | Away wins during regulation.
Away_Ties_Reg | Away ties during regulation. If a game goes into AET, then this counts as a tie during regulation.
Home_Goals_Reg | Goals scored during regulation at home.
Home_Goals_Conceded_Reg | Goals conceded during regulation at home.
Away_Goals_Reg | Goals scored during regulation away.
Away_Goals_Conceded_Reg | Goals conceded during regulation away.
Reg_Win_% | Win % during regulation.
Reg_Tie_% | Tie % during regulation.
Away_Reg_Win_% | Win % during regulation while away.
Home_Reg_Win_% | Win % during regulation while at home.
Away_Reg_Tie_% | Tie % during regulation while away.
Home_Reg_Tie_% | Tie % during regulation while at home.
Avg_Home_Goals_Reg | Average goals scored during regulation while at home.
Avg_Home_Goals_Conceded_Reg | Average goals conceded during regulation while at home.
Avg_Away_Goals_Reg | Average goals scored during regulation while away.
Avg_Away_Goals_Conceded_Reg | Average goals conceded during regulation while away.

Average Goals for Penalties and AET were scarce, which is why we left it out from our analyses.
