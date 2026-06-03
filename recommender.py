"""
recommender.py
--------------
Recommendation engine for MelodyMap.

Provides:
  * compute_artist_weight     -> edge weight between two artists
  * build_artist_graph        -> assembles the WeightedGraph
  * get_artist_recommendations-> tiered (Level 1/2/3) artist suggestions
  * audio_feature_similarity  -> normalized Euclidean similarity on
                                 (BPM, energy, danceability)
  * get_similar_songs         -> top-N songs ranked by audio similarity
"""

import math
from typing import Dict, List, Optional

from graph import WeightedGraph
from data import (
    ARTISTS_DATA,
    SONG_CATALOG,
    GENRE_SIMILARITY,
    DEFAULT_GENRE_SIMILARITY,
)


# ============================================================
# Genre similarity lookup (order-independent)
# ============================================================
def genre_score(g1: str, g2: str) -> float:
    """Return the genre similarity score between two genre strings."""
    a, b = g1.lower(), g2.lower()
    if (a, b) in GENRE_SIMILARITY:
        return GENRE_SIMILARITY[(a, b)]
    if (b, a) in GENRE_SIMILARITY:
        return GENRE_SIMILARITY[(b, a)]
    return DEFAULT_GENRE_SIMILARITY


# ============================================================
# Artist edge weight
#   weight = 0.9 * genre_score + 0.1 * (popularity / 100)
# Bounded in [0, 1].
# ============================================================
def compute_artist_weight(artist_genre: str, related_genre: str,
                          popularity: float) -> float:
    g = genre_score(artist_genre, related_genre)
    pop_normalized = max(0.0, min(100.0, popularity)) / 100.0
    weight = 0.9 * g + 0.1 * pop_normalized
    return round(weight, 3)


# ============================================================
# Graph construction
# ============================================================
def build_artist_graph() -> WeightedGraph:
    """Build the full artist graph from ARTISTS_DATA."""
    g = WeightedGraph()
    for artist, info in ARTISTS_DATA.items():
        g.add_vertex(artist)
        for related in info["related"]:
            w = compute_artist_weight(
                info["genre"],
                related["genre"],
                related["popularity"],
            )
            g.add_edge(artist, related["name"], w)
    return g


# ============================================================
# Tiered artist recommendations
#   Level 1: weight >= 0.8 (very similar)
#   Level 2: 0.6 <= weight < 0.8 (related)
#   Level 3: weight < 0.6 (loosely related)
# ============================================================
def get_artist_recommendations(graph: WeightedGraph,
                               artist_name: str) -> Optional[Dict]:
    """Return tiered recommendations for an artist, or None if unknown."""
    if artist_name not in ARTISTS_DATA:
        return None

    neighbors = graph.get_weighted_neighbors(artist_name)
    info = ARTISTS_DATA[artist_name]

    level1, level2, level3 = [], [], []
    for n in neighbors:
        w = n["weight"]
        if w >= 0.8:
            level1.append(n)
        elif w >= 0.6:
            level2.append(n)
        else:
            level3.append(n)

    return {
        "artist": artist_name,
        "genre": info["genre"],
        "color": info["color"],
        "levels": {
            "level1": level1,
            "level2": level2,
            "level3": level3,
        },
    }


# ============================================================
# Audio-feature similarity for songs
#
# Each song has (bpm, energy, danceability).
# We min-max normalize BPM into roughly [0, 1] using a 60..200 range
# (energy and danceability are already 0..100).
# Similarity = 1 - (Euclidean distance / sqrt(3)).
#
# This is true content-based filtering: similar audio profiles
# get ranked highly regardless of artist or genre.
# ============================================================
BPM_MIN, BPM_MAX = 60.0, 200.0


def _normalize(song: Dict) -> List[float]:
    bpm_norm = (song["bpm"] - BPM_MIN) / (BPM_MAX - BPM_MIN)
    bpm_norm = max(0.0, min(1.0, bpm_norm))
    return [
        bpm_norm,
        song["energy"] / 100.0,
        song["danceability"] / 100.0,
    ]


def audio_feature_similarity(song_a: Dict, song_b: Dict) -> float:
    """
    Cosine-of-Euclidean-style similarity in [0, 1] between two songs.
    Higher = more similar.
    """
    va, vb = _normalize(song_a), _normalize(song_b)
    sq = sum((a - b) ** 2 for a, b in zip(va, vb))
    dist = math.sqrt(sq)
    max_dist = math.sqrt(3)   # max possible distance in unit cube
    return 1.0 - (dist / max_dist)


def get_similar_songs(song_name: str, top_n: int = 5) -> Optional[Dict]:
    """Return the seed song plus its top-N most audio-similar candidates."""
    seed = next(
        (s for s in SONG_CATALOG
         if s["name"].lower() == song_name.lower() and s.get("seed")),
        None,
    )
    if seed is None:
        return None

    scored = []
    for candidate in SONG_CATALOG:
        if candidate["name"] == seed["name"]:
            continue
        sim = audio_feature_similarity(seed, candidate)
        scored.append({
            "name":          candidate["name"],
            "artist":        candidate["artist"],
            "genre":         candidate["genre"],
            "bpm":           candidate["bpm"],
            "energy":        candidate["energy"],
            "danceability":  candidate["danceability"],
            "similarity":    round(sim * 100, 1),
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    top = scored[:top_n]

    return {
        "artist":       seed["artist"],
        "genre":        seed["genre"],
        "bpm":          seed["bpm"],
        "energy":       seed["energy"],
        "danceability": seed["danceability"],
        "similar":      top,
    }


def list_seed_songs() -> List[str]:
    return [s["name"] for s in SONG_CATALOG if s.get("seed")]


def seed_songs_data() -> Dict[str, Dict]:
    """Compact dict of seed songs, used by GET /api/songs."""
    return {
        s["name"]: {
            "artist":       s["artist"],
            "genre":        s["genre"],
            "bpm":          s["bpm"],
            "energy":       s["energy"],
            "danceability": s["danceability"],
        }
        for s in SONG_CATALOG if s.get("seed")
    }
