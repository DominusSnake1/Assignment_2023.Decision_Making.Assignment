import numpy as np
import pandas as pd
import sqlalchemy as sa


def checkDataIssues(table):
    engine = sa.create_engine('mysql+pymysql://root:password@127.0.0.1/music')
    with engine.connect() as connection:
        query = 'SELECT * FROM {}'.format(table)
        df = pd.read_sql_query(query, connection)

    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Missing values found:")
        print(missing_values)

        df.fillna(df.mean(), inplace=True)

    numeric_columns = df.select_dtypes(include=np.number).columns

    duplicate_rows = df.duplicated(subset=numeric_columns)
    if duplicate_rows.any():
        print("Duplicate rows found:")
        print(df[duplicate_rows])

        df.drop_duplicates(subset=numeric_columns, inplace=True)

    z_scores = np.abs((df[numeric_columns] - df[numeric_columns].mean()) / df[numeric_columns].std())
    outlier_rows = (z_scores > 3).any(axis=1)
    if outlier_rows.any():
        print("Outlier rows found:")
        print(df[outlier_rows])

        df = df[~outlier_rows]

    return df


