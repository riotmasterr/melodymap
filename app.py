"""
app.py
------
MelodyMap Flask application.

A graph-based music recommendation system. Artist recommendations use a
weighted undirected graph (genre similarity + popularity). Song
recommendations use content-based filtering on audio features
(BPM, energy, danceability).

Run:
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000 in your browser.
"""

import logging
from typing import Tuple

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from data import ARTISTS_DATA
from recommender import (
    build_artist_graph,
    get_artist_recommendations,
    get_similar_songs,
    list_seed_songs,
    seed_songs_data,
)


# ----------------------------------------------------------------------
# App setup
# ----------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("melodymap")

# Build the artist graph once at startup
ARTIST_GRAPH = build_artist_graph()
log.info(
    "Artist graph built: %d vertices, %d edges",
    ARTIST_GRAPH.vertex_count(),
    ARTIST_GRAPH.edge_count(),
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def json_error(message: str, status: int) -> Tuple:
    return jsonify({"error": message, "status": status}), status


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    """Lightweight health check."""
    return jsonify({
        "status":   "ok",
        "service":  "melodymap",
        "vertices": ARTIST_GRAPH.vertex_count(),
        "edges":    ARTIST_GRAPH.edge_count(),
    })


@app.route("/api/artists")
def get_artists():
    """Return every seed artist plus their metadata."""
    return jsonify({
        "artists": list(ARTISTS_DATA.keys()),
        "data":    ARTISTS_DATA,
    })


@app.route("/api/songs")
def get_songs():
    """Return every seed song plus its audio features."""
    return jsonify({
        "songs": list_seed_songs(),
        "data":  seed_songs_data(),
    })


@app.route("/api/artist/<artist_name>")
def artist_recommendations(artist_name: str):
    """Tiered recommendations (Level 1/2/3) for a given seed artist."""
    result = get_artist_recommendations(ARTIST_GRAPH, artist_name)
    if result is None:
        log.info("Artist not found: %s", artist_name)
        return json_error(f"Artist '{artist_name}' not found.", 404)
    return jsonify(result)


@app.route("/api/song/<song_name>")
def song_recommendations(song_name: str):
    """Audio-feature-based similar songs for a given seed song."""
    top_n = request.args.get("top_n", default=5, type=int)
    top_n = max(1, min(top_n, 20))   # clamp to a sane range

    result = get_similar_songs(song_name, top_n=top_n)
    if result is None:
        log.info("Song not found: %s", song_name)
        return json_error(f"Song '{song_name}' not found.", 404)
    return jsonify({"song": song_name, "data": result})


@app.route("/api/search")
def search():
    """
    Case-insensitive substring search across artists and songs.

    Query params:
        q     - the search string (required)
        mode  - 'artist' or 'song' (optional, default 'all')
    """
    query = request.args.get("q", "").strip().lower()
    mode = request.args.get("mode", "all").lower()

    if not query:
        return json_error("Query parameter 'q' is required.", 400)

    results = {"artists": [], "songs": []}
    if mode in ("artist", "all"):
        results["artists"] = [
            name for name in ARTISTS_DATA if query in name.lower()
        ]
    if mode in ("song", "all"):
        results["songs"] = [
            name for name in list_seed_songs() if query in name.lower()
        ]
    return jsonify(results)


# ----------------------------------------------------------------------
# Error handlers
# ----------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_err):
    return json_error("Endpoint not found.", 404)


@app.errorhandler(500)
def internal_error(_err):
    log.exception("Internal server error")
    return json_error("Internal server error.", 500)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
