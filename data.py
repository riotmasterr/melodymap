"""
data.py
-------
Static dataset for MelodyMap: artists, songs, and the genre-similarity
lookup used by the weight function.

In a production deployment this would be replaced by a database
connection or an external API call (Spotify, MusicBrainz, etc.).
"""

# --------------------------------------------------------------------------
# Genre similarity matrix
#
# Values in [0, 1] where 1.0 = identical genre, 0.0 = entirely unrelated.
# Order does not matter: lookups in recommender.py try both directions.
# --------------------------------------------------------------------------
GENRE_SIMILARITY = {
    ("electronic", "electronic"): 1.0,
    ("electronic", "pop"):        0.7,
    ("electronic", "rock"):       0.5,
    ("electronic", "r&b"):        0.6,
    ("electronic", "k-pop"):      0.5,
    ("pop", "pop"):               1.0,
    ("pop", "r&b"):               0.8,
    ("pop", "rock"):              0.6,
    ("pop", "k-pop"):             0.8,
    ("rock", "rock"):             1.0,
    ("rock", "k-pop"):            0.4,
    ("r&b", "r&b"):               1.0,
    ("r&b", "k-pop"):             0.6,
    ("k-pop", "k-pop"):           1.0,
}

DEFAULT_GENRE_SIMILARITY = 0.3  # Fallback for unknown genre pairs

# --------------------------------------------------------------------------
# Artist dataset
# --------------------------------------------------------------------------
ARTISTS_DATA = {
    "Daft Punk": {
        "genre": "electronic",
        "color": "#00d9ff",
        "related": [
            {"name": "Pharrell Williams", "genre": "r&b",        "popularity": 95},
            {"name": "Tame Impala",       "genre": "rock",       "popularity": 90},
            {"name": "Justice",           "genre": "electronic", "popularity": 85},
            {"name": "Mark Ronson",       "genre": "pop",        "popularity": 80},
            {"name": "Kavinsky",          "genre": "electronic", "popularity": 70},
            {"name": "The Weeknd",        "genre": "r&b",        "popularity": 96},
            {"name": "Gorillaz",          "genre": "electronic", "popularity": 88},
            {"name": "Calvin Harris",     "genre": "electronic", "popularity": 92},
        ],
    },
    "Taylor Swift": {
        "genre": "pop",
        "color": "#ff1493",
        "related": [
            {"name": "Selena Gomez",    "genre": "pop", "popularity": 90},
            {"name": "Ed Sheeran",      "genre": "pop", "popularity": 95},
            {"name": "Lana Del Rey",    "genre": "pop", "popularity": 85},
            {"name": "Olivia Rodrigo",  "genre": "pop", "popularity": 92},
            {"name": "Ariana Grande",   "genre": "pop", "popularity": 98},
            {"name": "Billie Eilish",   "genre": "pop", "popularity": 96},
        ],
    },
    "The Weeknd": {
        "genre": "r&b",
        "color": "#ff4444",
        "related": [
            {"name": "Drake",        "genre": "r&b", "popularity": 97},
            {"name": "Post Malone",  "genre": "pop", "popularity": 92},
            {"name": "Travis Scott", "genre": "r&b", "popularity": 90},
            {"name": "SZA",          "genre": "r&b", "popularity": 89},
            {"name": "Frank Ocean",  "genre": "r&b", "popularity": 91},
        ],
    },
    "BTS": {
        "genre": "k-pop",
        "color": "#9b59b6",
        "related": [
            {"name": "Blackpink",   "genre": "k-pop", "popularity": 97},
            {"name": "EXO",         "genre": "k-pop", "popularity": 89},
            {"name": "Seventeen",   "genre": "k-pop", "popularity": 85},
            {"name": "Stray Kids",  "genre": "k-pop", "popularity": 90},
            {"name": "TWICE",       "genre": "k-pop", "popularity": 91},
        ],
    },
    "Coldplay": {
        "genre": "rock",
        "color": "#ffd700",
        "related": [
            {"name": "Imagine Dragons", "genre": "rock", "popularity": 95},
            {"name": "OneRepublic",     "genre": "rock", "popularity": 88},
            {"name": "U2",              "genre": "rock", "popularity": 87},
            {"name": "Muse",            "genre": "rock", "popularity": 86},
            {"name": "The Killers",     "genre": "rock", "popularity": 89},
        ],
    },
}

