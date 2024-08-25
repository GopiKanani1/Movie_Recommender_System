

import streamlit as st
import pickle
import pandas as pd
import  requests



page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/premium-photo/film-reel-frame-background-with-copy-space-frame-mockup_1199903-25768.jpg?size=626&ext=jpg&ga=GA1.1.1323782050.1704422980&semt=ais_hybrid");
background-size: cover;

background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
color: white;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

/* Custom styling for the selectbox label */
[data-testid="stSelectbox"] label {{
    color: white;  /* Set the label color to white */
    font-weight: bold; /* Make the label text bold */
    font-size: 1.2em; /* Increase font size for better readability */
}}
[data-testid="stButton"] button {{
    background-color: #c8d9df;
    color: #333333;
    font-weight: 20;
    border: none;
    padding: 0.5em 1em;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
}}

[data-testid="stButton"] button:hover {{
    background-color: #74888c;
    color: white;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


def fetch_poster(movie_id):
    reaponse=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=reaponse.json()

    return "https://image.tmdb.org/t/p/w500"+data["poster_path"]

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]

    for i in movies_list:
        movies_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movies_id))
    return recommended_movies,recommended_movies_posters

# Load movies and similarity data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_titles = movies['title'].values

st.markdown(
    """
    <h1 style='color: #FFFFFF;'>🎬 Movie Recommender System</h1>
    """,
    unsafe_allow_html=True
)


selected_movie_name = st.selectbox('How would you like to choose?', movie_titles)

if st.button('Recommend',type="primary"):
    names ,posters= recommend(selected_movie_name)


    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

