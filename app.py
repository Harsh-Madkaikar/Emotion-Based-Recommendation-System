import streamlit as st
import requests
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---------------------------
# API KEYS (REPLACE THESE)
# ---------------------------

API_KEY_FACE = 'Y50yFX-T_tOMTRmo_VvSqbAZGG324n3b' 
API_SECRET_FACE = '6nT63UxBINvwLPRqpQEjpZ8j_UcWJ0xh'

API_KEY_SPOONACULAR = '03eaef7233bf4c88a2aee399a15a59b0'
OMDB_API_KEY = '86a9fe15' 

SPOTIFY_CLIENT_ID = 'f07d6ff0d29449dba36598db280138d4' 
SPOTIFY_CLIENT_SECRET = 'c5e2dff72b3a45b081f97e812b86276d' 

FACE_URL = "https://api-us.faceplusplus.com/facepp/v3/detect"
SPOONACULAR_URL = "https://api.spoonacular.com/recipes/complexSearch"
OMDB_URL = "http://www.omdbapi.com/"

# ---------------------------
# PAGE TITLE
# ---------------------------

st.title("😊 Emotion-Based Recommendation System")

st.write(
"Upload an image and get **Meal 🍜, Movie 🎬, and Music 🎵 recommendations** "
"based on your detected emotion."
)

# ---------------------------
# IMAGE UPLOAD
# ---------------------------

uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

# Show message when no image is uploaded
if uploaded_file is None:
    st.info("Please upload a face image to start emotion detection.")

# ---------------------------
# EMOTION DETECTION
# ---------------------------

def detect_emotion(image_file):

    files = {"image_file": image_file}

    params = {
        "api_key": API_KEY_FACE,
        "api_secret": API_SECRET_FACE,
        "return_attributes": "emotion"
    }

    response = requests.post(FACE_URL, files=files, data=params)
    st.write(response.json())  # debug output

    faces = response.json().get("faces", [])

    if faces:

        emotions = faces[0]["attributes"]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)

        return dominant_emotion

    return None


# ---------------------------
# MEAL RECOMMENDATION
# ---------------------------

def recommend_meals(emotion):

    query_map = {
        "anger": "spicy",
        "happiness": "healthy",
        "sadness": "comfort food",
        "fear": "comfort food",
        "neutral": "quick meals",
        "surprise": "refreshing"
    }

    query = query_map.get(emotion, "food")

    params = {
        "query": query,
        "number": 5,
        "apiKey": API_KEY_SPOONACULAR
    }

    response = requests.get(SPOONACULAR_URL, params=params)

    meals = response.json().get("results", [])

    return [meal["title"] for meal in meals]


# ---------------------------
# MOVIE RECOMMENDATION
# ---------------------------

def recommend_movies(emotion):

    genre_map = {
        "anger": "Action",
        "happiness": "Comedy",
        "sadness": "Drama",
        "fear": "Horror",
        "neutral": "Family",
        "surprise": "Thriller"
    }

    genre = genre_map.get(emotion, "Comedy")

    params = {
        "apikey": OMDB_API_KEY,
        "s": genre,
        "type": "movie"
    }

    response = requests.get(OMDB_URL, params=params)

    movies = response.json().get("Search", [])

    return [movie["Title"] for movie in movies[:5]]


# ---------------------------
# MUSIC RECOMMENDATION
# ---------------------------

def recommend_music(emotion):

    fallback_music = {
        "sadness": ["Someone Like You", "Fix You", "Let Her Go"],
        "happiness": ["Happy", "Shake It Off", "Can't Stop The Feeling"],
        "anger": ["Numb", "Enter Sandman", "Stronger"],
        "neutral": ["Perfect", "Let It Be", "Thinking Out Loud"],
        "fear": ["Boulevard of Broken Dreams", "Demons", "Creep"],
        "surprise": ["Get Lucky", "Blinding Lights", "Uptown Funk"]
    }

    try:

        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
        )

        results = sp.search(q="pop", type="track", limit=5)

        tracks = results["tracks"]["items"]

        return [track["name"] for track in tracks]

    except:

        return fallback_music.get(emotion, ["Music unavailable"])


# ---------------------------
# MAIN APP LOGIC
# ---------------------------

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    emotion = detect_emotion(uploaded_file)

    if emotion:

        st.success(f"Detected Emotion: **{emotion.upper()}**")

        # MEALS
        st.subheader("🍜 Meal Recommendations")

        meals = recommend_meals(emotion)

        for meal in meals:
            st.write("•", meal)

        # MOVIES
        st.subheader("🎬 Movie Recommendations")

        movies = recommend_movies(emotion)

        for movie in movies:
            st.write("•", movie)

        # MUSIC
        st.subheader("🎵 Music Recommendations")

        music = recommend_music(emotion)

        for m in music:
            st.write("•", m)

    else:

        st.error("No face detected. Please upload a clearer image.")