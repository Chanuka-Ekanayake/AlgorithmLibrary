"""
K-Nearest Neighbors (KNN) Classifier

This module implements the KNN algorithm for classification using
instance-based lazy learning. Predictions are made by finding the K
closest training samples to a query point and voting on the class.

Algorithm:
- Store entire training dataset (no model fitting)
- For each query, compute distance to all training points
- Select K nearest neighbors
- Vote on class (uniform or distance-weighted)

Time Complexity: O(n * d) per prediction (n=samples, d=features)
Space Complexity: O(n * d) for storing training data

Author: Algorithm Library
"""

import math
import random
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter


def euclidean_distance(a: List[float], b: List[float]) -> float:
    """
    Compute Euclidean (L2) distance between two points.

    Formula: sqrt(sum((a_i - b_i)^2))

    This is the most common distance metric — it measures the
    straight-line distance between two points in feature space.

    Args:
        a: First feature vector.
        b: Second feature vector.

    Returns:
        Euclidean distance (always >= 0).
    """
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def manhattan_distance(a: List[float], b: List[float]) -> float:
    """
    Compute Manhattan (L1) distance between two points.

    Formula: sum(|a_i - b_i|)

    Also called "city block" distance — the sum of absolute
    differences along each dimension. More robust to outliers
    than Euclidean distance.

    Args:
        a: First feature vector.
        b: Second feature vector.

    Returns:
        Manhattan distance (always >= 0).
    """
    return sum(abs(ai - bi) for ai, bi in zip(a, b))


def minkowski_distance(a: List[float], b: List[float], p: int = 2) -> float:
    """
    Compute Minkowski (Lp) distance between two points.

    Formula: (sum(|a_i - b_i|^p))^(1/p)

    Generalization of Euclidean (p=2) and Manhattan (p=1).

    Args:
        a: First feature vector.
        b: Second feature vector.
        p: Power parameter (must be >= 1).

    Returns:
        Minkowski distance (always >= 0).
    """
    return sum(abs(ai - bi) ** p for ai, bi in zip(a, b)) ** (1 / p)


def min_max_normalize(X: List[List[float]]) -> Tuple[List[List[float]], List[float], List[float]]:
    """
    Apply Min-Max normalization to scale all features to [0, 1].

    This prevents features with large ranges (e.g., salary: 0-100000)
    from dominating features with small ranges (e.g., age: 0-100)
    in the distance calculation.

    Args:
        X: Feature matrix (n_samples x n_features).

    Returns:
        (X_normalized, mins, maxs) — normalized data and the
        min/max values needed to normalize future query points.
    """
    if not X:
        return X, [], []

    n_features = len(X[0])
    mins = [min(sample[f] for sample in X) for f in range(n_features)]
    maxs = [max(sample[f] for sample in X) for f in range(n_features)]

    X_norm = []
    for sample in X:
        row = []
        for f in range(n_features):
            range_f = maxs[f] - mins[f]
            if range_f == 0:
                row.append(0.0)
            else:
                row.append((sample[f] - mins[f]) / range_f)
        X_norm.append(row)

    return X_norm, mins, maxs


def train_test_split(X: List[List[float]], y: List[Any],
                     test_ratio: float = 0.2,
                     seed: Optional[int] = None) -> Tuple:
    """
    Split dataset into training and testing subsets.

    Args:
        X: Feature matrix.
        y: Labels.
        test_ratio: Fraction of data to use for testing (0 to 1).
        seed: Random seed for reproducibility.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    if seed is not None:
        random.seed(seed)

    indices = list(range(len(X)))
    random.shuffle(indices)

    split_point = int(len(X) * (1 - test_ratio))
    train_idx = indices[:split_point]
    test_idx = indices[split_point:]

    X_train = [X[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]

    return X_train, X_test, y_train, y_test


def accuracy_score(y_true: List[Any], y_pred: List[Any]) -> float:
    """
    Calculate classification accuracy.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.

    Returns:
        Accuracy as a float in [0, 1].
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch between y_true and y_pred.")
    if len(y_true) == 0:
        raise ValueError("y_true and y_pred must be non-empty.")

    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true)


