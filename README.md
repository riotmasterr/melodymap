# 🎵 MelodyMap
## 👥 Team

- **E Sai Brinda** — [@github-username](https://github.com/br-INDA)
- **Sreehitha G** — [@github-username](https://github.com/riotmasterr)
- **Harshith H** — [@github-username](https://github.com/harshith2006-coder)

> A graph-based music recommendation system that combines weighted-graph artist similarity with content-based audio-feature filtering for songs.

MelodyMap recommends music in two distinct ways:

- **Artists** — modeled as nodes in a weighted undirected graph. Edge weights combine genre compatibility (90%) with popularity (10%). Recommendations are returned in three tiers based on edge weight.
- **Songs** — ranked by audio-feature similarity. Each track has a `(BPM, energy, danceability)` feature vector; similar songs are found by Euclidean distance in the normalized feature space.

The frontend is a single-page D3.js visualization with radial graph layouts for artists and a card-based view for songs.

---

## ✨ Features

- 🕸️ Weighted undirected graph with adjacency-list representation
- 🎯 Tiered artist recommendations (Level 1 / 2 / 3 by similarity)
- 🎧 Content-based song filtering via normalized audio features
- 🔍 Substring search across artists and songs
- 🌐 RESTful Flask API with structured error responses
- 📊 Interactive D3.js radial visualization with hover tooltips
- 🩺 Health-check endpoint for monitoring

---

## 🛠️ Tech Stack

| Layer       | Technology               |
|-------------|--------------------------|
| Backend     | Python 3.9+ · Flask 3.0  |
| Frontend    | HTML5 · CSS3 · D3.js v7  |
| Algorithms  | Weighted graph, Euclidean similarity |

---

## 📁 Project Structure

```
melodymap/
├── app.py              # Flask routes + entry point
├── graph.py            # WeightedGraph data structure
├── recommender.py      # Graph builder + similarity engine
├── data.py             # Artist, song, and genre datasets
├── templates/
│   └── index.html      # D3.js frontend (single page)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/melodymap.git
cd melodymap

# (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
python app.py
```

Open your browser at **http://localhost:5000**.

---

## 🌐 API Reference

| Method | Endpoint                  | Description                                        |
|--------|---------------------------|----------------------------------------------------|
| GET    | `/`                       | Serves the frontend                                |
| GET    | `/api/health`             | Service health and graph stats                     |
| GET    | `/api/artists`            | List of seed artists and metadata                  |
| GET    | `/api/songs`              | List of seed songs with audio features             |
| GET    | `/api/artist/<name>`      | Tiered recommendations for an artist               |
| GET    | `/api/song/<name>`        | Audio-similar songs (optional `?top_n=` parameter) |
| GET    | `/api/search?q=<query>`   | Substring search (optional `?mode=artist\|song`)   |

### Example: artist recommendations

```bash
curl http://localhost:5000/api/artist/Daft%20Punk
```

```json
{
  "artist": "Daft Punk",
  "genre": "electronic",
  "color": "#00d9ff",
  "levels": {
    "level1": [{"node": "Calvin Harris", "weight": 0.992}, ...],
    "level2": [{"node": "Pharrell Williams", "weight": 0.695}, ...],
    "level3": [{"node": "Tame Impala", "weight": 0.54}]
  }
}
```

### Example: song recommendations

```bash
curl "http://localhost:5000/api/song/Blinding%20Lights?top_n=3"
```

---

## 🧠 How It Works

### Artist edge-weight formula

```
weight = 0.9 × genre_score + 0.1 × (popularity / 100)
```

`genre_score ∈ [0, 1]` comes from a hand-crafted genre-compatibility matrix; `popularity ∈ [0, 100]` is an artist-level score in the dataset.

### Recommendation tiers

| Tier      | Weight range  |
|-----------|---------------|
| Level 1   | `≥ 0.8`       |
| Level 2   | `0.6 – 0.8`   |
| Level 3   | `< 0.6`       |

### Song similarity

For two songs `a` and `b` with feature vectors normalized to `[0, 1]`:

```
similarity(a, b) = 1 − (||v_a − v_b||₂ / √3)
```

The cube root of 3 normalizes the maximum possible distance in a 3D unit cube, so the similarity score is always in `[0, 1]`.

---

## 🔮 Future Improvements

- Pull artist and song data dynamically from the Spotify Web API
- Add user accounts and a personal listening history
- Implement **collaborative filtering** alongside the content-based engine (hybrid recommender)
- Use embeddings (e.g. word2vec on playlists) instead of hand-crafted genre weights
- Add an LLM-powered "why was this recommended?" explanation layer
- Dockerize for one-command deployment
- Replace the in-memory data with PostgreSQL + a small caching layer

---

## 📄 License

Built for an academic course project (22AIE203 – Data Structures and Algorithms 2). Free to use and adapt for learning purposes.
