"""
Alex Eidt
Pranav Natarajan

CSE 163 AC
Final Project

Performs the analysis on the dataset to answer
out research question of who will win the Champions
League based on past performance.
"""

import pandas as pd
from process import process_data

# Returns Processed Champions League DataSet from 2008-2015.
# This is where the analysis starts.

"""
I think a good idea is to do something like a "Goals per minute"
for every team so that if our ML model predicts that a Knock-out round
game will be tied at the end of regulation, we can use the goals per minute
metric to predict the number of goals in extra time.
"""
df = process_data(2008, 2015)
print(df.loc['Chelsea'])