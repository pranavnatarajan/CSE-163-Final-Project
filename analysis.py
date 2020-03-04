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
df = process_data(2008, 2015)
print(df)