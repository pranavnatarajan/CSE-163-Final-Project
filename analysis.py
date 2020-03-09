"""
Alex Eidt- CSE 163 AC
Pranav Natarajan- CSE 163 AB

CSE 163 A
Final Project

Performs the analysis on the dataset to answer
out research question of who will win the Champions
League based on past performance.
"""

import pandas as pd
import matplotlib as plt
import seaborn as sns
from process import process_data
from sklearn.tree import DecisionTreeClassifier

# Returns Processed Champions League DataSet from 2008-2015.
# This is where the analysis starts.

def create_model(df):
    """
    Takes in the Champions League dataframe subset from 2008-2015
    as input, and creates a model for the coefficient of each team in
    the dataset.
    """

def create_ML_dataframe(df):
    """
    takes in the processed Champions League CSV data as input
    and creates the dataframe consisting of the relevant columns 
    used by the coefficient, and thereby the Classifier Model
    """

def predict_winner_coefficient(ml_df):
    """
    Takes in the dataframe created for machine learning as input,
    and predicts winner using the coefficient as the only column
    by a DecisionTreeClassifier Model
    """


def predict_winner_no_coefficient(ml_df):
    """
    Takes in the dataframe created for machine learning as input,
    and predicts winner using every other column but the coefficient,
    by a DecisionTreeClassifier Model
    """


def main():
    """
    The main function contains the one place to call all the functions from 
    """
    # Using the processs_data function to get the data subset from 2008-2015
    df = process_data(2008, 2015)
