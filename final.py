# Description: This file contains the code for the Streamlit web app that recommends movies based on user input.
# this code is used to create a web app that recommends movies based on user input. The app uses a dataset of movies and their similarity scores to recommend similar movies to the user. The app allows the user to select a movie from a dropdown menu and then click a button to get recommendations. The app displays the recommended movies along with their posters. The app also includes a footer with information about the app and the developer.
import streamlit as st #importing streamlit library
import pandas as pd #importing pandas library
import pickle #importing pickle library
import requests 

# Load Custom CSS
with open("style.css") as f: #
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Constants
API_KEY = "8265bd1679663a7ea12ac168da84d2e8" #API key for TMDB

# Helper functions
def fetch_poster(movie_id): #function to fetch movie poster
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url) #fetching data from the url
    data = response.json()    #converting the response to json format
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if 'poster_path' in data else "" #returning the poster path

def recommend(movie):  #function to recommend movies
    index = movies[movies['title'] == movie].index[0]   #getting the index of the selected movie
    distances = similarity[index]    #getting the similarity scores of the selected movie
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  #sorting the movies based on similarity scores
    
    recommended_movies = []  #list to store recommended movies
    recommended_posters = [] #list to store recommended movie posters
    for i in movie_list:   #iterating through the recommended movies
        movie_id = movies.iloc[i[0]].movie_id  #getting the movie id
        recommended_movies.append(movies.iloc[i[0]].title)      #appending the movie title to the list
        recommended_posters.append(fetch_poster(movie_id))      #appending the movie poster to the list             

    return recommended_movies, recommended_posters  #returning the recommended movies and posters

# Load data and similarity model
movies = pd.read_pickle(open('movie_list.pkl', 'rb'))   #loading the movie list
similarity = pd.read_pickle(open("similarity.pkl", 'rb'))   #loading the similarity scores  

# Streamlit App
st.title("🎬 Movie Recommendation System")                  #setting the title of the web app
st.write("## Get recommendations based on your favorite movies")     #writing a message on the web app

selected_movie = st.selectbox("Choose a movie", movies['title'].values)  #creating a dropdown menu to select a movie

if st.button("Recommend"):   #creating a button to get recommendations
    names, posters = recommend(selected_movie)   #getting the recommended movies and posters
    
    st.write(f"### If you liked **{selected_movie}**, you might also enjoy:") #displaying a message on the web app
    
    cols = st.columns(5)  #creating 5 columns to display the recommended movies
    for col, name, poster in zip(cols, names, posters):  #iterating through the recommended movies
        with col:
            # Updated parameter
            st.image(poster, caption=name)  #displaying the movie poster with the movie title

# Add a footer
st.markdown("""
    <hr style="border:2px solid gray"> </hr>
    <footer style="text-align: center; color: gray;">
    <p>&copy; 2025 Movie Recommender. All rights reserved.</p>
    <p>&copy; Made with ❤️ by [Tushant yadav ]</p>
    
    </footer>
    """, unsafe_allow_html=True)

