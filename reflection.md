# Reflection: Profile Comparisons

## Lofi Devotee vs Confused Party Animal
The Lofi Devotee gets perfect 100/100 scores for chill lofi songs like "Midnight Coding" because everything matches their relaxed preferences. But the Confused Party Animal, who wants lofi genres but high energy and intense/happy moods, gets "Gym Hero" (pop music) as their top recommendation. This makes sense because "Gym Hero" has the high energy they want, even though it's not lofi - the system prioritizes matching the energy level over the genre preference when they conflict.

## Maximum Maximalist vs Jazz Snob
The Maximum Maximalist, who wants extreme values in everything (energy 0.95, valence 0.95, etc.), gets "Gym Hero" as a top recommendation because it has high energy and danceability, though it scores lower due to valence mismatch. The Jazz Snob, with very specific jazz preferences and moderate features, gets perfect 100/100 for "Coffee Shop Stories" - the only jazz song. This shows how niche preferences work well when the dataset has matching songs, but extreme preferences struggle with the limited range in the catalog.

## Mood Ring Enthusiast vs Audio Engineer
The Mood Ring Enthusiast likes multiple genres (lofi, ambient, jazz) and flexible moods, so they get diverse top recommendations including "Midnight Coding" and "Coffee Shop Stories." The Audio Engineer prefers broad genres but very specific feature targets, getting "Sunrise City" as top pick because it matches their energy and danceability perfectly. This comparison shows how genre-heavy profiles get more variety in recommendations, while feature-heavy profiles get more precise matches to their numerical targets.

## Median Listener vs Lofi Devotee
The Median Listener has average preferences across pop/rock genres and happy/chill moods, getting "Midnight Coding" as a top recommendation because it matches their moderate energy and chill mood, even though it's lofi not pop/rock. The Lofi Devotee gets the same song at 100/100 because it perfectly matches their lofi preference. This demonstrates how the system can recommend the same song to different users for different reasons - mood/energy match vs. genre match.

## Why "Gym Hero" Shows Up for Happy Pop Profiles
"Gym Hero" keeps appearing for users who want happy pop music because it's a pop song with intense energy and high danceability, which matches profiles looking for upbeat, energetic pop tracks. Even though it's labeled as "intense" rather than "happy," its high valence (0.77) and danceability (0.88) make it a good fit for users wanting positive, lively music. The system sees the numerical similarities in energy and rhythm over the exact mood label match.