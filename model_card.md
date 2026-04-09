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

## Personal Reflection
My biggest learning moment was realizing how recommender systems can create hidden biases through seemingly neutral scoring rules - the weight shift experiment showed that doubling energy importance made the system confidently recommend wrong-genre songs, revealing that "objective" algorithms aren't really neutral. AI tools like GitHub Copilot helped me quickly implement complex scoring functions and generate test profiles, but I had to double-check the math calculations and verify that the scoring logic actually worked as intended, especially when the results surprised me. What surprised me most was how a simple point-weighting algorithm could still produce recommendations that "felt" right for many users, even though it was just basic distance calculations - it showed me why real music apps can seem smart with relatively straightforward math. If I extended this project, I'd try implementing collaborative filtering by adding user-song interaction data, and explore how to make the system learn from user feedback to automatically adjust weights over time.