class KNNClassifier:
    """
    K-Nearest Neighbors Classifier.

    A non-parametric, instance-based classifier that predicts by
    finding the K closest training examples and voting on the class.

    Supports multiple distance metrics and weighted voting.
    """

    def __init__(self, k: int = 5, metric: str = 'euclidean',
                 weights: str = 'uniform', p: int = 2,
                 normalize: bool = False):
        """
        Initialize KNN Classifier.

        Args:
            k: Number of neighbors to consider (must be >= 1).
            metric: Distance metric — 'euclidean', 'manhattan', or 'minkowski'.
            weights: Voting strategy — 'uniform' (equal votes) or
                     'distance' (closer neighbors have more influence).
            p: Power parameter for Minkowski distance (p=1 is Manhattan, p=2 is Euclidean).
            normalize: Whether to apply Min-Max normalization to features.
        """
        if k < 1:
            raise ValueError("k must be >= 1.")
        if metric not in ('euclidean', 'manhattan', 'minkowski'):
            raise ValueError(f"Unknown metric: '{metric}'. Use 'euclidean', 'manhattan', or 'minkowski'.")
        if weights not in ('uniform', 'distance'):
            raise ValueError(f"Unknown weights: '{weights}'. Use 'uniform' or 'distance'.")

        self.k = k
        self.metric = metric
        self.weights = weights
        self.p = p
        self.normalize = normalize

        # Populated by fit()
        self.X_train: List[List[float]] = []
        self.y_train: List[Any] = []
        self.classes: List[Any] = []
        self._mins: List[float] = []
        self._maxs: List[float] = []
        self._fitted = False

    def _compute_distance(self, a: List[float], b: List[float]) -> float:
        """Compute distance between two points using the configured metric."""
        if self.metric == 'euclidean':
            return euclidean_distance(a, b)
        elif self.metric == 'manhattan':
            return manhattan_distance(a, b)
        elif self.metric == 'minkowski':
            return minkowski_distance(a, b, self.p)
        else:
            raise ValueError(f"Unknown metric: {self.metric}")

    def _normalize_sample(self, sample: List[float]) -> List[float]:
        """Normalize a single sample using stored min/max from training data."""
        normalized = []
        for f in range(len(sample)):
            range_f = self._maxs[f] - self._mins[f]
            if range_f == 0:
                normalized.append(0.0)
            else:
                normalized.append((sample[f] - self._mins[f]) / range_f)
        return normalized

    def fit(self, X: List[List[float]], y: List[Any]) -> 'KNNClassifier':
        """
        Store the training dataset. KNN has no actual training phase —
        this simply memorizes the data for use during prediction.

        Args:
            X: Training features (n_samples x n_features).
            y: Training labels (n_samples).

        Returns:
            self
        """
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples.")
        if len(X) == 0:
            raise ValueError("Training data must not be empty.")

        if self.normalize:
            self.X_train, self._mins, self._maxs = min_max_normalize(X)
        else:
            self.X_train = [list(row) for row in X]
            self._mins = []
            self._maxs = []

        self.y_train = list(y)
        self.classes = sorted(set(y))
        self._fitted = True

        return self

    def get_neighbors(self, sample: List[float],
                      k: Optional[int] = None) -> List[Tuple[float, int]]:
        """
        Find the K nearest neighbors to a query sample.

        Args:
            sample: Feature vector to find neighbors for.
            k: Number of neighbors (defaults to self.k).

        Returns:
            List of (distance, training_index) tuples, sorted by distance.
        """
        if not self._fitted:
            raise ValueError("KNNClassifier is not fitted yet. Call 'fit' first.")

        k = k or self.k

        if self.normalize:
            sample = self._normalize_sample(sample)

        # Compute distance to every training sample
        distances = []
        for i, train_sample in enumerate(self.X_train):
            dist = self._compute_distance(sample, train_sample)
            distances.append((dist, i))

        # Sort by distance and return K nearest
        distances.sort(key=lambda x: x[0])
        return distances[:k]

    def predict(self, X: List[List[float]]) -> List[Any]:
        """
        Predict class labels for query samples.

        For each query point:
          1. Find K nearest neighbors in training data.
          2. Collect their class labels.
          3. Vote (uniform or distance-weighted) to determine prediction.

        Args:
            X: Feature matrix (n_samples x n_features).

        Returns:
            List of predicted class labels.
        """
        if not self._fitted:
            raise ValueError("KNNClassifier is not fitted yet. Call 'fit' first.")

        predictions = []
        for sample in X:
            neighbors = self.get_neighbors(sample)

            if self.weights == 'uniform':
                # Simple majority vote — each neighbor gets 1 vote
                neighbor_labels = [self.y_train[idx] for _, idx in neighbors]
                vote_counts = Counter(neighbor_labels)
                predictions.append(vote_counts.most_common(1)[0][0])

            elif self.weights == 'distance':
                # Distance-weighted vote — closer neighbors have more influence
                vote_weights: Dict[Any, float] = {}
                for dist, idx in neighbors:
                    label = self.y_train[idx]
                    # Use inverse distance as weight (add epsilon to avoid division by zero)
                    weight = 1.0 / (dist + 1e-10)
                    vote_weights[label] = vote_weights.get(label, 0.0) + weight

                predictions.append(max(vote_weights, key=vote_weights.get))

        return predictions

    def predict_proba(self, X: List[List[float]]) -> List[Dict[Any, float]]:
        """
        Predict class probabilities for query samples.

        Probabilities are computed as the proportion of neighbor votes
        (uniform) or weighted votes (distance) for each class.

        Args:
            X: Feature matrix (n_samples x n_features).

        Returns:
            List of dictionaries mapping class -> probability.
        """
        if not self._fitted:
            raise ValueError("KNNClassifier is not fitted yet. Call 'fit' first.")

        probabilities = []
        for sample in X:
            neighbors = self.get_neighbors(sample)

            if self.weights == 'uniform':
                neighbor_labels = [self.y_train[idx] for _, idx in neighbors]
                counts = Counter(neighbor_labels)
                total = sum(counts.values())
                proba = {cls: counts.get(cls, 0) / total for cls in self.classes}

            elif self.weights == 'distance':
                vote_weights: Dict[Any, float] = {}
                for dist, idx in neighbors:
                    label = self.y_train[idx]
                    weight = 1.0 / (dist + 1e-10)
                    vote_weights[label] = vote_weights.get(label, 0.0) + weight

                total = sum(vote_weights.values())
                proba = {cls: vote_weights.get(cls, 0.0) / total for cls in self.classes}

            probabilities.append(proba)

        return probabilities

    def __repr__(self) -> str:
        status = "fitted" if self._fitted else "not fitted"
        n = len(self.X_train) if self._fitted else 0
        return (f"<KNNClassifier k={self.k}, metric='{self.metric}', "
                f"weights='{self.weights}', {status}, n_train={n}>")


if __name__ == "__main__":
    # Quick demo
    print("K-Nearest Neighbors Classifier Demo")
    print("=" * 50)

    X_train = [
        [5.1, 3.5], [4.9, 3.0], [4.7, 3.2],  # Class 0
        [7.0, 3.2], [6.4, 3.2], [6.9, 3.1],  # Class 1
    ]
    y_train = [0, 0, 0, 1, 1, 1]

    clf = KNNClassifier(k=3, metric='euclidean', weights='distance')
    clf.fit(X_train, y_train)

    X_test = [[5.0, 3.4], [6.7, 3.1]]
    predictions = clf.predict(X_test)
    probas = clf.predict_proba(X_test)

    print(f"\nTest samples:  {X_test}")
    print(f"Predictions:   {predictions}")
    print(f"Probabilities: {probas}")
    print(f"\nClassifier:    {clf}")
