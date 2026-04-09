from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
            song_popularity=85,
            release_decade="2020s",
            detailed_moods="uplifting,energetic,happy",
            artist_popularity=80,
            song_length_seconds=200,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
            song_popularity=65,
            release_decade="2020s",
            detailed_moods="chill,nostalgic,peaceful",
            artist_popularity=75,
            song_length_seconds=180,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        prefer_popular_songs=True,
        preferred_decades=["2020s", "2010s"],
        preferred_moods_list=["uplifting", "energetic"],
        target_artist_popularity=80.0,
        target_song_length_seconds=200.0,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        prefer_popular_songs=True,
        preferred_decades=["2020s", "2010s"],
        preferred_moods_list=["uplifting", "energetic"],
        target_artist_popularity=80.0,
        target_song_length_seconds=200.0,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)


def test_recommend_songs_accepts_scoring_modes():
    user = {
        "preferred_genres": ["pop"],
        "preferred_moods": ["happy"],
        "target_energy": 0.8,
        "target_valence": 0.8,
        "target_danceability": 0.7,
        "target_acousticness": 0.2,
        "target_tempo_bpm": 120,
        "prefer_popular_songs": True,
        "preferred_release_decades": ["2010s"],
        "preferred_mood_tags": ["uplifting"],
        "target_artist_popularity": 80.0,
        "target_song_length_seconds": 200.0,
    }
    rec = make_small_recommender()
    recommendations = recommend_songs(user, [
        {
            "id": 1,
            "title": "Test Pop Track",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
            "song_popularity": 85,
            "release_decade": "2020s",
            "detailed_moods": "uplifting,energetic,happy",
            "artist_popularity": 80,
            "song_length_seconds": 200,
        }
    ], k=1, mode="mood-first")

    assert len(recommendations) == 1
    assert isinstance(recommendations[0][2], str)
    explanation = recommendations[0][2]
    assert explanation.strip() != ""
