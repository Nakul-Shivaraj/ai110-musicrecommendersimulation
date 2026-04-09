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

## Example Output: Recommendation CLI

When you run `python -m src.main`, the recommender generates personalized recommendations with detailed scoring explanations. Here's an example for a user who prefers chill lofi/jazz music:

```
Loaded songs: 18

🎵 Recommendations for Alex:
   Preferred genres: lofi, jazz, folk, ambient
   Preferred moods: chill, relaxed, contemplative
   Target vibe: Energy 0.45, Acousticness 0.75

================================================================================

1. Midnight Coding - LoRoom
   Score: 100.0/100
   Breakdown:
      • ✓ Genre match: lofi (+2.5)
      • ✓ Mood match: chill (+2.0)
      • Energy: 0.42 vs 0.45 (Perfect match) (+3.00)
      • Valence: 0.56 vs 0.65 (Perfect match) (+3.00)
      • Danceability: 0.62 vs 0.60 (Perfect match) (+3.00)
      • Acousticness: 0.71 vs 0.75 (Perfect match) (+3.00)
      • Tempo: 78 BPM vs 85 BPM (Perfect tempo match) (+2.50)

2. Library Rain - Paper Lanterns
   Score: 98.3/100
   Breakdown:
      • ✓ Genre match: lofi (+2.5)
      • ✓ Mood match: chill (+2.0)
      • Energy: 0.35 vs 0.45 (Close match (distance: 0.10)) (+3.00)
      • Valence: 0.60 vs 0.65 (Perfect match) (+3.00)
      • Danceability: 0.58 vs 0.60 (Perfect match) (+3.00)
      • Acousticness: 0.86 vs 0.75 (Close match (distance: 0.11)) (+2.90)
      • Tempo: 72 BPM vs 85 BPM (Close tempo match (13 BPM diff)) (+2.27)

3. Coffee Shop Stories - Slow Stereo
   Score: 97.9/100
   Breakdown:
      • ✓ Genre match: jazz (+2.5)
      • ✓ Mood match: relaxed (+2.0)
      • Energy: 0.37 vs 0.45 (Perfect match) (+3.00)
      • Valence: 0.71 vs 0.65 (Perfect match) (+3.00)
      • Danceability: 0.54 vs 0.60 (Perfect match) (+3.00)
      • Acousticness: 0.89 vs 0.75 (Close match (distance: 0.14)) (+2.60)
      • Tempo: 90 BPM vs 85 BPM (Perfect tempo match) (+2.50)

4. Focus Flow - LoRoom
   Score: 89.5/100
   Breakdown:
      • ✓ Genre match: lofi (+2.5)
      • Energy: 0.40 vs 0.45 (Perfect match) (+3.00)
      • Valence: 0.59 vs 0.65 (Perfect match) (+3.00)
      • Danceability: 0.60 vs 0.60 (Perfect match) (+3.00)
      • Acousticness: 0.78 vs 0.75 (Perfect match) (+3.00)
      • Tempo: 80 BPM vs 85 BPM (Perfect tempo match) (+2.50)

5. Spacewalk Thoughts - Orbit Bloom
   Score: 82.0/100
   Breakdown:
      • ✓ Genre match: ambient (+2.5)
      • ✓ Mood match: chill (+2.0)
      • Energy: 0.28 vs 0.45 (Close match (distance: 0.17)) (+2.30)
      • Valence: 0.65 vs 0.65 (Perfect match) (+3.00)
      • Danceability: 0.41 vs 0.60 (Close match (distance: 0.19)) (+2.10)
      • Acousticness: 0.92 vs 0.75 (Close match (distance: 0.17)) (+2.30)
      • Tempo: 60 BPM vs 85 BPM (Close tempo match (25 BPM diff)) (+1.38)

================================================================================
```

**Output Interpretation:**
- **Score**: Normalized 0-100 scale based on point-weighting algorithm (max 19.0 points → /19 × 100)
- **Breakdown**: Each feature shows:
  - Actual value vs. user's target
  - Match quality (Perfect/Close/Moderate/Poor)
  - Points awarded for that feature
- **Checkmarks**: ✓ indicates matching preferred genre/mood (bonus points)

---

## Experiments You Tried

### Stress Test: 7 Diverse User Profiles

To evaluate the recommender's behavior, I tested it with 7 distinct user profiles ranging from normal to adversarial:

#### **Stress Test Output: Lofi Devotee (Control Profile)**

![Stress Test Output Screenshot](Output%20Screenshot.png)

**Observation**: Perfect recommendations (100.0/100) when preferences are coherent and aligned with song features. The screenshot shows:
- Lofi Devotee profile with coherent preferences (lofi/ambient genres, chill/focused moods)
- Top recommendations scoring 100.0/100
- Complete scoring breakdown showing genre match, mood match, and feature similarity
- System excels with well-aligned user preferences

