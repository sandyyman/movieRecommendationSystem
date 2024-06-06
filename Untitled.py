import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch movie poster from TMDb API
def fetch_poster_url(movie_title):
    api_key = "d16ff4c78e529281021033e3af5c66e7"
    base_url = "https://api.themoviedb.org/3/search/movie"
    response = requests.get(base_url, params={"api_key": api_key, "query": movie_title})
    data = response.json()
    if data["results"]:
        poster_path = data["results"][0]["poster_path"]
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_poster_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster_url(
            movies.iloc[i[0]].title
        )  # Fetch poster URL from TMDb
        recommended_posters.append(poster_url)
    return recommended_movies, recommended_posters


# Load the movie dictionary and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit application title
st.title("MOVIE RECOMMENDER SYSTEM")

# Dropdown menu for movie selection
option = st.selectbox("Select your Movie:", movies["title"].values)

# Recommend movies when the button is clicked
if st.button("Recommend"):
    recommendations, posters = recommend(option)
    cols = st.columns(5)  # Create 5 columns
    for col, title, poster in zip(cols, recommendations, posters):
        with col:
            st.image(poster, width=150)  # Display movie poster
            st.write(title)  # Display movie title
