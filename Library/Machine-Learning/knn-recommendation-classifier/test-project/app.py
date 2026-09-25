import sys
import io
import time
import random
from pathlib import Path

# Fix Windows console encoding for Unicode output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent directory to path for core logic access
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

try:
    from core.knn import KNNClassifier, accuracy_score, train_test_split
except ImportError:
    print("Error: Ensure 'core/knn.py' and 'core/__init__.py' exist.")
    sys.exit(1)


def print_header(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def print_section(title):
    print(f"\n--- {title} ---")


# ============================================================
# DATASET: Movie Preference Profiles
# ============================================================
# Each user is described by 5 features (rated 0-10):
#   [Action, Comedy, Drama, Sci-Fi, Horror]
# Label = preferred genre to recommend next

MOVIE_DATA = {
    "features": [
        # --- Action Fans ---
        [9, 2, 3, 7, 4],   # User 0:  Loves action + sci-fi
        [8, 3, 2, 6, 5],   # User 1:  Strong action preference
        [10, 1, 1, 8, 3],  # User 2:  Pure action/sci-fi fan
        [7, 4, 3, 9, 2],   # User 3:  Action + sci-fi leaning
        [8, 2, 4, 7, 6],   # User 4:  Action with some horror
        [9, 3, 2, 8, 3],   # User 5:  Classic action fan
        # --- Comedy Fans ---
        [3, 9, 5, 2, 1],   # User 6:  Comedy lover
        [2, 8, 6, 3, 2],   # User 7:  Comedy + drama mix
        [4, 10, 4, 1, 1],  # User 8:  Pure comedy fan
        [3, 7, 7, 2, 3],   # User 9:  Comedy + drama
        [2, 9, 5, 3, 1],   # User 10: Strong comedy preference
        [5, 8, 4, 2, 2],   # User 11: Comedy with some action
        # --- Drama Fans ---
        [2, 4, 9, 3, 2],   # User 12: Drama lover
        [3, 5, 8, 2, 3],   # User 13: Drama + comedy mix
        [1, 3, 10, 1, 4],  # User 14: Pure drama fan
        [4, 3, 9, 2, 1],   # User 15: Drama with some action
        [2, 6, 8, 3, 2],   # User 16: Drama + comedy
        [3, 4, 9, 1, 3],   # User 17: Strong drama preference
        # --- Horror Fans ---
        [5, 1, 3, 4, 9],   # User 18: Horror lover
        [4, 2, 2, 3, 8],   # User 19: Horror + action mix
        [3, 1, 4, 5, 10],  # User 20: Pure horror fan
        [6, 2, 3, 4, 9],   # User 21: Horror + action
        [2, 3, 5, 3, 8],   # User 22: Horror + drama
        [4, 1, 2, 6, 9],   # User 23: Horror + sci-fi
    ],
    "labels": [
        "Action", "Action", "Action", "Action", "Action", "Action",
        "Comedy", "Comedy", "Comedy", "Comedy", "Comedy", "Comedy",
        "Drama",  "Drama",  "Drama",  "Drama",  "Drama",  "Drama",
        "Horror", "Horror", "Horror", "Horror", "Horror", "Horror",
    ],
    "feature_names": ["Action", "Comedy", "Drama", "Sci-Fi", "Horror"],
}

# New users to recommend movies for
NEW_USERS = [
    {"name": "Alice",   "profile": [9, 1, 2, 8, 3],  "description": "Action + Sci-Fi lover"},
    {"name": "Bob",     "profile": [2, 9, 6, 1, 2],  "description": "Comedy enthusiast"},
    {"name": "Carol",   "profile": [3, 5, 8, 2, 4],  "description": "Drama + Comedy mix"},
    {"name": "Dave",    "profile": [5, 2, 3, 5, 9],  "description": "Horror fanatic"},
    {"name": "Eve",     "profile": [6, 6, 6, 5, 5],  "description": "Balanced viewer (edge case)"},
]

GENRE_MOVIES = {
    "Action": ["Mad Max: Fury Road", "John Wick 4", "Top Gun: Maverick"],
    "Comedy": ["The Grand Budapest Hotel", "Superbad", "Barbie"],
    "Drama":  ["The Shawshank Redemption", "Oppenheimer", "Parasite"],
    "Horror": ["Hereditary", "Get Out", "The Conjuring"],
}


def demo_basic_classification():
    """Core KNN classification demo with movie dataset."""
    print_header("DEMO 1: MOVIE GENRE RECOMMENDATION ENGINE")
    print("Scenario: Predict a user's preferred genre from their rating profile.")
    print(f"Dataset:  {len(MOVIE_DATA['labels'])} users, {len(MOVIE_DATA['feature_names'])} features")
    print(f"Features: {MOVIE_DATA['feature_names']}")
    print(f"Classes:  {sorted(set(MOVIE_DATA['labels']))}\n")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        MOVIE_DATA["features"], MOVIE_DATA["labels"],
        test_ratio=0.25, seed=42
    )

    print(f"[SPLIT] Training: {len(X_train)} users | Testing: {len(X_test)} users")

    # Train classifier
    clf = KNNClassifier(k=3, metric='euclidean', weights='distance', normalize=True)
    clf.fit(X_train, y_train)
    print(f"[MODEL] {clf}")

    # Evaluate on test set
    time.sleep(0.3)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print_section("TEST SET EVALUATION")
    print(f"  Predictions: {y_pred}")
    print(f"  Actual:      {list(y_test)}")
    print(f"  Accuracy:    {acc:.1%}")

    # Recommend for new users
    time.sleep(0.3)
    print_section("RECOMMENDATIONS FOR NEW USERS")

    # Retrain on full dataset for best recommendations
    clf_full = KNNClassifier(k=3, metric='euclidean', weights='distance', normalize=True)
    clf_full.fit(MOVIE_DATA["features"], MOVIE_DATA["labels"])

    for user in NEW_USERS:
        prediction = clf_full.predict([user["profile"]])[0]
        probas = clf_full.predict_proba([user["profile"]])[0]
        movies = GENRE_MOVIES.get(prediction, ["Unknown"])
        top_movie = random.choice(movies)

        confidence = probas.get(prediction, 0.0)
        proba_str = ", ".join(f"{cls}: {p:.0%}" for cls, p in sorted(probas.items()))

        print(f"\n  [{user['name'].upper()}] {user['description']}")
        print(f"    Profile:      {dict(zip(MOVIE_DATA['feature_names'], user['profile']))}")
        print(f"    Predicted:    {prediction} ({confidence:.0%} confidence)")
        print(f"    Probabilities: {proba_str}")
        print(f"    Recommended:  \"{top_movie}\"")


