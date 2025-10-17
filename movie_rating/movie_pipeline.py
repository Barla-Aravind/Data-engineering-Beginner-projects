import sqlite3
import pandas as pd
import os
import math

CSV_FILE = 'movies.csv'
DB_FILE = 'movies.db'

# check file exists and show friendly message
if not os.path.exists(CSV_FILE):
    print(f" Cannot find {CSV_FILE}'.Please create the file in the same folder and try again.")
    # exit stops the program here so nothing else runs
    raise SystemError

# Read CSV into a pandas DataFrame (table in memory)
df = pd.read_csv(CSV_FILE)

print("First 5 rows of the datset")
print(df.head(), "\n")

# Data types check - helpful to know if 'rating' is number or text
print(" Column types and non-null counts:")
print(df.info(), "\n")

# Basic cleaning: ensure 'rating' and 'num_votes' are numeric
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')  # convert rating to number, invalid -> NaN
df['num_votes'] = pd.to_numeric(df['num_votes'], errors='coerce') # convert votes to number, invalid -> NaN

# Drop rows that do not have rating (we cannot analyze movies without rating)
# Dropna removes rows where specified columns are missing
df = df.dropna(subset=['rating', 'num_votes'])

# Create a new column 'weighted_score' that mixes rating & popularity
# We compute a simple weighted score: rating * log10(num_votes + 1)
df['weighted_score'] = df['rating'] * (df['num_votes'].apply(lambda x: math.log10(x + 1)))

# Show top 5 movies by rating (straight average rating)
print("Top 5 movies by simple rating")
top_by_rating = df.sort_values(by='rating', ascending=False).head(5)
print(top_by_rating[['title','year', 'genre', 'rating']].to_string(index=False), "\n")

# Show top 5 movies by weighted score (considers popularity)
print(" Top 5 movies by weighted score (rating * log10(votes):)")
top_by_weighted = df.sort_values(by='weighted_score',ascending=False).head(5)
print(top_by_weighted[['title','year', 'genre', 'rating', 'num_votes', 'weighted_score']].to_string(index=True), "\n")

# Group by genre to get average rating and total votes per genre
# groupby creates buckets by genre, then we compute aggregate like mean and sum.
genre_stats = df.groupby('genre').agg(
    avg_rating = ('rating', 'mean'), # # average rating per genre
    total_votes = ('num_votes', 'sum'), # # total votes for that genre
    count_movies = ('movie_id', 'count') # # how many movies in that genre
) 

# Print genre statistics nicely (rounded numbers)
print("Genre Statistics (Average rating, total votes, movie count):")
genre_stats['avg_rating']=genre_stats['avg_rating'].round(2)  # prettier rounding
print(genre_stats.to_string(index=False), "\n")


# Save the cleaned DataFrame to SQLite so other programs can use it
with sqlite3.connect(DB_FILE) as conn:
     # if table 'movies' exists, replace it with our cleaned table to keep things fresh
    df.to_sql('movies', conn, if_exists='replace', index=False)
    # show how many rows were written
    written_rows = conn.execute("SELECT COUNT(*) FROM movies").fetchall()[0]
    print(f"💾 Saved {written_rows} rows to SQLite database '{DB_FILE}' in table 'movies'.\n")

# 15) Example SQL query: find top movie by weighted_score using SQL
# #     This demonstrates how SQL can also be used after we save data
with sqlite3.connect(DB_FILE) as conn:
    # write a SQL query to return top movie sorted by weighted_score
    query = """
    SELECT title, year, genre, rating, num_votes, weighted_score
    FROM movies
    ORDER BY weighted_score DESC
    LIMIT 1;
    """
    top_sql = pd.read_sql_query(query, conn) # read_sql_query returns a DataFrame
    print(" Top movie by weighted_score (via SQL):")
    print(top_sql.to_string(index=False), "\n")

#  Save simple CSV reports so you can upload them or open in Excel
#   Save the top_by_rating and genre_stats to separate CSV files
top_by_rating[['movie_id', 'title', 'year', 'genre', 'rating']].to_csv('top_by_rating.csv', index=False)
genre_stats.to_csv('genre_status.csv', index=False)
print(" Reports Saved : ' top_by_rating.csv' and 'genre_stats.csv'. ")


# Final friendly message
print("\n Movie rating Analysis completed! You can open the CSV reports or inspect  'movies.db with a SQLite viewer.")


