from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from spotify_client import search_tracks_by_genre

app = FastAPI(title= "AI Mood Playlist API")

from fastapi.middleware.cors import CORSMiddleware

# Allow your frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] if you want only local HTML
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS etc.
    allow_headers=["*"],   # allow Content-Type, Authorization etc.
)

#data models

class MoodRequest(BaseModel):
    mood: str

class Song(BaseModel):
    title: str
    artist: str

class PlaylistResponse(BaseModel):
    mood: str
    genres: List[str]
    songs: List[Song]

#Helper: Rule based mood to genres mapping
#for now rule based later if have accesss, integrate it with LLMs

def mood_to_genres(mood:str) -> List[str]:
    mood = mood.lower()
    if "happy" in mood or "excited" in mood:
        return ["pop", "dance"]
    elif "sad" in mood or "lonely" in mood:
        return ["acoustic", "singer-songwriter"]
    elif "relaxed" in mood or "calm" in mood:
        return ["chill", "ambient", "jazz"]
    elif "nostalgic" in mood or "retro" in mood:
        return ["classic rock", "90's"]
    else:
        return ["alternative"]

#End points

@app.get("/health")
def health_check():
    return{"status": "ok", "messsage": "API is running" }

@app.post("/playlist", response_model= PlaylistResponse)
def generate_playlist(req: MoodRequest):
    genres = mood_to_genres(req.mood)
    # For now, return mock songs (later Spotify API)
    #mock_songs = [
     #   {"title": "Sample Song 1", "artist": "Mock Artist"},
      #  {"title": "Sample Song 2", "artist": "Mock Artist"},
    #]
    
    # Fetching songs from spotify

    songs = search_tracks_by_genre(genres[0], limit=5)
    return {
        "mood": req.mood,
        "genres": genres,
        "songs": songs
    }




