"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    
    print(f"Loaded songs: {len(songs)}")
    
    # User Profile: Alex (prefers chill lofi/jazz/folk music)
    user_prefs = {
        "name": "Alex",
        "preferred_genres": ["lofi", "jazz", "folk", "ambient"],
        "preferred_moods": ["chill", "relaxed", "contemplative"],
        "target_energy": 0.45,
        "target_valence": 0.65,
        "target_danceability": 0.60,
        "target_acousticness": 0.75,
        "target_tempo_bpm": 85
    }
    
    print(f"\n🎵 Recommendations for {user_prefs['name']}:")
    print(f"   Preferred genres: {', '.join(user_prefs['preferred_genres'])}")
    print(f"   Preferred moods: {', '.join(user_prefs['preferred_moods'])}")
    print(f"   Target vibe: Energy {user_prefs['target_energy']}, Acousticness {user_prefs['target_acousticness']}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("=" * 80)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n{i}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.1f}/100")
        print(f"   Breakdown:")
        # Parse explanations and print each reason indented
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"      • {reason}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
