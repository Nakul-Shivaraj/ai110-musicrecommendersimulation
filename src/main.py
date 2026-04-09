"""
Command line runner for the Music Recommender Simulation.

Tests diverse user profiles to evaluate recommender behavior:
- Control profile (normal preferences)
- Contradictory preferences (conflicting attributes)
- Extreme preferences (edge case values)
- Niche preferences (narrow genre focus)
- Genre-heavy vs. feature-heavy profiles
"""

from tabulate import tabulate

from .recommender import AVAILABLE_SCORING_MODES, load_songs, recommend_songs

SCORING_MODE = "genre-first"

# Define diverse user profiles for stress testing
USER_PROFILES = [
    {
        "name": "Lofi Devotee (Control)",
        "preferred_genres": ["lofi", "ambient"],
        "preferred_moods": ["chill", "focused"],
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
        "target_tempo_bpm": 75,
        "prefer_popular_songs": False,
        "preferred_release_decades": ["2020s", "2010s"],
        "preferred_mood_tags": ["chill", "nostalgic", "peaceful"],
        "target_artist_popularity": 70.0,
        "target_song_length_seconds": 200.0
    },
    {
        "name": "Confused Party Animal",
        "preferred_genres": ["lofi", "ambient"],
        "preferred_moods": ["intense", "happy"],
        "target_energy": 0.90,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.05,
        "target_tempo_bpm": 140,
        "prefer_popular_songs": True,
        "preferred_release_decades": ["2010s", "2020s"],
        "preferred_mood_tags": ["energetic", "intense", "happy"],
        "target_artist_popularity": 80.0,
        "target_song_length_seconds": 240.0
    },
    {
        "name": "Maximum Maximalist (Extremes)",
        "preferred_genres": ["rock"],
        "preferred_moods": ["intense"],
        "target_energy": 0.95,
        "target_valence": 0.95,
        "target_danceability": 0.95,
        "target_acousticness": 0.02,
        "target_tempo_bpm": 165,
        "prefer_popular_songs": True,
        "preferred_release_decades": ["2000s", "2010s"],
        "preferred_mood_tags": ["aggressive", "intense", "energetic"],
        "target_artist_popularity": 85.0,
        "target_song_length_seconds": 300.0
    },
    {
        "name": "Jazz Snob (Niche)",
        "preferred_genres": ["jazz"],
        "preferred_moods": ["relaxed"],
        "target_energy": 0.35,
        "target_valence": 0.70,
        "target_danceability": 0.50,
        "target_acousticness": 0.90,
        "target_tempo_bpm": 92,
        "prefer_popular_songs": False,
        "preferred_release_decades": ["1980s", "1970s"],
        "preferred_mood_tags": ["relaxed", "sophisticated", "smooth"],
        "target_artist_popularity": 60.0,
        "target_song_length_seconds": 260.0
    },
    {
        "name": "Mood Ring Enthusiast (Genre-Heavy)",
        "preferred_genres": ["lofi", "ambient", "jazz"],
        "preferred_moods": ["chill", "focused", "relaxed"],
        "target_energy": 0.50,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
        "target_tempo_bpm": 80,
        "prefer_popular_songs": False,
        "preferred_release_decades": ["2020s", "2010s", "1980s"],
        "preferred_mood_tags": ["chill", "focused", "relaxed", "peaceful"],
        "target_artist_popularity": 65.0,
        "target_song_length_seconds": 220.0
    },
    {
        "name": "Audio Engineer (Feature-Heavy)",
        "preferred_genres": ["pop", "rock", "electronic", "hip-hop"],
        "preferred_moods": ["happy", "intense", "chill"],
        "target_energy": 0.75,
        "target_valence": 0.70,
        "target_danceability": 0.80,
        "target_acousticness": 0.25,
        "target_tempo_bpm": 115,
        "prefer_popular_songs": True,
        "preferred_release_decades": ["2010s", "2020s"],
        "preferred_mood_tags": ["energetic", "happy", "confident"],
        "target_artist_popularity": 75.0,
        "target_song_length_seconds": 230.0
    },
    {
        "name": "Median Listener (Neutral)",
        "preferred_genres": ["pop", "rock"],
        "preferred_moods": ["happy", "chill"],
        "target_energy": 0.50,
        "target_valence": 0.65,
        "target_danceability": 0.65,
        "target_acousticness": 0.45,
        "target_tempo_bpm": 100,
        "prefer_popular_songs": False,
        "preferred_release_decades": ["2010s", "2000s"],
        "preferred_mood_tags": ["happy", "chill", "uplifting"],
        "target_artist_popularity": 70.0,
        "target_song_length_seconds": 240.0
    }
]


