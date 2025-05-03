import streamlit as st
import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id, retries=3, delay=1):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1ad74c1ea6815dbb42a4a8223831b8e6&language=en-US"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt + 1}] Failed to fetch poster for movie ID {movie_id}: {e}")
            time.sleep(delay)

    # Fallback image if all retries fail
    print(f"All {retries} attempts failed. Using fallback image for movie ID {movie_id}.")
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in rec_movies_list:
        movie_id_py = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch poster using API
        recommend_movies_posters.append(fetch_poster(movie_id_py))
    return recommend_movies, recommend_movies_posters

movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl","rb"))

movies_list = movies["title"].values
st.title("Movie Recommender System")
selected_movie_name = st.selectbox("select from the tuple", movies_list)

if st.button("Recommend"):

    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(poster[0])
        st.text(names[0])
    with col2:
        st.image(poster[1])
        st.text(names[1])
    with col3:
        st.image(poster[2])
        st.text(names[2])
    with col4:
        st.image(poster[3])
        st.text(names[3])
    with col5:
        st.image(poster[4])
        st.text(names[4])