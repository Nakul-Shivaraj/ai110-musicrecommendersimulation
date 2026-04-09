from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import csv
import logging
from pathlib import Path

# Configure logging for error tracking
logger = logging.getLogger(__name__)

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    song_popularity: int
    release_decade: str
    detailed_moods: str
    artist_popularity: int
    song_length_seconds: int

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    prefer_popular_songs: bool
    preferred_decades: List[str]
    preferred_moods_list: List[str]
    target_artist_popularity: float
    target_song_length_seconds: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return "Explanation placeholder"


class ScoringStrategy(ABC):
    """Strategy interface for scoring songs."""
    name: str = "balanced"
    genre_weight: float = 1.0
    mood_weight: float = 1.0
    energy_weight: float = 1.0
    valence_weight: float = 1.0
    danceability_weight: float = 1.0
    acousticness_weight: float = 1.0
    tempo_weight: float = 1.0
    popularity_weight: float = 1.0
    decade_weight: float = 1.0
    detailed_mood_weight: float = 1.0
    artist_popularity_weight: float = 1.0
    length_weight: float = 1.0

    @property
    def max_points(self) -> float:
        return (
            1.25 * self.genre_weight
            + 2.0 * self.mood_weight
            + 6.0 * self.energy_weight
            + 3.0 * self.valence_weight
            + 3.0 * self.danceability_weight
            + 3.0 * self.acousticness_weight
            + 2.5 * self.tempo_weight
            + 2.0 * self.popularity_weight
            + 2.0 * self.decade_weight
            + 2.5 * self.detailed_mood_weight
            + 1.5 * self.artist_popularity_weight
            + 2.0 * self.length_weight
        )

    def score(self, song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
        points = 0.0
        reasons: List[str] = []

        # Genre match
        if song.get("genre") in user_prefs.get("preferred_genres", []):
            genre_points = 1.25 * self.genre_weight
            points += genre_points
            reasons.append(f"Genre match: {song.get('genre')} (+{genre_points:.2f})")

        # Mood match
        if song.get("mood") in user_prefs.get("preferred_moods", []):
            mood_points = 2.0 * self.mood_weight
            points += mood_points
            reasons.append(f"Mood match: {song.get('mood')} (+{mood_points:.2f})")

        # Energy
        energy_distance = abs(song.get("energy", 0.0) - user_prefs.get("target_energy", 0.5))
        energy_points, energy_reason = _calculate_energy_score_0_to_6(energy_distance)
        weighted_energy = energy_points * self.energy_weight
        points += weighted_energy
        reasons.append(
            f"Energy: {song.get('energy', 0.0):.2f} vs {user_prefs.get('target_energy', 0.5):.2f} "
            f"({energy_reason}) (+{weighted_energy:.2f})"
        )

        # Valence
        valence_distance = abs(song.get("valence", 0.0) - user_prefs.get("target_valence", 0.5))
        valence_points, valence_reason = _calculate_distance_score_0_to_3(valence_distance)
        weighted_valence = valence_points * self.valence_weight
        points += weighted_valence
        reasons.append(
            f"Valence: {song.get('valence', 0.0):.2f} vs {user_prefs.get('target_valence', 0.5):.2f} "
            f"({valence_reason}) (+{weighted_valence:.2f})"
        )

        # Danceability
        dance_distance = abs(song.get("danceability", 0.0) - user_prefs.get("target_danceability", 0.5))
        dance_points, dance_reason = _calculate_distance_score_0_to_3(dance_distance)
        weighted_dance = dance_points * self.danceability_weight
        points += weighted_dance
        reasons.append(
            f"Danceability: {song.get('danceability', 0.0):.2f} vs {user_prefs.get('target_danceability', 0.5):.2f} "
            f"({dance_reason}) (+{weighted_dance:.2f})"
        )

        # Acousticness
        acoustic_distance = abs(song.get("acousticness", 0.0) - user_prefs.get("target_acousticness", 0.5))
        acoustic_points, acoustic_reason = _calculate_distance_score_0_to_3(acoustic_distance)
        weighted_acoustic = acoustic_points * self.acousticness_weight
        points += weighted_acoustic
        reasons.append(
            f"Acousticness: {song.get('acousticness', 0.0):.2f} vs {user_prefs.get('target_acousticness', 0.5):.2f} "
            f"({acoustic_reason}) (+{weighted_acoustic:.2f})"
        )

        # Tempo
        tempo_distance = abs(song.get("tempo_bpm", 120.0) - user_prefs.get("target_tempo_bpm", 120.0))
        tempo_points, tempo_reason = _calculate_tempo_score(tempo_distance)
        weighted_tempo = tempo_points * self.tempo_weight
        points += weighted_tempo
        reasons.append(
            f"Tempo: {song.get('tempo_bpm', 120.0):.0f} BPM vs {user_prefs.get('target_tempo_bpm', 120.0):.0f} BPM "
            f"({tempo_reason}) (+{weighted_tempo:.2f})"
        )

        # Song popularity
        song_pop = song.get("song_popularity", 50)
        prefer_popular = user_prefs.get("prefer_popular_songs", False)
        pop_points, pop_reason = _calculate_popularity_score(song_pop, prefer_popular, weight=self.popularity_weight)
        points += pop_points
        reasons.append(f"Song Popularity: {pop_reason}")

        # Decade
        song_decade = song.get("release_decade", "2010s")
        pref_decades = user_prefs.get("preferred_release_decades", [])
        decade_points, decade_reason = _calculate_decade_score(song_decade, pref_decades)
        weighted_decade = decade_points * self.decade_weight
        points += weighted_decade
        reasons.append(
            f"Release Decade: {decade_reason} (weighted x{self.decade_weight:.2f} = +{weighted_decade:.2f})"
        )

        # Detailed mood tags
        song_moods_str = song.get("detailed_moods", "")
        pref_mood_tags = user_prefs.get("preferred_mood_tags", [])
        mood_points, mood_reason = _calculate_mood_tags_score(song_moods_str, pref_mood_tags)
        weighted_mood = mood_points * self.detailed_mood_weight
        points += weighted_mood
        reasons.append(
            f"Mood Tags: {mood_reason} (weighted x{self.detailed_mood_weight:.2f} = +{weighted_mood:.2f})"
        )

        # Artist popularity
        artist_pop = song.get("artist_popularity", 50)
        artist_pop_points, artist_pop_reason = _calculate_popularity_score(
            artist_pop,
            prefer_popular,
            weight=0.75 * self.artist_popularity_weight,
        )
        points += artist_pop_points
        reasons.append(f"Artist Popularity: {artist_pop_reason}")

        # Song length
        song_length = song.get("song_length_seconds", 240)
        target_length = user_prefs.get("target_song_length_seconds", 240.0)
        length_points, length_reason = _calculate_song_length_score(song_length, target_length)
        weighted_length = length_points * self.length_weight
        points += weighted_length
        reasons.append(
            f"Song Length: {length_reason} (weighted x{self.length_weight:.2f} = +{weighted_length:.2f})"
        )

        normalized_score = 0.0
        if self.max_points > 0:
            normalized_score = (points / self.max_points) * 100

        return normalized_score, reasons


class BalancedScoringStrategy(ScoringStrategy):
    name = "balanced"


class GenreFirstScoringStrategy(ScoringStrategy):
    name = "genre-first"
    genre_weight = 1.5
    mood_weight = 1.2
    energy_weight = 0.9
    tempo_weight = 0.9
    length_weight = 0.9


class MoodFirstScoringStrategy(ScoringStrategy):
    name = "mood-first"
    genre_weight = 1.1
    mood_weight = 1.5
    detailed_mood_weight = 1.3
    acousticness_weight = 0.9
    popularity_weight = 0.9


class EnergyFocusedScoringStrategy(ScoringStrategy):
    name = "energy-focused"
    genre_weight = 0.9
    energy_weight = 1.4
    tempo_weight = 1.2
    danceability_weight = 1.1
    popularity_weight = 0.9


AVAILABLE_SCORING_MODES = [
    BalancedScoringStrategy.name,
    GenreFirstScoringStrategy.name,
    MoodFirstScoringStrategy.name,
    EnergyFocusedScoringStrategy.name,
]


def get_scoring_strategy(mode: str) -> ScoringStrategy:
    normalized_mode = mode.strip().lower()
    if normalized_mode == GenreFirstScoringStrategy.name:
        return GenreFirstScoringStrategy()
    if normalized_mode == MoodFirstScoringStrategy.name:
        return MoodFirstScoringStrategy()
    if normalized_mode == EnergyFocusedScoringStrategy.name:
        return EnergyFocusedScoringStrategy()
    return BalancedScoringStrategy()


def load_songs(csv_path: str) -> List[Dict]:
    """
    Load song data from a CSV file and return as a list of dictionaries.
    
    Converts numerical columns to appropriate types:
    - id, song_popularity, artist_popularity, song_length_seconds: int
    - tempo_bpm, energy, valence, danceability, acousticness: float
    
    String columns (genre, mood, title, artist, release_decade, detailed_moods) remain as strings.
    
    Args:
        csv_path: Path to the CSV file containing song data
        
    Returns:
        List of dictionaries, each representing one song with keys matching CSV headers.
        Returns empty list if file doesn't exist or can't be read.
    """
    songs = []
    
    # Numeric columns that need type conversion
    int_columns = {'id', 'song_popularity', 'artist_popularity', 'song_length_seconds'}
    float_columns = {'tempo_bpm', 'energy', 'valence', 'danceability', 'acousticness'}
    
    try:
        # Check if file exists
        path = Path(csv_path)
        if not path.exists():
            logger.warning(f"CSV file not found: {csv_path}")
            print(f"Error: CSV file not found at {csv_path}")
            return songs
        
        # Read CSV file
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validate headers exist
            if reader.fieldnames is None:
                logger.error(f"CSV file is empty or malformed: {csv_path}")
                print(f"Error: CSV file is empty or malformed")
                return songs
            
            # Process each row
            for row in reader:
                try:
                    converted_row = {}
                    
                    for key, value in row.items():
                        if key in int_columns:
                            # Convert to int
                            converted_row[key] = int(value) if value.strip() else None
                        elif key in float_columns:
                            # Convert to float
                            converted_row[key] = float(value) if value.strip() else None
                        else:
                            # Keep as string
                            converted_row[key] = value.strip()
                    
                    songs.append(converted_row)
                    
                except (ValueError, TypeError) as e:
                    logger.warning(f"Skipping row due to conversion error: {row}. Error: {e}")
                    continue
        
        logger.info(f"Successfully loaded {len(songs)} songs from {csv_path}")
        return songs
    
    except FileNotFoundError:
        logger.warning(f"CSV file not found: {csv_path}")
        print(f"Error: CSV file not found at {csv_path}")
        return songs
    except IOError as e:
        logger.error(f"Error reading CSV file {csv_path}: {e}")
        print(f"Error reading CSV file: {e}")
        return songs
    except Exception as e:
        logger.error(f"Unexpected error loading songs from {csv_path}: {e}")
        print(f"Error loading songs: {e}")
        return songs


# ============================================================================
# SCORING FUNCTIONS - Point-weighting algorithm for song recommendations
# ============================================================================

def _calculate_distance_score_0_to_3(distance: float) -> Tuple[float, str]:
    """
    Calculate points for attributes with 0-3.0 point scale based on distance.
    Used for: Valence, Danceability, Acousticness
    
    Args:
        distance: Absolute difference between song attribute and user target
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    if distance <= 0.10:
        return 3.0, "Perfect match"
    elif distance <= 0.30:
        points = 4.0 - (10 * distance)
        return max(0.0, points), f"Close match (distance: {distance:.2f})"
    elif distance <= 0.50:
        points = 2.5 - (5 * distance)
        return max(0.0, points), f"Moderate match (distance: {distance:.2f})"
    else:
        return 0.0, f"Poor match (distance: {distance:.2f})"


def _calculate_energy_score_0_to_6(distance: float) -> Tuple[float, str]:
    """
    Calculate points for energy with 0-6.0 point scale based on distance.
    Double the original 0-3.0 scale to emphasize energy matching.
    
    Args:
        distance: Absolute difference between song energy and user target
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    if distance <= 0.10:
        return 6.0, "Perfect match"
    elif distance <= 0.30:
        points = 8.0 - (20 * distance)
        return max(0.0, points), f"Close match (distance: {distance:.2f})"
    elif distance <= 0.50:
        points = 5.0 - (10 * distance)
        return max(0.0, points), f"Moderate match (distance: {distance:.2f})"
    else:
        return 0.0, f"Poor match (distance: {distance:.2f})"


def _calculate_tempo_score(distance: float) -> Tuple[float, str]:
    """
    Calculate points for tempo with 0-2.5 point scale based on BPM distance.
    
    Args:
        distance: Absolute difference in BPM from target tempo
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    if distance <= 10:
        return 2.5, "Perfect tempo match"
    elif distance <= 30:
        points = 3.25 - (0.075 * distance)
        return max(0.0, points), f"Close tempo match ({distance:.0f} BPM diff)"
    elif distance <= 50:
        points = 2.5 - (0.05 * distance)
        return max(0.0, points), f"Moderate tempo match ({distance:.0f} BPM diff)"
    else:
        return 0.0, f"Poor tempo match ({distance:.0f} BPM diff)"


def _calculate_popularity_score(song_pop: int, user_prefers_popular: bool, weight: float = 1.0) -> Tuple[float, str]:
    """
    Calculate points for song popularity based on user preference.
    
    If user prefers popular songs, score is proportional to the song's popularity (0-100).
    If user doesn't care about popularity, give neutral score.
    
    Args:
        song_pop: Song popularity score (0-100)
        user_prefers_popular: Whether user prefers popular songs
        weight: Multiplier for the score (default 1.0 for song popularity, 0.75 for artist popularity)
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    max_points = 2.0 * weight
    
    if user_prefers_popular:
        # Higher popularity = higher score, normalized to max_points
        points = (song_pop / 100.0) * max_points
        match_text = "Matches popularity preference"
    else:
        # User doesn't care; give middle score
        points = max_points * 0.5
        match_text = "Neutral on popularity"
    
    return points, f"{match_text} ({song_pop}/100) (+{points:.2f})"


def _calculate_decade_score(song_decade: str, preferred_decades: List[str]) -> Tuple[float, str]:
    """
    Calculate points for release decade matching.
    
    Exact match: 2.0 points
    Decade within ±20 years (adjacent decades): 1.0 points
    Otherwise: 0.0 points
    
    Args:
        song_decade: Song's release decade as string (e.g., "2010s", "1980s")
        preferred_decades: List of user's preferred decades (e.g., ["1980s", "1990s"])
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    if not preferred_decades:
        return 0.0, "No decade preferences"
    
    # Extract decade year (e.g., "2010s" -> 2010)
    try:
        song_year = int(song_decade[:4])
    except (ValueError, IndexError):
        return 0.0, f"Invalid decade format: {song_decade}"
    
    for pref_decade in preferred_decades:
        try:
            pref_year = int(pref_decade[:4])
        except (ValueError, IndexError):
            continue
        
        year_diff = abs(song_year - pref_year)
        
        if year_diff == 0:
            return 2.0, f"Exact decade match: {song_decade} (+2.0)"
        elif year_diff <= 20:
            return 1.0, f"Close decade match: {song_decade} (within 20 years) (+1.0)"
    
    return 0.0, f"No decade match: {song_decade} (+0.0)"


def _calculate_mood_tags_score(song_moods_str: str, preferred_moods: List[str]) -> Tuple[float, str]:
    """
    Calculate points for detailed mood tag matching.
    
    Scores based on count of matching mood tags:
    - 3+ matches: 2.5 points
    - 2 matches: 2.0 points
    - 1 match: 1.0 points
    - 0 matches: 0.0 points
    
    Args:
        song_moods_str: Comma-separated mood tags from the song (e.g., "chill,nostalgic")
        preferred_moods: List of user's preferred mood tags
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    if not preferred_moods:
        return 0.0, "No mood tag preferences"
    
    # Parse song moods
    song_moods = [m.strip().lower() for m in song_moods_str.split(',')]
    preferred_moods_lower = [m.strip().lower() for m in preferred_moods]
    
    # Count matches
    matches = [mood for mood in song_moods if mood in preferred_moods_lower]
    match_count = len(matches)
    
    if match_count >= 3:
        points = 2.5
        reason = f"Multiple mood matches: {', '.join(matches)} (+2.5)"
    elif match_count == 2:
        points = 2.0
        reason = f"Two mood matches: {', '.join(matches)} (+2.0)"
    elif match_count == 1:
        points = 1.0
        reason = f"One mood match: {matches[0]} (+1.0)"
    else:
        points = 0.0
        reason = f"No mood matches (+0.0)"
    
    return points, reason


def _calculate_song_length_score(song_length: int, target_length: float) -> Tuple[float, str]:
    """
    Calculate points for song length based on user's target length.
    
    Scoring with 0-2.0 point scale based on distance from target:
    - Within 10 seconds: 2.0 points (perfect match)
    - Within 30 seconds: 1.5-2.0 points (close match)
    - Within 60 seconds: 1.0-1.5 points (moderate match)
    - Otherwise: 0.0-1.0 points (poor match)
    
    Args:
        song_length: Song length in seconds
        target_length: User's target song length in seconds
        
    Returns:
        Tuple of (points: float, reason: str)
    """
    distance = abs(song_length - target_length)
    
    if distance <= 10:
        return 2.0, f"Perfect length match: {song_length}s vs target {target_length:.0f}s (+2.0)"
    elif distance <= 30:
        points = 2.0 - (0.0167 * distance)  # Decrease from 2.0 to 1.5 over 30 seconds
        return max(0.0, points), f"Close length match: {distance:.0f}s difference (+{points:.2f})"
    elif distance <= 60:
        points = 1.5 - (0.0083 * distance)  # Decrease from 1.5 to 1.0 over 30 more seconds
        return max(0.0, points), f"Moderate length match: {distance:.0f}s difference (+{points:.2f})"
    else:
        points = max(0.0, 1.0 - (0.005 * (distance - 60)))  # Gradual decrease to 0
        return points, f"Poor length match: {distance:.0f}s difference (+{points:.2f})"


def score_song(song: Dict, user_prefs: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score a song using the requested scoring strategy mode."""
    return get_scoring_strategy(mode).score(song, user_prefs)


def _apply_diversity_penalty(
    candidate: Dict,
    selected: List[Dict],
    artist_penalty: float = 0.35,
    genre_penalty: float = 0.20,
) -> Tuple[float, List[str]]:
    """
    Calculate cumulative diversity penalties for a candidate song based on
    artists and genres already present in the selected list.

    Each duplicate artist already selected incurs an `artist_penalty` multiplier
    reduction (e.g. 0.35 means the score is multiplied by 0.65).  Each duplicate
    genre already selected incurs a `genre_penalty` multiplier reduction.
    Penalties compound multiplicatively so a second repeat hurts more than the
    first.

    Args:
        candidate:      Song dict being evaluated.
        selected:       Songs already chosen for the recommendation list.
        artist_penalty: Score multiplier reduction per repeated artist (0-1).
        genre_penalty:  Score multiplier reduction per repeated genre  (0-1).

    Returns:
        Tuple of (total_multiplier, list_of_penalty_reason_strings).
        total_multiplier == 1.0 means no penalty; lower means penalised.
    """
    multiplier = 1.0
    reasons: List[str] = []

    candidate_artist = candidate.get("artist", "").strip().lower()
    candidate_genre = candidate.get("genre", "").strip().lower()

    artist_count = sum(
        1 for s in selected
        if s.get("artist", "").strip().lower() == candidate_artist
    )
    genre_count = sum(
        1 for s in selected
        if s.get("genre", "").strip().lower() == candidate_genre
    )

    if artist_count > 0:
        artist_multiplier = (1.0 - artist_penalty) ** artist_count
        multiplier *= artist_multiplier
        reasons.append(
            f"Artist '{candidate.get('artist')}' already appears {artist_count}x "
            f"-> artist penalty x{artist_multiplier:.2f}"
        )

    if genre_count > 0:
        genre_multiplier = (1.0 - genre_penalty) ** genre_count
        multiplier *= genre_multiplier
        reasons.append(
            f"Genre '{candidate.get('genre')}' already appears {genre_count}x "
            f"-> genre penalty x{genre_multiplier:.2f}"
        )

    return multiplier, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = True,
    artist_penalty: float = 0.35,
    genre_penalty: float = 0.20,
) -> List[Tuple[Dict, float, str]]:
    """
    Score all songs and return top-K recommendations with explanations.

    When diversity=True (default), a greedy selection loop applies cumulative
    penalties to candidates that repeat an artist or genre already in the
    result list.  This prevents any single artist or genre from dominating
    the top results (filter-bubble mitigation).

    Args:
        user_prefs:     User preferences dictionary.
        songs:          List of song dictionaries.
        k:              Number of top recommendations to return.
        mode:           Scoring strategy ('balanced', 'genre-first', etc.).
        diversity:      Enable diversity penalties (default True).
        artist_penalty: Score multiplier reduction per repeated artist (0-1).
        genre_penalty:  Score multiplier reduction per repeated genre  (0-1).

    Returns:
        List of (song_dict, penalized_score, explanation_string) tuples,
        sorted by final score descending.
    """
    if not songs:
        return []

    strategy = get_scoring_strategy(mode)

    # Step 1 — score every song against the user profile
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        raw_score, reasons = strategy.score(song, user_prefs)
        explanation = " | ".join(reasons)
        scored.append((song, raw_score, explanation))

    if not diversity:
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    # Step 2 — greedy diversity-aware selection
    # Keep a pool of remaining candidates (mutable scores).
    pool: List[Tuple[Dict, float, str]] = list(scored)
    selected: List[Dict] = []
    results: List[Tuple[Dict, float, str]] = []

    while len(results) < k and pool:
        # Re-score every remaining candidate with current diversity penalties
        penalized_pool: List[Tuple[Dict, float, str]] = []
        for song, base_score, explanation in pool:
            multiplier, penalty_reasons = _apply_diversity_penalty(
                song, selected, artist_penalty, genre_penalty
            )
            penalized_score = base_score * multiplier
            full_explanation = explanation
            if penalty_reasons:
                full_explanation += " | DIVERSITY: " + "; ".join(penalty_reasons)
            penalized_pool.append((song, penalized_score, full_explanation))

        # Pick the highest-scoring candidate after penalties
        penalized_pool.sort(key=lambda x: x[1], reverse=True)
        best_song, best_score, best_explanation = penalized_pool[0]

        results.append((best_song, best_score, best_explanation))
        selected.append(best_song)

        # Remove the chosen song from the pool (match by song id)
        best_id = best_song.get("id")
        pool = [(s, sc, ex) for s, sc, ex in pool if s.get("id") != best_id]

    return results
