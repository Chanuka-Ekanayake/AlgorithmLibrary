# User Guide: The Movie Recommendation Engine (KNN)

This project demonstrates the **K-Nearest Neighbors** algorithm by building a movie genre recommendation engine that predicts a user's preferred genre from their rating profile.

## What You'll See

The simulation runs four demos in sequence:

1. **Genre Recommendation:** Train on 24 user profiles, then recommend movies for 5 new users (Alice, Bob, Carol, Dave, Eve) based on their viewing patterns.
2. **Distance Metric Comparison:** See how Euclidean, Manhattan, and Minkowski distance produce different neighbor selections and predictions for the same ambiguous user.
3. **K-Value Sensitivity:** Watch how accuracy changes as K varies from 1 to 11 — demonstrating the bias-variance trade-off.
4. **Uniform vs Weighted Voting:** For a user right on the boundary between Action and Horror, see how distance-weighted voting makes a smarter decision than simple majority voting.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```

## Key Scenario to Watch

In Demo 4, the "boundary user" rates Action=7 and Horror=8 — they're a fan of both genres. With **uniform voting**, the 5 nearest neighbors each get 1 vote, and the genre with more neighbors wins. With **distance-weighted voting**, the closest neighbor (who might be a different genre) gets disproportionately more influence, often producing a more accurate prediction.

## No Dependencies

This project uses only Python standard library modules. No `pip install` required.
