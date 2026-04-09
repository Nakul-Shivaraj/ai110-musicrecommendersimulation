# Step 3: Data Experiment - Weight Shift Results

## Experiment Design

**Hypothesis**: Doubling energy importance and halving genre importance will improve recommendations by emphasizing feature matching over categorical preferences.

**Changes Applied**:
- Genre weight: 2.5 → 1.25 (50% reduction)
- Energy weight: 3.0 → 6.0 (100% increase)
- New max score: 20.75 (was 19.0)
- All other weights unchanged

---

## Key Finding: Weight Shift Made Accuracy WORSE

### Critical Profile: "Confused Party Animal"
This profile explicitly prefers lofi/ambient genres but has contradictory energy targets (0.90 = party vibes).

**OLD Algorithm Results (Genre 2.5, Energy 3.0)**:
```
1. Gym Hero - Max Pulse
   Score: 86.8/100
   Top recommendation is wrong genre (pop) but has good valence/danceability
```

**NEW Algorithm Results (Genre 1.25, Energy 6.0)**:
```
1. Gym Hero - Max Pulse
   Score: 94.0/100 ← SCORE INCREASED!
   Still wrong genre, but now energy match (+6.0) dominates even more
```

### Why This Happened

The weight shift **made the problem worse**:

1. **Genre penalty weakened**: Halving genre from 2.5 to 1.25 means "wrong genre" songs are penalized less
2. **Energy dominance increased**: Doubling energy from 3.0 to 6.0 means feature matching overpowers categorical preferences
3. **Perfect energy match override**: "Gym Hero" has energy 0.93 vs target 0.90 = "Perfect match" (+6.0 points)
4. **Result**: Even though the song is pop (not lofi), it now scores 94.0/100 instead of 86.8/100

---

## Detailed Comparison Table

### Profile 1: Lofi Devotee (Control)
| Rank | Song | OLD Score | NEW Score | Change |
|------|------|-----------|-----------|--------|
| 1 | Midnight Coding | 100.0 | 100.0 | ➡️ Same |
| 2 | Library Rain | 100.0 | 100.0 | ➡️ Same |
| 3 | Focus Flow | 100.0 | 100.0 | ➡️ Same |
| 4 | Spacewalk Thoughts | 91.3 vs 91.0 | 91.0 | ↓ Slightly lower |

**Observation**: Minimal impact. Genre matches still get these right.

### Profile 2: Confused Party Animal ⚠️ PROBLEM PROFILE
| Rank | Song | OLD Score | NEW Score | Change | Notes |
|------|------|-----------|-----------|--------|-------|
| 1 | Gym Hero | 86.8 | **94.0** | ↑ +7.2 | **WORSE! More confident in WRONG genre** |
| 2 | Sunrise City | ~82 | 88.2 | ↑ Higher | High energy songs score even better now |

**Observation**: The doubled energy weight makes pop/electronic songs score HIGHER, contradicting the user's lofi preference. The profile gets increasingly confidentin the wrong recommendations.

### Profile 4: Jazz Snob (Niche)
| Rank | Song | OLD Score | NEW Score | Change |
|------|------|-----------|-----------|--------|
| 1 | Coffee Shop Stories | 100.0 | 100.0 | ➡️ Same |

**Observation**: Perfect matches remain perfect. Genre match still carries weight.

### Profile 5: Mood Ring Enthusiast (Genre-Heavy)
| Rank | Song | OLD Score | NEW Score | Change |
|------|------|-----------|-----------|--------|
| 1 | Midnight Coding | 100.0 | 100.0 | ➡️ Same |
| 2 | Focus Flow | 100.0 | 100.0 | ➡️ Same |

**Observation**: Multiple genre preferences protect against energy-only matching.

---

## Mathematical Analysis

### Why Doubling Energy Amplifies the Problem

**Gym Hero scoring (Confused Party Animal profile)**:

**OLD (max 19.0)**:
- Genre match: 0 (not lofi/ambient)
- Mood match: +2.0 (intense ✓)
- Energy: +~3.0 (0.93 vs 0.90 = close)
- Valence: +3.0 (0.77 vs 0.85 = close)
- Danceability: +3.0 (0.88 vs 0.85 ✓)
- Acousticness: +3.0 (0.05 vs 0.05 ✓)
- Tempo: +2.5 (132 vs 140 ✓)
- **Raw: 16.5/19.0 = 86.8/100**

**NEW (max 20.75)**:
- Genre match: 0 (not lofi/ambient)
- Mood match: +2.0 (intense ✓)
- **Energy: +6.0 (0.93 vs 0.90 = "Perfect match")**  ← doubled impact
- Valence: +3.0 (0.77 vs 0.85)
- Danceability: +3.0 (0.88 vs 0.85 ✓)
- Acousticness: +3.0 (0.05 vs 0.05 ✓)
- Tempo: +2.5 (132 vs 140 ✓)
- **Raw: 19.5/20.75 = 94.0/100**

**Conclusion**: By doubling energy and halving genre, we made energetic pop songs score 7.2 points higher for a user who explicitly wants lofi.

---

## Broader Impact Across All 7 Profiles

**Profiles that improved recommendations**: 
- None significantly. All-correct recommendations stayed correct.

**Profiles where quality degraded**:
- Profile 2 (Confused Party Animal): Genre preference increasingly ignored

**Profiles where behavior changed but quality unclear**:
- Profile 6 (Audio Engineer): Energy-heavy profile now scores high-energy songs even higher. Mostly positive since this profile doesn't have conflicting preferences.
- Profile 7 (Median Listener): Neutral preferences, so energy preference now dominates.

---

## Conclusion

**Different, but NOT MORE ACCURATE. Actually Less Accurate.**

### Key Insight
The weight shift revealed a fundamental trade-off:
- **Lowering genre weight**: Makes wrong-genre recommendations score higher when their features happen to match
- **Doubling energy weight**: Amplifies feature dominance, defeating the purpose of categorical preferences

### What This Shows About Recommender Design
The system needs **higher** genre weighting, not lower. The original analysis was correct—Profile 2 needs genre to be weighted MORE, not energy to be weighted LESS.

### Recommendation For Next Iteration
Try the **inverse adjustment**: 
- Genre: 2.5 → 4.0 (60% increase)
- Energy: 3.0 → 2.0 (33% reduction)
- This would make genre mismatches costlier and feature matching less dominant

---

## Experiment Validation

✅ **Math Integrity**: All scores normalized correctly to (raw_points / 20.75) * 100  
✅ **System Stability**: No crashes, all 7 profiles ran successfully  
✅ **Expected Behavior**: Energy-heavy songs scored higher across all profiles  
✅ **Revealed Design Flaw**: Halving genre unmasked the feature-dominance problem even more clearly

