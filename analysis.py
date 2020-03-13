"""
Alex Eidt- CSE 163 AC
Pranav Natarajan- CSE 163 AB

CSE 163 A
Final Project

Performs the analysis on the dataset to answer
out research question of who will win the Champions
League based on past performance.
"""

import graphviz
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from process import process_data
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn import metrics


# Returns Processed Champions League DataSet from 2008-2015.
# This is where the analysis starts.
# Have set NaN's to 0

def get_data(start=2008, end=2015):
    """
    Takes 2 integers of start and end years as input,
    and returns the DataFrame of Champions League Data
    From start year to end year, both inclusive.
    """
    df = process_data(2008, 2015)
    # Creating the name column from the indices of df
    df['name'] = df.index
    return df


def create_visualizations(df):
    """
    Takes in the Champions League dataframe subset from 2008-2015
    as input, and produces 4 separate figures showing
    the home and away win percentage of teams in regulation time with
    a size parameter for number of goals scored and number of goals conceded
    """
    df1 = df.sort_values(by=['Reg_Win_%'], ascending=False).head(10)
    plt.clf()
    sns.relplot(x='Away_Reg_Win_%', y='Reg_Win_%', hue='name',size='Home_Goals_Reg',data=df1, s=55)
    plt.title('Home Win Percentage vs Away Win Percentage of Top 10 Teams by Home Goals Scored')
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Scored', bbox_inches='tight')
    plt.clf()
    sns.relplot(x='Away_Reg_Win_%', y='Reg_Win_%', hue='name',size='Home_Goals_Conceded_Reg',data=df1)
    plt.title('Home Win Percentage vs Away Win Percentage of Top 10 Teams by Home Goals Conceded')
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Conceded', bbox_inches='tight')
    plt.clf()
    sns.relplot(x='Away_Reg_Win_%', y='Away_Reg_Win_%',hue='name', size='Away_Goals_Reg', data = df1)
    plt.xticks(rotation=-60)
    plt.savefig('Away_Win_Percentage_data_Scored.png', bbox_inches='tight')
    plt.clf()
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
    df['coefficient'] = (0.15 * df['Reg_Win_%'] + 0.25 * df['Away_Reg_Win_%']\
    + 0.08 * df['Avg_Home_Goals_Reg']\
    + 0.22 * df['Avg_Away_Goals_Reg']\
    - 0.22 * df['Avg_Home_Goals_Conceded_Reg']\
    - 0.08 * df['Avg_Away_Goals_Conceded_Reg'])
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
    ml_df = ml_df.fillna(0)
    ml_df = sort_df(ml_df)
    return ml_df

def sort_df(ml_df, column='Reg_Win_%'):
    """
    Sorts the DataFrame by any of the columns
    And returns the sorted DataFrame
    """
    ml_df = ml_df.sort_values(by=column, ascending=True)
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    #print(pd.DataFrame(X_test, y_test))
    winner_coefficient_model = DecisionTreeClassifier()
    winner_coefficient_model.fit(X_train, y_train)
    plot_tree(winner_coefficient_model, X, y)
    y_train_pred = winner_coefficient_model.predict(X_train)
    print('Training Accuracy: ', metrics.accuracy_score(y_train, y_train_pred))
    y_test_pred = winner_coefficient_model.predict(X_test)
    print('Team(coefficient): ', y_test_pred)
    print('Prediction Accuracy: ', metrics.accuracy_score(y_test, y_test_pred))
    return y_test_pred


def predict_coefficient(ml_df):
    """
    Takes in the DataFrame of curated Data as input,
    and performs Machine Learning Using a Regressor Model to get
    a prediction of the coefficient.
    It prints out the Mean Square Error value of the predictions
    """
    X = ml_df[['Reg_Win_%', 'Away_Reg_Win_%', 'Avg_Home_Goals_Reg',
      'Avg_Home_Goals_Conceded_Reg', 'Avg_Away_Goals_Reg', 'Avg_Away_Goals_Conceded_Reg']]
    X = pd.get_dummies(X)
    y = ml_df['coefficient']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    coefficient_prediction = DecisionTreeRegressor()
    coefficient_prediction.fit(X_train, y_train)
    y_test_pred = coefficient_prediction.predict(X_test)
    print('Mean Square error Of Predictions: ', metrics.mean_squared_error(y_test, y_test_pred))
    return (y_test, y_test_pred)

