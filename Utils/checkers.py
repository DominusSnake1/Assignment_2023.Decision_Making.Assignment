import pandas as pd
import sqlalchemy as sa


def checkDataIssues(tableName):
    engine = sa.create_engine('mysql+pymysql://root:password@127.0.0.1/music')
    with engine.connect() as connection:
        query = f"SELECT * FROM {tableName}"
        df = pd.read_sql(query, connection)

    missing_values = df.isnull().any(axis=1)
    if missing_values.any():
        print("Rows with Missing Values:")
        print(df[missing_values])
        df = df.dropna()

    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        print("Duplicate Values:")
        print(duplicate_rows)
        df.drop_duplicates(inplace=True)

    # df.to_sql(tableName, engine, if_exists='replace', index=False)

    engine.dispose()
