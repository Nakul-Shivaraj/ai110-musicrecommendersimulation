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
    - id: int
    - tempo_bpm, energy, valence, danceability, acousticness: float
    
    String columns (genre, mood, title, artist) remain as strings.
    
    Args:
        csv_path: Path to the CSV file containing song data
        
    Returns:
        List of dictionaries, each representing one song with keys matching CSV headers.
        Returns empty list if file doesn't exist or can't be read.
    """
    songs = []
    
    # Numeric columns that need type conversion
    int_columns = {'id'}
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
    Used for: Energy, Valence, Danceability, Acousticness
    
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


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Score a song based on user preferences using a point-weighting algorithm.
    
    Maximum possible score: 19.0 points
    - Genre match: 2.5 points
    - Mood match: 2.0 points
    - Energy: 3.0 points (distance-based)
    - Valence: 3.0 points (distance-based)
    - Danceability: 3.0 points (distance-based)
    - Acousticness: 3.0 points (distance-based)
    - Tempo: 2.5 points (distance-based)
    
    Args:
        song: Dictionary with keys: id, title, artist, genre, mood, energy, 
              tempo_bpm, valence, danceability, acousticness
        user_prefs: Dictionary with:
            - preferred_genres: List[str]
            - preferred_moods: List[str]
            - target_energy: float (0-1)
            - target_valence: float (0-1)
            - target_danceability: float (0-1)
            - target_acousticness: float (0-1)
            - target_tempo_bpm: float (60-180)
            
    Returns:
        Tuple of (normalized_score: float [0-100], reasons: List[str])
    """
    points = 0.0
    reasons = []
    
    # Genre match (2.5 points)
    if song.get('genre') in user_prefs.get('preferred_genres', []):
        points += 2.5
        reasons.append(f"✓ Genre match: {song.get('genre')} (+2.5)")
    
    # Mood match (2.0 points)
    if song.get('mood') in user_prefs.get('preferred_moods', []):
        points += 2.0
        reasons.append(f"✓ Mood match: {song.get('mood')} (+2.0)")
    
    # Energy (0-3.0 points)
    energy_distance = abs(song.get('energy', 0.0) - user_prefs.get('target_energy', 0.5))
    energy_points, energy_reason = _calculate_distance_score_0_to_3(energy_distance)
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
    
    # Normalize to 0-100 scale
    normalized_score = (points / 19.0) * 100
    
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
