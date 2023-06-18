import pandas as pd
from sqlalchemy import create_engine
import DBCreation.connection as dbcon
import Utils.checkers as chk


def insertStatistics(artist_id):
    cursor = dbcon.__getDBCursor()

    getArtistsFans = 'SELECT COUNT(user_id) FROM userlikes WHERE artist_id = %(artist_id)s'

    cursor.execute(getArtistsFans, {'artist_id': artist_id})
    artists_fans = cursor.fetchone()

    getGenreID = """
        SELECT genres.genre_id
            FROM genres
            JOIN artists ON genres.genre = artists.genre
            WHERE artists.artist_id = {}
    """.format(artist_id)

    cursor.execute(getGenreID, {'artist_id': artist_id})
    genreid = cursor.fetchone()[0]

    getGenreFans = """
            SELECT COUNT(userlikes.user_id) AS genre_fans
                FROM genres
                JOIN artists ON genres.genre = artists.genre
                JOIN userlikes ON artists.artist_id = userlikes.artist_id
                WHERE genres.genre_id = {}
                GROUP BY genres.genre
    """.format(genreid)

    cursor.execute(getGenreFans, {'genre_id': genreid})
    genreFans = cursor.fetchone()

    insertStats = 'INSERT INTO stats (artist_id, artists_fans, genre_id, genres_fans) VALUES (%(artist_id)s, %(artists_fans)s, %(genre_id)s, %(genres_fans)s) ON DUPLICATE KEY UPDATE artists_fans = artists_fans + 1, genres_fans = genres_fans + 1'

    statsData = {
        'artist_id': artist_id,
        'artists_fans': artists_fans[0],
        'genre_id': genreid,
        'genres_fans': genreFans[0]
    }

    try:
        cursor.execute(insertStats, statsData)
    except dbcon.__getSQLConError() as err:
        if err.errno == dbcon.__getSQLConErrorcode().ER_DUP_ENTRY:
            print("[Genre] with an ID \"{}\" already exists.".format(statsData['genre_id']))
    else:
        print("[Artist] with an ID \"{}\" has {} fans.".format(statsData['artist_id'], statsData['artists_fans']))
        print("[Genre] with an ID \"{}\" has {} fans.".format(statsData['genre_id'], statsData['genres_fans']))

    chk.checkDataIssues('stats')
    dbcon.__commitDB()
    cursor.close()


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
