import gdown
import pickle
import streamlit as st
import requests
import pandas as pd
import os

# ------------------ Poster Fetch ------------------ #
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f6e7905e47de8125c6d3e0ac678b1e04&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"


# ------------------ Recommendation Logic ------------------ #
def recommend(movie):
    # Safe matching (case + space)
    matched = movies[movies['title'].str.strip().str.lower() == movie.strip().lower()]

    if matched.empty:
        st.error("Movie not found in dataset")
        return [], []

    index = matched.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# ------------------ Streamlit UI ------------------ #
st.header('Movie Recommender System')



# Download similarity.pkl from Google Drive if not present
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1AY4IifUiqLn9MAwX8qXhBefZVd1QXgFO"
    gdown.download(url, "similarity.pkl", quiet=False)

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    if len(names) == 5:
        col1, col2, col3, col4, col5 = st.columns(5)

        for idx, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.text(names[idx])
                st.image(posters[idx])



