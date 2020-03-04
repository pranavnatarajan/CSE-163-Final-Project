# Champions League Data Analysis Project
## Alex Eidt and Pranav Natarajan


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
Total_Matches_AET | All matches that were decided after AET.
Home_Matches_AET | Home Matches that were decided after AET.
Total_Matches_Pens | All matches that ended in Penalty Kicks.
Home_Matches_Pens | All home matches that ended in Penalty Kicks.
Home_Wins_Reg | Home wins during regulation.
Home_Ties_Reg | Home ties during regulation. If a game goes into AET, then this counts as a tie during regulation.
Away_Wins_Reg | Away wins during regulation.
Away_Ties_Reg | Away ties during regulation. If a game goes into AET, then this counts as a tie during regulation.
Home_Goals_Reg | Goals scored during regulation at home.
Home_Goals_Conceded_Reg | Goals conceded during regulation at home.
Away_Goals_Reg | Goals scored during regulation away.
Away_Goals_Conceded_Reg | Goals conceded during regulation away.
Home_Wins_AET | Home wins during AET.
Home_Ties_AET | Home ties during AET. Leads to penalties.
Away_Wins_AET | Away wins during AET.
Away_Ties_AET | Away ties during AET. Leads to penalties.
Home_Goals_AET | Home goals scored during AET.
Home_Goals_Conceded_AET | Home goals conceded during AET.
Away_Goals_AET | Away goals scored during AET.
Away_Goals_Conceded_AET | Away goals conceded during AET.
Home_Wins_Pens | Home wins from penalty kicks.
Away_Wins_Pens | Away wins from penalty kicks.
Home_Goals_Pens | Penalties scored during penalty kicks while at home.
Home_Goals_Conceded_Pens | Penalties conceded during penalty kicks while at home.
Away_Goals_Pens | Penalties scored during penalty kicks while away.
Away_Goals_Conceded_Pens | Penalties conceded during penalty kicks while away.
Reg_Win_% | Win % during regulation.
AET_Win_% | Win % during AET.
Pens_Win_% | Win % during penalties.
Away_Reg_Win_% | Win % during regulation while away.
Home_Reg_Win_% | Win % during regulation while at home.
Away_AET_Win_% | Win % during AET while away.
Home_AET_Win_% | Win % during AET while at home.
Away_Pens_Win_% | Win % on penalties while away.
Home_Pens_Win_% | Win % on penalties while at home.
Avg_Home_Goals_Reg | Average home goals scored during regulation.
Avg_Home_Goals_Conceded_Reg | Average home goals conceded during regulation.
Avg_Away_Goals_Reg | Average away goals scored during regulation.
Avg_Away_Goals_Conceded_Reg | Average away goals conceded during regulation.
Avg_Home_Goals_AET | Average home goals scored during AET.
Avg_Home_Goals_Conceded_AET | Average home goals conceded during AET.
Avg_Away_Goals_AET | Average away goals scored during AET.
Avg_Away_Goals_Conceded_AET | Average away goals conceded during AET.
Avg_Home_Goals_Pens | Average penalties scored during penalty kicks while at home.
Avg_Home_Goals_Conceded_Pens | Average penalties conceded during penalty kicks while at home.
Avg_Away_Goals_Pens | Average penalties scored during penalty kicks while away.
Avg_Away_Goals_Conceded_Pens | Average penalties conceded during penalty kicks while away.
