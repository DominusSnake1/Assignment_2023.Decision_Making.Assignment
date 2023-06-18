import pandas as pd
import mysql.connector as sqlcon


def generateStatistics(table):
    connection = sqlcon.connect(
        user='root',
        password='password',
        host='127.0.0.1',
        database='music'
    )

    query = 'SELECT * FROM {}'.format(table)
    df = pd.read_sql_query(query, connection)

    # Calculate the mean
    mean = df.mean()

    # # Calculate the median
    # median = df.median()
    #
    # # Calculate the mode
    # mode = df.mode().iloc[0]
    #
    # # Calculate the standard deviation
    # std_dev = df.std()
    #
    # # Calculate the variance
    # variance = df.var()
    #
    # # Calculate the range
    # data_range = df.max() - df.min()
    #
    # # Calculate quartiles
    # quartiles = df.quantile([0.25, 0.5, 0.75])
    #
    # # Calculate the count
    # count = df.count()
    #
    # # Calculate skewness
    # skewness = df.skew()
    #
    # # Calculate kurtosis
    # kurtosis = df.kurtosis()

    # Print the calculated statistics
    print("Mean:")
    print(mean)
    # print("\nMedian:")
    # print(median)
    # print("\nMode:")
    # print(mode)
    # print("\nStandard Deviation:")
    # print(std_dev)
    # print("\nVariance:")
    # print(variance)
    # print("\nRange:")
    # print(data_range)
    # print("\nQuartiles:")
    # print(quartiles)
    # print("\nCount:")
    # print(count)
    # print("\nSkewness:")
    # print(skewness)
    # print("\nKurtosis:")
    # print(kurtosis)
