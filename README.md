# Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender that scores songs against a user taste profile and returns the top-K matches with full scoring explanations. It supports four scoring modes (balanced, genre-first, mood-first, energy-focused), a diversity penalty to prevent artist/genre repetition in results, and a tabulate-formatted terminal table that shows every scoring reason per recommendation.

---

## How The System Works

This system implements a **content-based recommender** — it matches songs to users based on song attributes, not other users' behavior (collaborative filtering). Each song is scored using a point-weighting algorithm across 12 features, normalized to a 0–100 scale.

**Song Features:**
- **Categorical**: `genre`, `mood`, `detailed_moods` (comma-separated tags)
- **Numerical (0–1)**: `energy`, `valence`, `danceability`, `acousticness`
- **Metadata**: `tempo_bpm`, `song_popularity`, `artist_popularity`, `release_decade`, `song_length_seconds`

**User Preferences:**
- `preferred_genres`, `preferred_moods`, `preferred_mood_tags`, `preferred_release_decades`
- `target_energy`, `target_valence`, `target_danceability`, `target_acousticness`, `target_tempo_bpm`
- `target_song_length_seconds`, `target_artist_popularity`, `prefer_popular_songs`

Each of the 12 features (genre, mood, energy, valence, danceability, acousticness, tempo, popularity, decade, mood tags, artist popularity, song length) earns points based on how closely the song matches the user's targets. Raw points are normalized to a 0–100 score. Full scoring details are in [model_card.md](model_card.md).

**Diversity Penalty:**  
A greedy selection loop applies compounding penalties — 35% per repeated artist, 20% per repeated genre — so no single artist or genre dominates the top results.

**Ranking:**
1. Score every song against the user profile
2. Greedy selection with per-round diversity re-scoring
3. Return top-K with full explanation strings

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac / Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Example Output

```
==========================================================================================
  MUSIC RECOMMENDER SIMULATION - STRESS TEST
  18 songs loaded  |  Scoring mode: genre-first
==========================================================================================

  PROFILE: Lofi Devotee (Control)
  Genres : lofi, ambient
  Moods  : chill, focused

+---+------------------+-------------+--------+-------+----------------------------------+
| # | Title            | Artist      | Genre  | Score | Reasons                          |
+===+==================+=============+========+=======+==================================+
| 1 | Midnight Coding  | LoRoom      | lofi   |  93.3 | Genre: lofi (+1.88)              |
|   |                  |             |        |       |   Mood: chill (+2.40)            |
|   |                  |             |        |       |   Energy: Perfect match (+5.40)  |
|   |                  |             |        |       |   ...                            |
+---+------------------+-------------+--------+-------+----------------------------------+
```

Each row shows rank, song info, normalized score (0–100), and a full per-feature breakdown including any diversity penalties applied.

---

## Experiments Tried

### 7 Diverse Stress-Test Profiles

| Profile | Key Conflict | Finding |
|---|---|---|
| Lofi Devotee (control) | None | Perfect scores when preferences are coherent |
| Confused Party Animal | Wants lofi but high energy | Numerical features override genre labels |
| Maximum Maximalist | Extreme targets (0.95+) | Graceful degradation, no perfect match exists |
| Jazz Snob | Single niche genre | Filter bubble — only 1 jazz song in catalog |
| Mood Ring Enthusiast | Broad genre/mood list | High diversity in top results |
| Audio Engineer | Specific numerics, broad genre | Features drive results even across genres |
| Median Listener | Middle-ground everything | Average preferences → average, undifferentiated results |

**Key finding:** When genre and feature preferences conflict (e.g., wants lofi + high energy), the algorithm sides with features because the 12 numerical dimensions outweigh the binary genre match. Genre weight needs to be higher or the conflict needs explicit handling.

---

## Limitations and Risks

- **Tiny catalog**: 18 songs is not enough to evaluate diversity or filter bubbles meaningfully.
- **No lyric/semantic understanding**: Cannot capture "nostalgic" or "intimate" qualities — only quantifiable attributes.
- **Popularity bias**: Songs with high `song_popularity` get surfaced more for users who prefer popular content, reinforcing a "rich get richer" pattern.
- **Era bias**: Decade preferences create temporal filter bubbles; users may never hear music outside their preferred era.
- **No collaborative signal**: Cannot discover what other users with similar tastes enjoy, limiting serendipity.
- **Genre over-simplification**: Adjacent genres (synthwave vs. lofi) are treated as completely unrelated if neither is in the preferred list.

---

## Reflection

Building this system made the "black box" of recommenders concrete. Every weight is a design choice that encodes assumptions about what matters — and the stress tests showed those assumptions break quickly. The Confused Party Animal profile exposed a real tension: a user who says "I want lofi" but has high-energy targets gets pop music, because 12 numerical features mathematically outweigh one genre label. That's not a bug; it's what the weights say. Changing the outcome means changing the weights, which means deciding whose preference signal to trust more — and that is a value judgment, not a math problem.

The diversity penalty in Challenge 3 made this even clearer. The "most accurate" result list and the "best" result list are not the same thing. Without the penalty, LoRoom appeared twice and lofi took three of five slots for a user who nominally just wanted "chill music." The fix — intentionally penalizing repeat artists and genres — is a deliberate override of accuracy in favor of fairness and variety. Real platforms like Spotify make this exact trade-off. Building it from scratch here made it obvious that features like Discover Weekly are not neutral math — they are policy decisions baked into code.

---

## Model Card

See [model_card.md](model_card.md) for full documentation of intended use, data, biases, evaluation, and future work.