---

#### **1. Lofi Devotee (Control Profile)**

- **Preferences**: lofi/ambient, chill/focused mood, low energy (0.40), high acousticness (0.80)
- **Result**: Perfect recommendations (100.0/100) - Algorithm excels with coherent preferences
- **Top song**: "Midnight Coding" by LoRoom - perfect genre/mood match + all numerical features aligned

#### **2. Confused Party Animal (Contradictory)**
- **Preferences**: lofi/ambient genres BUT wants high energy (0.90), intense/happy mood, electronic sound
- **Result**: Algorithm prioritizes numerical features over genre mismatch
  - Top: "Gym Hero" (86.8/100) - pop/intense, not lofi, but matches energy perfectly
  - Shows **algorithmic bias**: Features win over genre when conflicting
- **Insight**: System can be "tricked" by conflicting preferences; features dominate genre labels

#### **3. Maximum Maximalist (Extreme Values)**
- **Preferences**: Extreme targets (energy 0.95, valence 0.95, danceability 0.95, acousticness 0.02, tempo 165 BPM)
- **Result**: No song perfectly matches extreme combo; graceful degradation observed
  - Top: "Gym Hero" (73.9/100) - incomplete match but highest overall
  - Lower scores overall (50-74 range) because no song satisfies all extremes
- **Insight**: Extreme preferences expose **distance metric limitations**; no single perfect result

#### **4. Jazz Snob (Niche Profile)**
- **Preferences**: Jazz only, very specific numerical targets, high acousticness (0.90)
- **Result**: Deep expertise isolation
  - Top: "Coffee Shop Stories" (100.0/100) - only jazz song, perfect match
  - Fallback: Lofi songs score 70-74, showing **cold-start problem** for niche genres
- **Insight**: Creates **filter bubble** - jazz fan gets mostly jazz recommendations with weak alternatives

#### **5. Mood Ring Enthusiast (Genre-Heavy)**
- **Preferences**: Multiple genres (lofi/ambient/jazz), multiple moods, flexible numerics
- **Result**: Excellent diversity with high scores
  - Top 3 all score 95-100/100 (different songs, different artists)
  - Broad preferences → broad recommendations
- **Insight**: Demonstrates **importance of genre/mood weighting** (+2.5, +2.0) = 24% of max points

#### **6. Audio Engineer (Feature-Heavy)**
- **Preferences**: Broad genres/moods, very specific numerical targets (energy 0.75, valence 0.70, etc.)
- **Result**: Precise numerical matching works
  - Top: "Sunrise City" (97.9/100) - excellent feature fit despite being pop (not favorite genre)
  - Shows features can overcome genre mismatch when numerically aligned
- **Insight**: Demonstrates **numerical features compete equally with categorical** when well-defined

#### **7. Median Listener (Neutral/Average)**
- **Preferences**: Common genres (pop/rock), common moods (happy/chill), middle-ground targets (all 0.50-0.65)
- **Result**: Moderate scores across diverse songs
  - Closest matches: Midnight Coding, Sunrise City, Island Vibes (70-73/100)
  - No perfect matches because middle targets are reasonable but not aligned with actual song values
- **Insight**: **Regression to mean** - average preferences get average recommendations; lacks differentiation

### Key Findings from Stress Tests

| Profile | Main Finding | Algorithmic Bias Revealed |
|---------|---|---|
| **Control** | Works as designed | ✅ None - excellent baseline |
| **Contradictory** | Features override genre | ⚠️ Numerical features dominate categorical |
| **Extremes** | Graceful degradation | ⚠️ Hard to satisfy extreme combinations |
| **Niche** | Filter bubble effect | ⚠️ Isolates users in single genre |
| **Genre-Heavy** | Genre weighting effective | ✅ Multiple genres enable discovery |
| **Feature-Heavy** | Features drive recommendations | ⚠️ Genre can be overridden by numerics |
| **Neutral** | Middle-ground results | ⚠️ Tends toward average; lacks differentiation |

### How Real-World Biases Appear

1. **Filter Bubble Risk**: Niche preferences (Profile #4) trap users in single genre despite good audio features elsewhere
2. **Popularity Bias**: Average preferences (Profile #7) recommend only the statistically "safe" songs
3. **Feature Dominance**: Contradictory profiles (Profile #2) show features can override semantic meaning of genre labels
4. **Cold Start**: New artists without genre label can't overcome niche user preferences
5. **No Serendipity**: Adjacent genres (e.g., "synthwave" vs. "lofi") treated as unrelated if not in preferred list

---

## Experiments You Tried

Examples of what you could test:

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