def visualize_prediction(test_data):
    """
    Visualizes the relation between predicted coefficients
    and actual coefficient values as a scatterplot.
    """
    y_test, y_test_pred = test_data
    df1 = pd.DataFrame(list(zip(y_test, y_test_pred)),columns=['y_test', 'y_test_pred'])
    plt.clf()
    sns.scatterplot(x='y_test', y='y_test_pred', legend=False, data = df1)
    plt.xlabel('Actual Coefficient Values')
    plt.ylabel('Predicted Coefficient Values')
    plt.title('Predicted Vs Actual Coefficient Values')
    plt.savefig('Regression_Visualization.png', bbox_inches='tight')


# def predict_winner_no_coefficient(ml_df):
#     """
#     Takes in the dataframe created for machine learning as input,
#     and predicts winner using every other column but the coefficient,
#     by a DecisionTreeClassifier Model
#     """
#     X = ml_df[['Reg_Win_%', 'Away_Reg_Win_%', 'Avg_Home_Goals_Reg',
#      'Avg_Home_Goals_Conceded_Reg', 'Avg_Away_Goals_Reg', 'Avg_Away_Goals_Conceded_Reg']]
#     X = pd.get_dummies(X)
#     y = ml_df['name']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
#     #print(pd.DataFrame(X_test,y_test))
#     winner_no_coefficient_model = DecisionTreeClassifier()
#     winner_no_coefficient_model.fit(X_train, y_train)
#     #plot_tree(winner_no_coefficient_model, X, y)
#     y_train_pred = winner_no_coefficient_model.predict(X_train)
#     print('Training Accuracy: ', metrics.accuracy_score(y_train, y_train_pred))
#     y_test_pred = winner_no_coefficient_model.predict(X_test)
#     print('Team(No Coefficient): ', y_test_pred)
#     print('Prediction Accuracy: ', metrics.accuracy_score(y_test, y_test_pred))
#     return y_test_pred

# def evaluation_of_models(y_test_pred_co, y_test_pred_no_co):
#     """
#     Returns the Accuracy Scores of the Machine Prediction Models
#     of the coefficient and the model without the coefficient,
#     as well as the report and the confusion matrix.
#     """
#     # Accuracy Score of the two  predicted modules with respect to ech other
#     print('Accuracy of Coefficient MODEL To Non coefficeint Model: ', metrics.accuracy_score(y_test_pred_no_co, y_test_pred_co))
#     # Confusion Matrix
#     #print('Confusion Matrix: ', metrics.confusion_matrix(y_test_pred_no_co, y_test_pred_co))
#     # Report
#     print('classification_report: ', metrics.classification_report(y_test_pred_co, y_test_pred_no_co))


# def plot_tree(model, X, y):
#   """
#   This function takes a model and the X and y values for a dataset
#   and plots a visualization of the decision tree

#   This function won't work with your cse163 environment.
#   ADAPTED FROM LECTURE 9 COLAB OF MACHINE LEARNING
#   BY HUNTER SCHAFER AND CSE 163 WI 20 STAFF
#   """
#   dot_data = export_graphviz(model, out_file='Visualization.pdf', 
#                       feature_names=X.columns,  
#                       class_names=y.unique(),  
#                       filled=True, rounded=True,  
#                       special_characters=True)
#   return graphviz.Source(dot_data)

def main():
    """
    The main function contains all functions in analysis.py
    allowing easy running of the program.
    """
    # Using the processs_data function to get the data subset from 2008-2015
    df = get_data(2008, 2015)
    # Creating visualizations
    create_visualizations(df)
    # Adding a coefficient column to the dataframe
    df = calculate_coefficient(df)
    # Creating the Dataframe for machine learning
    ml_df = create_ML_dataframe(df)
    # Predicting coefficient values using relevant data.
    test_data = predict_coefficient(ml_df)
    # Visualizing Predictions
    visualize_prediction(test_data)
    

if __name__ == '__main__':
    main()
