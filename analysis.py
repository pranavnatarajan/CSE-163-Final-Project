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
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from process import process_data
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics


# Returns Processed Champions League DataSet from 2008-2015.
# This is where the analysis starts.
# Have set NaN's to 0
def create_visualizations(df):
    """
    Takes in the Champions League dataframe subset from 2008-2015
    as input, and produces 4 separate figures showing
    the home and away win percentage of teams in regulation time with
    a size parameter for number of goals scored and number of goals conceded
    """
    df1 = df.sort_values(by=['Reg_Win_%'], ascending=False).head(10)
    sns.relplot(x='Away_Reg_Win_%', y='Reg_Win_%', hue='name',size='Home_Goals_Reg',data=df1)
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Scored', bbox_inches='tight')
    sns.relplot(x='Away_Reg_Win_%', y='Reg_Win_%', hue='name',size='Home_Goals_Conceded_Reg',data=df1)
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Conceded', bbox_inches='tight')
    sns.relplot(x='Away_Reg_Win_%', y='Away_Reg_Win_%',hue='name', size='Away_Goals_Reg', data = df1)
    plt.xticks(rotation=-60)
    plt.savefig('Away_Win_Percentage_data_Scored.png', bbox_inches='tight')
    sns.relplot(x='Away_Reg_Win_%', y='Away_Reg_Win_%',hue='name', size='Away_Goals_Conceded_Reg', data = df1)
    plt.xticks(rotation=-60)
    plt.savefig('Away_Win_Percentage_data_Conceded.png', bbox_inches='tight')

def calculate_coefficient(df):
    """
    Takes in the Champions League dataframe subset from 2008-2015
    as input, and calculates the coefficient of each team in
    the dataset as a new column in the dataset,
    and returns the dataset.

    The model is weighted as follows:
    1. Win Percentage(Overall) = 40%,
    under which we have 
        Reg_Win_% = 15%
        Away_Reg_Win_% = 25%

    2. Average Goals Scored(Home) = 8%
    
    3. Average Goals Scored(Away) = 22%

    4. Average Goals Conceded(Home) = 22%

    5. Average Goals Conceded(Away) = 8% 
    """
    df['coefficient'] = 0.15 * df['Reg_Win_%'] + 0.25 * df['Away_Reg_Win_%']\
    + 0.08 * df['Avg_Home_Goals_Reg']\
    + 0.22 * df['Avg_Away_Goals_Reg']\
    - 0.22 * df['Avg_Home_Goals_Conceded_Reg']\
    - 0.08 * df['Avg_Away_Goals_Conceded_Reg']
    #print('The Range of Values of the coefficient range from: ',
    #(df['coefficient'].min, df['coefficient'].max))
    print(df['coefficient'])
    return df


def create_ML_dataframe(df):
    """
    takes in the processed Champions League CSV data as input
    and creates the dataframe consisting of the relevant columns
    used by the coefficient, and thereby the Classifier Model
    """
    ml_df = df[['name', 'Reg_Win_%', 'Away_Reg_Win_%', 'Avg_Home_Goals_Reg',
     'Avg_Home_Goals_Conceded_Reg', 'Avg_Away_Goals_Reg', 'Avg_Away_Goals_Conceded_Reg',
     'coefficient']]
    ml_df.fillna(0)
    ml_df = ml_df.sort_values(by=['coefficient'])
    return ml_df


def predict_winner_coefficient(ml_df):
    """
    Takes in the dataframe created for machine learning as input,
    and predicts winner using the coefficient as the only column
    by a DecisionTreeClassifier Model
    """
    X = ml_df['coefficient']
    X = pd.get_dummies(X)
    y = ml_df['name']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    print(y_test)
    winner_coefficient_model = DecisionTreeClassifier()
    winner_coefficient_model.fit(X_train, y_train)
    y_train_pred = winner_coefficient_model.predict(X_train)
    print('Training Accuracy: ', metrics.accuracy_score(y_train, y_train_pred))
    y_test_pred = winner_coefficient_model.predict(X_test)
    print('Winner Of the Champions League(coefficient): ', y_test_pred)
    print('Prediction Accuracy: ', metrics.accuracy_score(y_test, y_test_pred))


def predict_winner_no_coefficient(ml_df):
    """
    Takes in the dataframe created for machine learning as input,
    and predicts winner using every other column but the coefficient,
    by a DecisionTreeClassifier Model
    """
    X = ml_df[['Reg_Win_%', 'Away_Reg_Win_%', 'Avg_Home_Goals_Reg',
     'Avg_Home_Goals_Conceded_Reg', 'Avg_Away_Goals_Reg', 'Avg_Away_Goals_Conceded_Reg']]
    X = pd.get_dummies(X)
    y = ml_df['name']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    print(y_test)
    winner_no_coefficient_model = DecisionTreeClassifier(max_depth=200)
    winner_no_coefficient_model.fit(X_train, y_train)
    y_train_pred = winner_no_coefficient_model.predict(X_train)
    print('Training Accuracy: ', metrics.accuracy_score(y_train, y_train_pred))
    y_test_pred = winner_no_coefficient_model.predict(X_test)
    print('Winner Of the Champions League: ', y_test_pred)
    print('Prediction Accuracy: ', metrics.accuracy_score(y_test, y_test_pred))


def main():
    """
    The main function contains all functions in analysis.py
    allowing easy running of the program.
    """
    # Using the processs_data function to get the data subset from 2008-2015
    df = process_data(2008, 2015)
    # Creating the name column from the indices of df
    df['name'] = df.index
    print(df['name'].head)
    # Creating visualizations
    create_visualizations(df)
    # Adding a coefficient column to the dataframe
    df = calculate_coefficient(df)
    # Creating the Dataframe for machine learning
    ml_df = create_ML_dataframe(df)
    # Predicting winner of the champions league
    # using Machine Learning on coefficient
    predict_winner_coefficient(ml_df)
    # Predicting winner of the champions league
    # using Machine Learning on every other column but coefficient
    predict_winner_no_coefficient(ml_df)
  

if __name__ == 'main':
    main()
