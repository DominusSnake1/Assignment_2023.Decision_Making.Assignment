import pandas as pd
import sqlalchemy as sa


def checkDataIssues(tableName):
    """
        Checks for data issues in a specified table.

        Parameters:
            tableName (str): Name of the table to check for data issues.
    """
    # Create a connection to the MySQL database
    engine = sa.create_engine('mysql+pymysql://root:password@127.0.0.1/music')

    # Retrieve the data from the specified table into a DataFrame
    with engine.connect() as connection:
        query = f"SELECT * FROM {tableName}"
        df = pd.read_sql(query, connection)

    # Check for missing values in the DataFrame
    missing_values = df.isnull().any(axis=1)
    if missing_values.any():
        print("Rows with Missing Values:")
        print(df[missing_values])
        df = df.dropna()

    # Check for duplicate rows in the DataFrame
    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        print("Duplicate Values:")
        print(duplicate_rows)
        df.drop_duplicates(inplace=True)

    # df.to_sql(tableName, engine, if_exists='replace', index=False)

    # close the connection to the database
    engine.dispose()
