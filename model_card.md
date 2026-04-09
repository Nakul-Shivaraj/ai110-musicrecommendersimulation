# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The system exhibits a significant bias toward numerical audio features over categorical preferences like genre, as demonstrated by the weight shift experiment where doubling energy importance and halving genre weight caused users preferring lofi music to receive pop recommendations with higher confidence scores. This feature dominance creates filter bubbles for users with conflicting preferences, where songs matching energy levels are prioritized even when they contradict stated genre preferences. Additionally, users seeking extreme values in features like very low energy (below 0.28) or very high acousticness (above 0.94) may receive suboptimal recommendations due to the dataset's limited range in these attributes. The binary nature of genre and mood matching compared to the continuous scoring of audio features further amplifies this imbalance, potentially marginalizing users whose musical taste relies more heavily on categorical distinctions than numerical similarities.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested the recommender with seven diverse user profiles to evaluate its behavior across different musical preferences: Lofi Devotee (chill, focused lofi/ambient), Confused Party Animal (lofi genres but high energy/intense mood), Maximum Maximalist (extreme values across all features), Jazz Snob (niche jazz preference), Mood Ring Enthusiast (multiple genres and moods), Audio Engineer (broad genres with specific feature targets), and Median Listener (average preferences). I looked for whether recommendations matched musical intuition, whether the system handled conflicting preferences appropriately, and how changes to the scoring weights affected outcomes. What surprised me was that the weight shift experiment (doubling energy importance while halving genre weight) actually made recommendations worse for users with conflicting preferences, revealing that numerical features dominate categorical preferences more than expected. I ran a simple experiment comparing original vs. modified scoring logic and documented the results in EXPERIMENT_RESULTS.md.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
