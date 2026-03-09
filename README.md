# Emotion-Based Meal, Movie & Music Recommendation System

## Overview

This project detects a user's facial emotion and recommends meals, movies, and music based on the detected emotion.

The system captures an image using a webcam or allows the user to upload an image. It then analyzes facial emotions and provides personalized recommendations.

## Features

• Facial emotion detection using Face++ API  
• Meal recommendations using Spoonacular API  
• Movie recommendations using OMDB API  
• Music recommendations using Spotify API  
• Webcam capture or image upload  
• Recommendation history saved in a file  
• Fallback music suggestions if Spotify API fails  

## Technologies Used

Python  
OpenCV  
Face++ API  
Spoonacular API  
OMDB API  
Spotify API  
Tkinter  

## How to Run the Project

1. Install required libraries

```
pip install -r requirements.txt
```

2. Run the program

```
python main.py
```

3. Capture image or upload image

The system will detect emotion and provide recommendations.

## Example Output

Emotion Detected: Sadness

Meals:
Comfort Food Suggestions

Movies:
Drama Movies

Music:
Emotional Songs

## Author

Harsh Madkaikar