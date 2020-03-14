"""
Alex Eidt - CSE 163 AC
Pranav Natarajan - CSE 163 AB

CSE 163 A
Final Project

Performs the analysis on the dataset to answer
out research question of who will win the Champions
League based on past performance.
"""
from process import process_data
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# Returns Processed Champions League DataSet from 2008-2015.
# This is where the analysis starts.

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
    # Getting data of top 10 teams by coefficient
    df1 = df.sort_values(by=['coefficient'], ascending=False).head(10)
    plt.clf()
    # Home Win Percentage vs Away Win Percentage
    # of Top 10 Teams by Home Goals Scored
    sns.relplot(x='Away_Reg_Win_%',
                y='Reg_Win_%',
                hue='name',
                size='Home_Goals_Reg',
                data=df1)
    plt.xlabel('Regulation Time Win Percentage(Away)')
    plt.ylabel('Regulation Time Win Percentage(Home)')
    plt.title('Home Win Percentage vs Away Win Percentage\
        of Top 10 Teams by Home Goals Scored')
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Scored', bbox_inches='tight')
    plt.clf()
    # Home Win Percentage vs Away Win Percentage
    # of Top 10 Teams by Home Goals Conceded
    sns.relplot(x='Away_Reg_Win_%',
                y='Reg_Win_%',
                hue='name',
                size='Home_Goals_Conceded_Reg',
                data=df1)
    plt.xlabel('Regulation Time Win Percentage(Away)')
    plt.ylabel('Regulation Time Win Percentage(Home)')
    plt.title('Home Win Percentage vs Away Win Percentage\
    of Top 10 Teams by Home Goals Conceded')
    plt.xticks(rotation=-60)
    plt.savefig('HomeWin%_by_Home_Goals_Conceded', bbox_inches='tight')
    plt.clf()
    # Home Win Percentage vs Away Win Percentage
    # of Top 10 Teams by Away Goals Scored
    sns.relplot(x='Away_Reg_Win_%',
                y='Reg_Win_%',
                hue='name',
                size='Away_Goals_Reg',
                data=df1)
    plt.xlabel('Regulation Time Win Percentage(Away)')
    plt.ylabel('Regulation Time Win Percentage(Home)')
    plt.title('Home Win Percentage vs Away Win Percentage\
    of Top 10 Teams by Away Goals Scored')
    plt.xticks(rotation=-60)
    plt.savefig('Away_Win_Percentage_data_Scored.png', bbox_inches='tight')
    plt.clf()
    # Home Win Percentage vs Away Win Percentage 
    # of Top 10 Teams by Away Goals Conceded'
    sns.relplot(x='Away_Reg_Win_%',
                y='Reg_Win_%',
                hue='name',
                size='Away_Goals_Conceded_Reg',
                data=df1)
    plt.xlabel('Regulation Time Win Percentage(Away)')
    plt.ylabel('Regulation Time Win Percentage(Home)')
    plt.title('Home Win Percentage vs Away Win Percentage\
    of Top 10 Teams by Away Goals Conceded')
    plt.xticks(rotation=-60)
    # Saving Figure in working directory
    plt.savefig('Away_Win_Percentage_data_Conceded.png', bbox_inches='tight')


def calculate_coefficient(df):
    """
    Takes in the Champions League dataframe subset from 2008-2015
    as input, and calculates the coefficient of each team in
    the dataset as a new column in the dataset,
    and returns the DataFrame.

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
    df['coefficient'] = (0.15 * df['Reg_Win_%'] + 0.25 * df['Away_Reg_Win_%']
        + 0.08 * df['Avg_Home_Goals_Reg']
        + 0.22 * df['Avg_Away_Goals_Reg']
        - 0.22 * df['Avg_Home_Goals_Conceded_Reg']
        - 0.08 * df['Avg_Away_Goals_Conceded_Reg'])
    return df


def create_ML_dataframe(df):
    """
    takes in the processed Champions League CSV data as input
    and creates the dataframe consisting of the relevant columns
    used by the coefficient, and thereby the Classifier Model
    """
    # Getting relevant columns from 
    # the initial processed data frame
    ml_df = df[['name', 
                'Reg_Win_%',
                'Away_Reg_Win_%',
                'Avg_Home_Goals_Reg',
                'Avg_Home_Goals_Conceded_Reg',
                'Avg_Away_Goals_Reg',
                'Avg_Away_Goals_Conceded_Reg',
                'coefficient']]
    # Setting any NaN values to 0
    ml_df = ml_df.fillna(0)
    return ml_df


def predict_coefficient(ml_df):
    """
    Takes in the DataFrame of curated Data as input,
    and performs Machine Learning Using a Regressor Model to get
    a prediction of the coefficient.
    Returns the List of Names of teams whose coefficients were in the test set,
    and the set of actual test coefficients and the predicted coefficients
    as a tuple
    """
    # Splitting the DataFrame into Features and Label to predict,
    # Getting the features
    X = ml_df[['Reg_Win_%', 'Away_Reg_Win_%', 'Avg_Home_Goals_Reg',
               'Avg_Home_Goals_Conceded_Reg', 'Avg_Away_Goals_Reg',
               'Avg_Away_Goals_Conceded_Reg']]

    X = pd.get_dummies(X)
    y = ml_df['coefficient']

    # Splitting the Set into an 80/20 Testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    coefficient_prediction = DecisionTreeRegressor()
    coefficient_prediction.fit(X_train, y_train)

    # getting predictions on the testing data
    y_test_pred = coefficient_prediction.predict(X_test)
    # mean squared error of predictions
    mse = metrics.mean_squared_error(y_test, y_test_pred)
    print('Mean Square error Of Predictions: ', mse)
    return (y_test, y_test_pred, mse)


def visualize_prediction(test_data):
    """
    Takes in the tuple containing the test set of coefficients
    and the set of predicted coefficients, and
    visualizes their relation as a scatterplot.
    """
    # Unpacking test data and predicted data from tuple
    y_test = test_data[1]
    y_test_pred = test_data[2]
    # Creating the data frame for easy plotting
    df1 = pd.DataFrame(list(zip(y_test, y_test_pred)), columns=['y_test',
                                                                'y_test_pred'])
    # Plotting scatterplot
    plt.clf()
    sns.scatterplot(x='y_test', y='y_test_pred', legend=False, data=df1)
    plt.xlabel('Actual Coefficient Values')
    plt.ylabel('Predicted Coefficient Values')
    plt.title('Predicted Vs Actual Coefficient Values')
    plt.savefig('Regression_Visualization.png', bbox_inches='tight')


def main():
    """
    The main function contains all functions in analysis.py
    allowing easy running of the program.
    """
    # Using the processs_data function to get the data subset from 2008-2015
    df = get_data(2008, 2015)
    # Adding a coefficient column to the dataframe
    df = calculate_coefficient(df)
    # Creating visualizations
    create_visualizations(df)
    # Creating the Dataframe for machine learning
    ml_df = create_ML_dataframe(df)
    # Predicting coefficient values using relevant data.
    test_data = predict_coefficient(ml_df)
    # Visualizing Predictions
    visualize_prediction(test_data)


# main method format
if __name__ == 'main':
    main()
