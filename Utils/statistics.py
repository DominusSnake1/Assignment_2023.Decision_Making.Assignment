import pandas as pd
from sqlalchemy import create_engine


def generateStatistics():
    engine = create_engine('mysql+pymysql://root:password@127.0.0.1/music')
    query = f'SELECT * FROM stats'
    df = pd.read_sql_query(query, engine)

    average_fans_per_artist = df['artists_fans'].mean()
    print("Average Number of Fans per Artist:\n", average_fans_per_artist)

    genre_popularity = df.groupby('genre_id')['artists_fans'].sum()
    print("Genre Popularity:\n", genre_popularity)

    artist_popularity_by_genre = df.groupby(['genre_id', 'artist_id'])['artists_fans'].sum()
    print("Artist Popularity by Genre:\n", artist_popularity_by_genre)

    unique_genres = df['genre_id'].nunique()
    print("Number of Unique Genres:\n", unique_genres)

    correlation = df['genre_id'].corr(df['artists_fans'])
    print("Correlation between Genre and Artists' Fans:\n", correlation)

    dominant_genres = df['genre_id'].value_counts()
    print("Dominant Genres by Artists:\n", dominant_genres)
