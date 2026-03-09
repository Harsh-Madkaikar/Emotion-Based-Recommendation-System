import cv2
import requests
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import filedialog
import logging

# Disable Spotify error logs
logging.getLogger("spotipy").setLevel(logging.CRITICAL)

# -------------------------------
# API KEYS
# -------------------------------

API_KEY_FACE = 'Y50yFX-T_tOMTRmo_VvSqbAZGG324n3b' 
API_SECRET_FACE = '6nT63UxBINvwLPRqpQEjpZ8j_UcWJ0xh'
API_URL_FACE = "https://api-us.faceplusplus.com/facepp/v3/detect"

API_KEY_SPOONACULAR = '03eaef7233bf4c88a2aee399a15a59b0'
SPOONACULAR_URL = "https://api.spoonacular.com/recipes/complexSearch"

OMDB_API_KEY = '86a9fe15' 
OMDB_URL = "http://www.omdbapi.com/"

SPOTIFY_CLIENT_ID = 'f07d6ff0d29449dba36598db280138d4' 
SPOTIFY_CLIENT_SECRET = 'c5e2dff72b3a45b081f97e812b86276d' 

history_text_file = "recommendation_history.txt"

# -------------------------------
# EMOTION DETECTION
# -------------------------------

def get_emotion_from_face(image_path):

    image_data = open(image_path, "rb").read()

    files = {"image_file": image_data}

    params = {
        "api_key": API_KEY_FACE,
        "api_secret": API_SECRET_FACE,
        "return_attributes": "emotion"
    }

    response = requests.post(API_URL_FACE, files=files, data=params)

    response.raise_for_status()

    faces = response.json().get("faces", [])

    if faces:

        emotions = faces[0]["attributes"]["emotion"]

        print("Detected emotions:", emotions)

        dominant_emotion = max(emotions, key=emotions.get)

        return dominant_emotion

    else:

        return None


# -------------------------------
# MEAL RECOMMENDATION
# -------------------------------

def recommend_meal_from_spoonacular(emotion):

    meal_map = {
        "anger": "spicy food",
        "happiness": "healthy food",
        "sadness": "comfort food",
        "fear": "comfort food",
        "neutral": "easy meals",
        "surprise": "refreshing meals"
    }

    search_term = meal_map.get(emotion, "easy meals")

    params = {
        "query": search_term,
        "number": 10,
        "apiKey": API_KEY_SPOONACULAR
    }

    try:

        response = requests.get(SPOONACULAR_URL, params=params)

        meals = response.json().get("results", [])

        if meals:
            return [meal["title"] for meal in meals]

        else:
            return ["No meals found"]

    except:

        return ["Meal recommendation unavailable"]


# -------------------------------
# MOVIE RECOMMENDATION
# -------------------------------

def recommend_movies_from_omdb(emotion):

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

    try:

        response = requests.get(OMDB_URL, params=params)

        movies = response.json().get("Search", [])

        if movies:
            return [movie["Title"] for movie in movies]

        else:
            return ["No movies found"]

    except:

        return ["Movie recommendation unavailable"]


# -------------------------------
# MUSIC RECOMMENDATION
# -------------------------------

def recommend_music_from_spotify(emotion):

    emotion_artist_map = {
        "anger": "Metallica",
        "happiness": "Taylor Swift",
        "sadness": "Adele",
        "fear": "Linkin Park",
        "neutral": "Ed Sheeran",
        "surprise": "Daft Punk"
    }

    artist = emotion_artist_map.get(emotion, "Coldplay")

    try:

        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        results = sp.search(q=artist, type="track", limit=5)

        tracks = results["tracks"]["items"]

        if tracks:

            return [track["name"] for track in tracks]

        else:

            return ["No music found"]

    except:

        print("Spotify unavailable. Using fallback music recommendations.")

        fallback_music = {
            "sadness": [
                "Someone Like You - Adele",
                "Fix You - Coldplay",
                "Let Her Go - Passenger"
            ],
            "happiness": [
                "Happy - Pharrell Williams",
                "Shake It Off - Taylor Swift",
                "Can't Stop The Feeling - Justin Timberlake"
            ],
            "anger": [
                "Numb - Linkin Park",
                "Enter Sandman - Metallica",
                "Stronger - Kanye West"
            ],
            "neutral": [
                "Perfect - Ed Sheeran",
                "Let It Be - Beatles",
                "Thinking Out Loud - Ed Sheeran"
            ],
            "fear": [
                "Boulevard of Broken Dreams - Green Day",
                "Demons - Imagine Dragons",
                "Creep - Radiohead"
            ],
            "surprise": [
                "Get Lucky - Daft Punk",
                "Blinding Lights - The Weeknd",
                "Uptown Funk - Bruno Mars"
            ]
        }

        return fallback_music.get(emotion, ["Music unavailable"])


# -------------------------------
# SAVE HISTORY
# -------------------------------

def save_to_history(image_path, emotion, meals, movies, music):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_text_file, "a") as f:

        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Image Path: {image_path}\n")
        f.write(f"Detected Emotion: {emotion}\n")
        f.write(f"Meal Suggestions: {', '.join(meals)}\n")
        f.write(f"Movie Suggestions: {', '.join(movies)}\n")
        f.write(f"Music Suggestions: {', '.join(music)}\n")
        f.write("-" * 50 + "\n")


# -------------------------------
# IMAGE UPLOAD
# -------------------------------

def upload_image():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    return file_path


# -------------------------------
# WEBCAM CAPTURE
# -------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Camera not accessible")

else:

    print("Press SPACE to capture")
    print("Press U to upload image")
    print("Press ESC to exit")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:

            image_filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            cv2.imwrite(image_filename, frame)

            print("Image saved:", image_filename)

            break

        elif key == ord("u"):

            image_filename = upload_image()

            if image_filename:

                print("Image uploaded:", image_filename)

                break

        elif key == 27:

            print("Exited")

            break

    cap.release()

    cv2.destroyAllWindows()


# -------------------------------
# RUN SYSTEM
# -------------------------------

emotion = get_emotion_from_face(image_filename)

if emotion:

    print("Detected Emotion:", emotion)

    meals = recommend_meal_from_spoonacular(emotion)
    print("Meals:", meals)

    movies = recommend_movies_from_omdb(emotion)
    print("Movies:", movies)

    music = recommend_music_from_spotify(emotion)
    print("Music:", music)

    save_to_history(image_filename, emotion, meals, movies, music)

else:

    print("No face detected")