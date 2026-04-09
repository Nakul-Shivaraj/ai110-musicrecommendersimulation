# 🎧 Model Card: Music Recommender Simulation

## Model Name
**VibeFinder 1.0**

## Goal / Task
VibeFinder predicts which songs from a music catalog will best match a user's musical preferences, suggesting personalized song recommendations based on genre, mood, and audio features like energy and danceability.

## Data Used
The system uses a catalog of 18 songs with features including genre, mood, energy level, tempo, valence (positivity), danceability, and acousticness. Genres include pop, lofi, rock, jazz, electronic, and more. The dataset has some limitations - lofi is overrepresented with 3 songs, while most genres have only 1 song, and extreme values in features like very low energy or high acousticness are missing.

## Algorithm Summary
VibeFinder scores songs using a point system where genre matches give 1.25 points, mood matches give 2 points, and audio features like energy (6 points), valence, danceability, and acousticness (3 points each) are scored based on how close they are to user preferences. Tempo gets 2.5 points based on BPM difference. Higher scores mean better matches, with a maximum of 20.75 points.

## Observed Behavior / Biases
The system shows a strong bias toward numerical audio features over categorical preferences like genre. Users with conflicting preferences (wanting lofi but high energy) often get recommendations that match the energy level but ignore the genre, creating filter bubbles. Songs with extreme feature values outside the dataset's range get poor scores for those users.

## Evaluation Process
I tested VibeFinder with 7 diverse user profiles representing different musical tastes, from chill lofi fans to high-energy party seekers. I ran a weight shift experiment doubling energy importance and halving genre weight, which made recommendations worse for users with conflicting preferences. I compared recommendation differences between profile pairs to understand how preferences affect results.

## Intended Use and Non-Intended Use
VibeFinder is intended for classroom exploration of how recommender systems work, helping students understand the trade-offs between different scoring approaches. It should not be used for real music recommendations to actual users, as it's a simplified simulation with limited data and known biases that could lead to poor suggestions.

## Ideas for Improvement
1. Increase genre weight to better balance categorical and numerical matching
2. Add more songs to the catalog, especially for underrepresented genres and extreme feature values
3. Implement hybrid scoring that considers both individual preferences and overall user patterns

## Challenge 3 Reflection: Diversity and Fairness Logic

Before adding the diversity penalty, the recommender had a clear filter-bubble problem: a user who liked lofi would get 3 of their top 5 results from the same genre, and the same artist (LoRoom) could appear twice back-to-back. The results were accurate in the sense that those songs genuinely scored highest, but they made the playlist feel repetitive and narrow.

To fix this, I implemented a greedy diversity-aware selection loop with two compounding penalties:

- **Artist penalty (35%)**: each time an artist already appears in the results, the next song by that artist has its score multiplied by 0.65. A second repeat is multiplied again — penalties compound, so repeat offenders are pushed down progressively harder.
- **Genre penalty (20%)**: same logic for genre — a second lofi song in the results takes a 20% score hit, a third would take another 20% on top of that.

The selection loop re-evaluates every remaining candidate after each pick, so the penalties reflect the actual current state of the result list rather than a fixed pre-computed deduction.

The smoke test showed the effect clearly: without diversity, LoRoom appeared twice and lofi dominated 3 of 5 slots. With diversity, each slot went to a different artist, and two different genres replaced the repeated ones — while the top-ranked song (the genuinely best match) was unchanged.

What this taught me about fairness in recommender systems: the "most accurate" result and the "best user experience" result are not always the same thing. A recommender that always picks the highest raw score can confidently lock a user into a bubble — feeding them the same sound over and over because it keeps scoring well. Diversity logic is a deliberate override of pure accuracy in favor of variety, and that trade-off is a design choice, not a math mistake. Real platforms like Spotify make this same trade-off intentionally, which is why Discover Weekly doesn't just give you 30 songs from your single most-played artist.

## Personal Reflection
My biggest learning moment was realizing how recommender systems can create hidden biases through seemingly neutral scoring rules - the weight shift experiment showed that doubling energy importance made the system confidently recommend wrong-genre songs, revealing that "objective" algorithms aren't really neutral. AI tools like GitHub Copilot helped me quickly implement complex scoring functions and generate test profiles, but I had to double-check the math calculations and verify that the scoring logic actually worked as intended, especially when the results surprised me. What surprised me most was how a simple point-weighting algorithm could still produce recommendations that "felt" right for many users, even though it was just basic distance calculations - it showed me why real music apps can seem smart with relatively straightforward math. If I extended this project, I'd try implementing collaborative filtering by adding user-song interaction data, and explore how to make the system learn from user feedback to automatically adjust weights over time.
