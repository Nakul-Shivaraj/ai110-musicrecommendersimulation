"""
Command line runner for the Music Recommender Simulation.

Tests diverse user profiles to evaluate recommender behavior:
- Control profile (normal preferences)
- Contradictory preferences (conflicting attributes)
- Extreme preferences (edge case values)
- Niche preferences (narrow genre focus)
- Genre-heavy vs. feature-heavy profiles
"""

from .recommender import load_songs, recommend_songs


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


def format_recommendation(song, score, explanation, rank):
    """Format a single recommendation nicely."""
    output = f"\n{rank}. {song['title']} - {song['artist']}"
    output += f"\n   Score: {score:.1f}/100"
    output += f"\n   Breakdown:"
    reasons = explanation.split(" | ")
    for reason in reasons:
        output += f"\n      • {reason}"
    return output


def main() -> None:
    songs = load_songs("data/songs.csv")
    
    print(f"\n[MUSIC RECOMMENDER SIMULATION - STRESS TEST]")
    print(f"Loaded songs: {len(songs)} songs from catalog\n")
    
    # Test each profile
    for profile in USER_PROFILES:
        print("=" * 90)
        print(f"\n[TEST PROFILE: {profile['name']}]")
        print(f"   Genres: {', '.join(profile['preferred_genres'])}")
        print(f"   Moods: {', '.join(profile['preferred_moods'])}")
        print(f"   Targets: Energy {profile['target_energy']}, Valence {profile['target_valence']}, "
              f"Danceability {profile['target_danceability']}", end="")
        print(f"\n            Acousticness {profile['target_acousticness']}, "
              f"Tempo {profile['target_tempo_bpm']} BPM\n")
        
        recommendations = recommend_songs(profile, songs, k=5)
        
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            print(format_recommendation(song, score, explanation, i))
        
        print()
    
    print("=" * 90)
    print("\n[STRESS TEST COMPLETE]")


if __name__ == "__main__":
    main()
