"""
Program 4: Develop a recommendation system using Flask that suggests content to users based on their preferences.

"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from flask import Flask, render_template, request


app = Flask(__name__)

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")


# Preprocess movie titles
def clean_title(title):
    return re.sub(r"[^a-zA-Z0-9 ]", "", title)


movies["clean_title"] = movies["title"].apply(clean_title)

# Create TF-IDF vectorizer
vector = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vector.fit_transform(movies["clean_title"])


# Function to search for similar movies
def search(title):
    """
    Search for similar movies based on the provided title.

    This function takes a movie title as input, preprocesses it, and finds similar movies based on the title's
    cosine similarity to other movies in the dataset. It returns a list of the top 5 similar movies.

    :param title: (str) The title of the movie to find similar movies for.

    :return: pandas.DataFrame-A DataFrame containing the top 5 similar movies, including their titles and genres.
    """

    # Preprocess the input title
    title = clean_title(title)

    # Transform the title into a TF-IDF vector
    query_vec = vector.transform([title])

    # Calculate cosine similarity between the input title and all movies
    similarity = cosine_similarity(query_vec, tfidf).flatten()

    # Find the indices of the top 5 most similar movies
    indices = (-similarity).argsort()[:5]  # Use argsort for top 5 indices

    # Retrieve the details of the top similar movies
    results = movies.iloc[indices]

    return results


def find_similar_movies(movie_id):
    """
    Find similar movies based on user ratings.

    This function takes a movie ID and finds movies that are similar to it based on user ratings.
    It calculates a score for each movie and returns a list of the top similar movies.

    :param movie_id: (int) The ID of the movie to find similar movies for.
    :return: pandas.DataFrame-A DataFrame containing the top similar movies, including their scores, titles, and genres.


    """
    # find users who rated the movie highly (rating > 4)
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()

    # find movies rated highly by similar users
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]

    # calculate the percentage of users who rated a movie highly
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    # Keep movies with at least 10% of similar users' ratings
    similar_user_recs = similar_user_recs[similar_user_recs > 0.10]

    # Filter movies rated highly by all users
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]

    # Calculate the percentage of users who rated each movie highly
    all_users_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())

    # Combine both percentages and calculate a score
    rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]

    # Sort movies by score and return the top 10
    rec_percentages = rec_percentages.sort_values("score", ascending=False)

    # Merge with movie data to get movie titles and genres
    similar_movies = rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[
        ["score", "title", "genres"]]

    return similar_movies


@app.route("/")
def home():
    return render_template("index.html", recommendations=None)


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Handle the recommendation request and display similar movies.

    This route handles POST requests, where users provide a movie title as input. It searches for similar movies based
    on the provided title and displays the recommendations on the webpage. The recommendations are based on the
    cosine similarity of movie titles and user ratings in the dataset.

    :return: HTML page with movie recommendations.

    Example:
    User submits a POST request with "The Dark Knight" as the input movie title, and the route returns
    an HTML page displaying recommended movies similar to "The Dark Knight."

    """

    recommendations = None
    title = request.form["movie"]

    # Check if a valid movie title is provided (at least 5 characters)
    if title and len(title) > 5:

        # Search for similar movies based on the input title
        results = search(title)

        # Check if any similar movies are found
        if not results.empty:
            movie_id = results.iloc[0]["movieId"]
            recommendations = find_similar_movies(movie_id)

    # Render the HTML page with movie recommendations
    return render_template('index.html', recommendations=recommendations)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)