def demo_distance_metrics():
    """Compare how different distance metrics affect predictions."""
    print_header("DEMO 2: DISTANCE METRIC COMPARISON")
    print("Same dataset, same K=3, different distance metrics.\n")

    clf_full_data = MOVIE_DATA["features"]
    clf_full_labels = MOVIE_DATA["labels"]

    test_user = [6, 6, 6, 5, 5]  # Eve - the balanced viewer
    print(f"  Test User (balanced): {dict(zip(MOVIE_DATA['feature_names'], test_user))}\n")

    metrics = [
        ("euclidean", "Euclidean (L2)", {}),
        ("manhattan", "Manhattan (L1)", {}),
        ("minkowski", "Minkowski (L3)", {"p": 3}),
    ]

    for metric_name, display_name, extra_kwargs in metrics:
        clf = KNNClassifier(k=3, metric=metric_name, weights='distance',
                            normalize=True, **extra_kwargs)
        clf.fit(clf_full_data, clf_full_labels)
        pred = clf.predict([test_user])[0]
        probas = clf.predict_proba([test_user])[0]

        neighbors = clf.get_neighbors(test_user, k=3)
        neighbor_info = [(f"d={d:.3f}, {clf_full_labels[idx]}") for d, idx in neighbors]

        print(f"  [{display_name}]")
        print(f"    Prediction: {pred}")
        print(f"    Neighbors:  {neighbor_info}")
        proba_str = ", ".join(f"{cls}: {p:.0%}" for cls, p in sorted(probas.items()))
        print(f"    Probas:     {proba_str}")
        print()


