import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

FILE_LOCATION = './Assets/File_series.csv'


def __getEngine():
    """
        Retrieves data from the 'stats' table in the MySQL database.

        Returns:
            pd.DataFrame: DataFrame containing the retrieved data.

    """

    # create the database engine and retrieve data from the stats table
    engine = create_engine('mysql+pymysql://root:password@127.0.0.1/music')
    query = 'SELECT * FROM stats'
    df = pd.read_sql_query(query, engine)
    return df


def getScatterPlot():
    """
        Generates a scatter plot of 'artists_fans' against 'artist_id'.

    """

    df = __getEngine()

    # Create a scatter plot of 'artists_fans' against 'artist_id'
    plt.scatter(df['artists_fans'], df['artist_id'])
    plt.xlabel('Artists Fans')
    plt.ylabel('Artists IDs')
    plt.title('Scatter Plot: Artists Fans vs Artists IDs')
    plt.show()


def getARIMATrainingSplit():
    """
        Trains an ARIMA model and evaluates its performance on a test set.

    """

    # read the data from the csv file
    df = pd.read_csv(FILE_LOCATION)

    # split the data into training and testing sets
    train_data, test_data = train_test_split(df['values'], test_size=0.24, shuffle=False)

    # train the ARIMA model
    model = ARIMA(train_data, order=(1, 0, 0))  # Παράδειγμα: ARIMA(1, 0, 0)
    model_fit = model.fit()

    # make predictions on the test set
    predictions = model_fit.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)

    # evaluate the performance
    mse = mean_squared_error(test_data, predictions)
    rmse = np.sqrt(mse)
    print("Root Mean Squared Error (RMSE):", rmse)


def getTimeSeries():
    """
        Performs time series analysis on the values from a CSV file.

    """

    # Read the values from a csv file
    df = pd.read_csv(FILE_LOCATION)

    # Create a DataFrame with a column containing the values from the 'values' column in the DataFrame 'df'
    series = pd.DataFrame({'values': df['values']})

    # Generate a date range based on the length of the series
    date_rng = pd.date_range(start='1/1/2018', periods=len(series), freq='D')

    # Set the date range as the index of the series
    series.set_index(date_rng, inplace=True)

    # Plot the time series
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    series['values'].plot(ax=axes[0])
    axes[0].set_ylabel('Values')

    # Perform seasonal decomposition
    decomposition = seasonal_decompose(series['values'], model='additive',
                                       period=365)  # Assuming a period of 365 for annual seasonality

    # Retrieve the decomposed components
    trend = decomposition.trend
    seasonality = decomposition.seasonal
    residuals = decomposition.resid

    # Plot the decomposed components
    trend.plot(ax=axes[1])
    axes[1].set_ylabel('Trend')

    seasonality.plot(ax=axes[2])
    axes[2].set_ylabel('Seasonality')

    plt.tight_layout()
    plt.show()

    # Print the decomposed components
    print("Residuals:")
    print(residuals.head())

