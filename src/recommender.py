from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Score a song based on user preferences using a point-weighting algorithm.
    
    Maximum possible score: 30.75 points
    - Genre match: 1.25 points
    - Mood match: 2.0 points
    - Energy: 6.0 points (distance-based)
    - Valence: 3.0 points (distance-based)
    - Danceability: 3.0 points (distance-based)
    - Acousticness: 3.0 points (distance-based)
    - Tempo: 2.5 points (distance-based)
    - Song Popularity: 2.0 points (popularity-based)
    - Release Decade: 2.0 points (exact/close match)
    - Detailed Moods: 2.5 points (tag matching)
    - Artist Popularity: 1.5 points (popularity-based, weighted less)
    - Song Length: 2.0 points (distance-based)
    
    Args:
        song: Dictionary with keys: id, title, artist, genre, mood, energy, tempo_bpm, 
              valence, danceability, acousticness, song_popularity, release_decade, 
              detailed_moods, artist_popularity, song_length_seconds
        user_prefs: Dictionary with:
            - preferred_genres: List[str]
            - preferred_moods: List[str]
            - target_energy: float (0-1)
            - target_valence: float (0-1)
            - target_danceability: float (0-1)
            - target_acousticness: float (0-1)
            - target_tempo_bpm: float (60-180)
            - prefer_popular_songs: bool
            - preferred_release_decades: List[str]
            - preferred_mood_tags: List[str]
            - target_artist_popularity: float (0-100)
            - target_song_length_seconds: float (120-400)
            
    Returns:
        Tuple of (normalized_score: float [0-100], reasons: List[str])
    """
    points = 0.0
    reasons = []
    
    # Genre match (1.25 points)
    if song.get('genre') in user_prefs.get('preferred_genres', []):
        points += 1.25
        reasons.append(f"✓ Genre match: {song.get('genre')} (+1.25)")
    
    # Mood match (2.0 points)
    if song.get('mood') in user_prefs.get('preferred_moods', []):
        points += 2.0
        reasons.append(f"✓ Mood match: {song.get('mood')} (+2.0)")
    
    # Energy (0-6.0 points)
    energy_distance = abs(song.get('energy', 0.0) - user_prefs.get('target_energy', 0.5))
    energy_points, energy_reason = _calculate_energy_score_0_to_6(energy_distance)
    points += energy_points
    reasons.append(
        f"Energy: {song.get('energy', 0.0):.2f} vs {user_prefs.get('target_energy', 0.5):.2f} "
        f"({energy_reason}) (+{energy_points:.2f})"
    )
    
    # Valence (0-3.0 points)
    valence_distance = abs(song.get('valence', 0.0) - user_prefs.get('target_valence', 0.5))
    valence_points, valence_reason = _calculate_distance_score_0_to_3(valence_distance)
    points += valence_points
    reasons.append(
        f"Valence: {song.get('valence', 0.0):.2f} vs {user_prefs.get('target_valence', 0.5):.2f} "
        f"({valence_reason}) (+{valence_points:.2f})"
    )
    
    # Danceability (0-3.0 points)
    dance_distance = abs(song.get('danceability', 0.0) - user_prefs.get('target_danceability', 0.5))
    dance_points, dance_reason = _calculate_distance_score_0_to_3(dance_distance)
    points += dance_points
    reasons.append(
        f"Danceability: {song.get('danceability', 0.0):.2f} vs {user_prefs.get('target_danceability', 0.5):.2f} "
        f"({dance_reason}) (+{dance_points:.2f})"
    )
    
    # Acousticness (0-3.0 points)
    acoustic_distance = abs(song.get('acousticness', 0.0) - user_prefs.get('target_acousticness', 0.5))
    acoustic_points, acoustic_reason = _calculate_distance_score_0_to_3(acoustic_distance)
    points += acoustic_points
    reasons.append(
        f"Acousticness: {song.get('acousticness', 0.0):.2f} vs {user_prefs.get('target_acousticness', 0.5):.2f} "
        f"({acoustic_reason}) (+{acoustic_points:.2f})"
    )
    
    # Tempo (0-2.5 points)
    tempo_distance = abs(song.get('tempo_bpm', 120.0) - user_prefs.get('target_tempo_bpm', 120.0))
    tempo_points, tempo_reason = _calculate_tempo_score(tempo_distance)
    points += tempo_points
    reasons.append(
        f"Tempo: {song.get('tempo_bpm', 120.0):.0f} BPM vs {user_prefs.get('target_tempo_bpm', 120.0):.0f} BPM "
        f"({tempo_reason}) (+{tempo_points:.2f})"
    )
    
    # Song Popularity (0-2.0 points)
    song_pop = song.get('song_popularity', 50)
    prefer_popular = user_prefs.get('prefer_popular_songs', False)
    pop_points, pop_reason = _calculate_popularity_score(song_pop, prefer_popular, weight=1.0)
    points += pop_points
    reasons.append(f"Song Popularity: {pop_reason}")
    
    # Release Decade (0-2.0 points)
    song_decade = song.get('release_decade', '2010s')
    pref_decades = user_prefs.get('preferred_release_decades', [])
    decade_points, decade_reason = _calculate_decade_score(song_decade, pref_decades)
    points += decade_points
    reasons.append(f"Release Decade: {decade_reason}")
    
    # Detailed Moods (0-2.5 points)
    song_moods_str = song.get('detailed_moods', '')
    pref_mood_tags = user_prefs.get('preferred_mood_tags', [])
    mood_points, mood_reason = _calculate_mood_tags_score(song_moods_str, pref_mood_tags)
    points += mood_points
    reasons.append(f"Mood Tags: {mood_reason}")
    
    # Artist Popularity (0-1.5 points)
    artist_pop = song.get('artist_popularity', 50)
    artist_pop_points, artist_pop_reason = _calculate_popularity_score(artist_pop, prefer_popular, weight=0.75)
    points += artist_pop_points
    reasons.append(f"Artist Popularity: {artist_pop_reason}")
    
    # Song Length (0-2.0 points)
    song_length = song.get('song_length_seconds', 240)
    target_length = user_prefs.get('target_song_length_seconds', 240.0)
    length_points, length_reason = _calculate_song_length_score(song_length, target_length)
    points += length_points
    reasons.append(f"Song Length: {length_reason}")
    
    # Normalize to 0-100 scale
    normalized_score = (points / 30.75) * 100
    
    return normalized_score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Score all songs and return top-K recommendations with explanations.
    
    Args:
        user_prefs: User preferences dictionary
        songs: List of song dictionaries
        k: Number of top recommendations to return
        
    Returns:
        List of (song_dict, normalized_score, explanation_string) tuples, sorted by score descending
    """
    if not songs:
        return []
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(song, user_prefs)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top-K
    return scored_songs[:k]