def demo_k_sensitivity():
    """Show how different K values affect predictions."""
    print_header("DEMO 3: K-VALUE SENSITIVITY ANALYSIS")
    print("How does changing K affect accuracy and predictions?\n")

    X_train, X_test, y_train, y_test = train_test_split(
        MOVIE_DATA["features"], MOVIE_DATA["labels"],
        test_ratio=0.25, seed=42
    )

    k_values = [1, 3, 5, 7, 11]
    print(f"  {'K':>3}  {'Accuracy':>10}  {'Predictions'}")
    print(f"  {'---':>3}  {'--------':>10}  {'-----------'}")

    for k in k_values:
        clf = KNNClassifier(k=k, metric='euclidean', weights='distance', normalize=True)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"  {k:>3}  {acc:>9.1%}  {y_pred}")

    print(f"\n  [TIP] For this dataset (N={len(MOVIE_DATA['labels'])}), ")
    print(f"        sqrt(N) = {int(len(MOVIE_DATA['labels'])**0.5)}, so K=3-5 is the sweet spot.")


def demo_uniform_vs_weighted():
    """Compare uniform vs distance-weighted voting."""
    print_header("DEMO 4: UNIFORM vs DISTANCE-WEIGHTED VOTING")
    print("When a user sits between two genres, weighting matters.\n")

    clf_full_data = MOVIE_DATA["features"]
    clf_full_labels = MOVIE_DATA["labels"]

    # A user right on the boundary between Action and Horror
    boundary_user = [7, 1, 2, 5, 8]
    print(f"  Boundary User: {dict(zip(MOVIE_DATA['feature_names'], boundary_user))}")
    print(f"  (High Action AND high Horror -- who wins?)\n")

    for weight_type in ["uniform", "distance"]:
        clf = KNNClassifier(k=5, metric='euclidean', weights=weight_type, normalize=True)
        clf.fit(clf_full_data, clf_full_labels)
        pred = clf.predict([boundary_user])[0]
        probas = clf.predict_proba([boundary_user])[0]

        neighbors = clf.get_neighbors(boundary_user, k=5)
        print(f"  [{weight_type.upper()} VOTING]")
        print(f"    K=5 Neighbors:")
        for dist, idx in neighbors:
            label = clf_full_labels[idx]
            profile = clf_full_data[idx]
            if weight_type == "distance":
                weight = 1.0 / (dist + 1e-10)
                print(f"      d={dist:.3f}  weight={weight:.2f}  -> {label}  {profile}")
            else:
                print(f"      d={dist:.3f}  vote=1       -> {label}  {profile}")

        proba_str = ", ".join(f"{cls}: {p:.0%}" for cls, p in sorted(probas.items()))
        print(f"    Prediction: {pred}")
        print(f"    Probas:     {proba_str}")
        print()


def run_full_demo():
    print("=" * 65)
    print("  SYSTEM: THE MOVIE RECOMMENDATION ENGINE")
    print("  ALGORITHM: K-NEAREST NEIGHBORS (KNN) CLASSIFIER")
    print("=" * 65)

    demo_basic_classification()
    demo_distance_metrics()
    demo_k_sensitivity()
    demo_uniform_vs_weighted()

    print("\n" + "=" * 65)
    print("  FINAL REPORT")
    print("=" * 65)
    print("  Algorithm:           K-Nearest Neighbors (KNN)")
    print("  Dataset:             24 users, 5 genre-rating features")
    print("  Classes:             Action, Comedy, Drama, Horror")
    print("  Distance Metrics:    Euclidean, Manhattan, Minkowski")
    print("  Voting Strategies:   Uniform, Distance-Weighted")
    print("  Training Time:       O(1) -- instant (lazy learning)")
    print("  External Libraries:  NONE (pure Python)")
    print("=" * 65)


if __name__ == "__main__":
    run_full_demo()
