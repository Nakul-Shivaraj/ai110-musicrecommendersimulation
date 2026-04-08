# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This system implements a **content-based recommender** that matches songs to users based on song attributes (audio features and metadata) rather than collaborative filtering (learning from other users' behavior). Real-world systems like Spotify use hybrid approaches combining collaborative, content-based, and contextual signals, but our version prioritizes **simplicity and explainability**. We focus on quantifying musical "vibe" through features like energy, mood, and tempo—the primary factors that define whether a song matches a user's current taste.

**Song Features:**
- **Categorical**: `genre` (e.g., pop, lofi, rock), `mood` (e.g., happy, chill, intense)
- **Numerical (0-1 scale)**: `energy`, `valence` (positivity), `danceability`, `acousticness`
- **Metadata**: `tempo_bpm`, `title`, `artist`, `id`

**UserProfile Information:**
- **Target preferences**: `target_energy`, `target_valence`, `target_danceability`, `target_acousticness`, `target_tempo_bpm`
- **Categorical preferences**: `preferred_genres` (list), `preferred_moods` (list)
- **Feature weights**: How much each feature matters (e.g., energy_weight=0.4, genre_weight=0.3)

**Algorithm Recipe (Point-Weighting System):**

The recommender scores each song using a point-based system with a theoretical maximum of **19.0 points**:

| Feature | Points | Calculation |
|---------|--------|-------------|
| **Genre Match** | +2.5 | If song genre ∈ preferred_genres |
| **Mood Match** | +2.0 | If song mood ∈ preferred_moods |
| **Energy** | 0–3.0 | Distance-based: 3.0 if |song_energy - target| ≤ 0.10; decays with distance |
| **Valence** | 0–3.0 | Distance-based: max 3.0 points for closeness to target valence |
| **Danceability** | 0–3.0 | Distance-based: max 3.0 points for closeness to target danceability |
| **Acousticness** | 0–3.0 | Distance-based: max 3.0 points for closeness to target acousticness |
| **Tempo (BPM)** | 0–2.5 | 2.5 if |song_tempo - target_tempo| ≤ 10 BPM; decays with distance |

**Final Score: `(raw_points / 19.0) × 100`** → Normalized to 0–100 scale for intuitive interpretation.

**Ranking and Recommendation Process:**
1. **Score all songs**: Load catalog (18 songs from CSV) and apply point-weighting formula to each
2. **Sort descending**: Rank by raw points, highest first
3. **Select top-K**: Return top K recommendations (e.g., top 5) with explanations showing which features matched

**Example Score Calculation** (User prefers lofi/chill, target energy 0.45):
- "Library Rain" (lofi, chill, energy 0.35): Genre match (+2.5) + Mood match (+2.0) + Energy match (3.0) + other features = **98.3/100** ✨
- "Island Vibes" (reggae, uplifting, energy 0.58): Energy close (+2.7) + Valence close (+2.8) = **73.7/100** ✓
- "Burning Skies" (metal, aggressive, energy 0.96): No genre/mood match, poor energy fit = **17.4/100** ✗

**Expected Biases and Limitations:**
- **Genre over-prioritization**: With +2.5 for genre match, songs outside preferred genres start at a disadvantage, potentially creating "filter bubbles" and suppressing cross-genre discovery (e.g., a great reggae song never gets recommended to a lofi-heavy user).
- **Narrow categorical filtering**: Only 4 preferred genres means ~78% of diverse songs are genre mismatches from the start, limiting serendipity.
- **No semantic understanding**: System can't evaluate lyrics, instrumentals, or nuanced qualities like "nostalgic" or "intimate"—only quantifiable audio features.
- **Limited dataset**: With only 18 songs, recommendations are constrained; real systems have millions of tracks.
- **No collaborative signals**: System ignores what other users like; can't discover emerging artists or cross-community tastes.
- **Feature extraction limits**: Energy and valence are approximations; the "vibe" of a song is multidimensional and subjective.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