_REASON_LABELS = {
    "Genre":       "Genre",
    "Mood":        "Mood",
    "Energy":      "Energy",
    "Valence":     "Valence",
    "Danceability":"Dance",
    "Acousticness":"Acoustic",
    "Tempo":       "Tempo",
    "Song Pop":    "SongPop",
    "Artist Pop":  "ArtistPop",
    "Release":     "Decade",
    "Mood Tags":   "MoodTags",
    "Song Length": "Length",
    "DIVERSITY":   "Diversity",
}

# Maximum characters allowed in the Reasons column before wrapping
_REASON_WRAP = 62


def _format_reasons(explanation: str) -> str:
    """
    Condense the pipe-separated explanation string into a compact,
    wrapped multi-line string suitable for a table cell.

    Each reason is shortened to 'Label: value' form and prefixed with
    a bullet so the cell stays readable at a glance.
    """
    parts = explanation.split(" | ")
    lines = []
    for part in parts:
        label = part.split(":")[0].strip()
        # Find the closest short label
        short = next(
            (v for k, v in _REASON_LABELS.items() if label.upper().startswith(k.upper())),
            label[:10],
        )
        lines.append(f"  {short}: {part.split(':', 1)[-1].strip()}")

    # Wrap long lines
    wrapped = []
    for line in lines:
        while len(line) > _REASON_WRAP:
            wrapped.append(line[:_REASON_WRAP])
            line = "    " + line[_REASON_WRAP:]
        wrapped.append(line)
    return "\n".join(wrapped)


def _build_table(recommendations) -> str:
    """
    Build a tabulate grid table for a list of (song, score, explanation)
    tuples.  Columns: Rank | Title | Artist | Genre | Score | Reasons.
    """
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        rows.append([
            rank,
            song.get("title", ""),
            song.get("artist", ""),
            song.get("genre", ""),
            f"{score:.1f}",
            _format_reasons(explanation),
        ])

    headers = ["#", "Title", "Artist", "Genre", "Score", "Reasons"]
    return tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[3, 22, 18, 12, 6, _REASON_WRAP])


def main() -> None:
    songs = load_songs("data/songs.csv")

    print(f"\n{'='*90}")
    print(f"  MUSIC RECOMMENDER SIMULATION - STRESS TEST")
    print(f"  {len(songs)} songs loaded  |  Scoring mode: {SCORING_MODE}")
    print(f"  Available modes: {', '.join(AVAILABLE_SCORING_MODES)}")
    print(f"{'='*90}")

    for profile in USER_PROFILES:
        print(f"\n  PROFILE: {profile['name']}")
        print(f"  Genres : {', '.join(profile['preferred_genres'])}")
        print(f"  Moods  : {', '.join(profile['preferred_moods'])}")
        print(
            f"  Targets: Energy {profile['target_energy']}  "
            f"Valence {profile['target_valence']}  "
            f"Danceability {profile['target_danceability']}  "
            f"Acousticness {profile['target_acousticness']}  "
            f"Tempo {profile['target_tempo_bpm']} BPM"
        )
        print()

        recommendations = recommend_songs(profile, songs, k=5, mode=SCORING_MODE)
        print(_build_table(recommendations))
        print()

    print(f"{'='*90}")
    print("  STRESS TEST COMPLETE\n")


if __name__ == "__main__":
    main()