# --------------------------------------------------------------------------
# Song dataset
#
# Each seed song has audio features. The similar songs are computed
# dynamically in recommender.py using Euclidean distance on
# (BPM, energy, danceability), so we keep the candidate pool here.
# --------------------------------------------------------------------------
SONG_CATALOG = [
    # Seed tracks (these are searchable from the home screen)
    {"name": "Blinding Lights",     "artist": "The Weeknd",  "genre": "pop",        "bpm": 171, "energy": 73, "danceability": 51, "seed": True},
    {"name": "Shape of You",        "artist": "Ed Sheeran",  "genre": "pop",        "bpm": 96,  "energy": 65, "danceability": 83, "seed": True},
    {"name": "One More Time",       "artist": "Daft Punk",   "genre": "electronic", "bpm": 123, "energy": 78, "danceability": 61, "seed": True},
    {"name": "Dynamite",            "artist": "BTS",         "genre": "k-pop",      "bpm": 114, "energy": 74, "danceability": 75, "seed": True},
    {"name": "Yellow",              "artist": "Coldplay",    "genre": "rock",       "bpm": 87,  "energy": 58, "danceability": 35, "seed": True},

    # Candidate pool used to populate "Similar Songs"
    {"name": "Save Your Tears",       "artist": "The Weeknd",   "genre": "pop",        "bpm": 118, "energy": 68, "danceability": 65},
    {"name": "Levitating",            "artist": "Dua Lipa",     "genre": "pop",        "bpm": 103, "energy": 82, "danceability": 88},
    {"name": "Don't Start Now",       "artist": "Dua Lipa",     "genre": "pop",        "bpm": 124, "energy": 79, "danceability": 79},
    {"name": "Starboy",               "artist": "The Weeknd",   "genre": "pop",        "bpm": 186, "energy": 59, "danceability": 67},
    {"name": "Perfect",               "artist": "Ed Sheeran",   "genre": "pop",        "bpm": 95,  "energy": 44, "danceability": 60},
    {"name": "Thinking Out Loud",     "artist": "Ed Sheeran",   "genre": "pop",        "bpm": 79,  "energy": 40, "danceability": 78},
    {"name": "Cheap Thrills",         "artist": "Sia",          "genre": "pop",        "bpm": 130, "energy": 75, "danceability": 80},
    {"name": "Get Lucky",             "artist": "Daft Punk",    "genre": "electronic", "bpm": 116, "energy": 81, "danceability": 79},
    {"name": "Around the World",      "artist": "Daft Punk",    "genre": "electronic", "bpm": 121, "energy": 71, "danceability": 82},
    {"name": "Feel Good Inc.",        "artist": "Gorillaz",     "genre": "electronic", "bpm": 139, "energy": 82, "danceability": 73},
    {"name": "Butter",                "artist": "BTS",          "genre": "k-pop",      "bpm": 110, "energy": 80, "danceability": 76},
    {"name": "Permission to Dance",   "artist": "BTS",          "genre": "k-pop",      "bpm": 125, "energy": 72, "danceability": 70},
    {"name": "How You Like That",     "artist": "Blackpink",    "genre": "k-pop",      "bpm": 132, "energy": 83, "danceability": 64},
    {"name": "Fix You",               "artist": "Coldplay",     "genre": "rock",       "bpm": 138, "energy": 48, "danceability": 35},
    {"name": "The Scientist",         "artist": "Coldplay",     "genre": "rock",       "bpm": 146, "energy": 45, "danceability": 30},
    {"name": "Chasing Cars",          "artist": "Snow Patrol",  "genre": "rock",       "bpm": 102, "energy": 42, "danceability": 33},
    {"name": "Viva La Vida",          "artist": "Coldplay",     "genre": "rock",       "bpm": 138, "energy": 62, "danceability": 49},
    {"name": "Heat Waves",            "artist": "Glass Animals","genre": "pop",        "bpm": 81,  "energy": 53, "danceability": 76},
    {"name": "As It Was",             "artist": "Harry Styles", "genre": "pop",        "bpm": 174, "energy": 73, "danceability": 52},
]
