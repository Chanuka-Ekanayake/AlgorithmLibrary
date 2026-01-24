import numpy as np
from typing import Tuple, List

class KMeans:
    """
    K-Means Clustering implementation from scratch using NumPy.
    
    This algorithm partitions N observations into K clusters in which each 
    observation belongs to the cluster with the nearest mean (centroid).
    """

    def __init__(self, k: int = 3, max_iters: int = 100, tolerance: float = 1e-4):
        """
        Args:
            k: The number of clusters to form.
            max_iters: Maximum number of iterations for the algorithm.
            tolerance: Convergence threshold (if centroids move less than this, we stop).
        """
        self.k = k
        self.max_iters = max_iters
        self.tolerance = tolerance
        self.centroids = None
        self.labels = None

    def _euclidean_distance(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """Calculates the straight-line distance between two points/vectors."""
        return np.sqrt(np.sum((x1 - x2) ** 2, axis=1))

    def fit(self, X: np.ndarray) -> 'KMeans':
        """
        Compute k-means clustering.
        
        LOGIC (Expectation-Maximization):
        1. Initialize centroids randomly.
        2. Assign each point to the nearest centroid (Expectation).
        3. Re-calculate centroids based on the mean of assigned points (Maximization).
        4. Repeat until convergence or max_iters.
        """
        # --- 1. Initialization ---
        # Randomly select k data points as initial centroids
        n_samples, n_features = X.shape
        random_indices = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[random_indices]

        for i in range(self.max_iters):
            # --- 2. Assignment Step (Expectation) ---
            # For each point, find distance to all k centroids and pick the closest
            old_centroids = self.centroids.copy()
            
            # self.labels stores the index of the closest centroid for each point
            self.labels = self._assign_clusters(X)

            # --- 3. Update Step (Maximization) ---
            # Move centroids to the mean of all points assigned to them
            for idx in range(self.k):
                points_in_cluster = X[self.labels == idx]
                if len(points_in_cluster) > 0:
                    self.centroids[idx] = np.mean(points_in_cluster, axis=0)

            # --- 4. Convergence Check ---
            # If centroids move less than our tolerance, we are done
            distances_moved = np.sqrt(np.sum((self.centroids - old_centroids) ** 2))
            if distances_moved < self.tolerance:
                print(f"Converged at iteration {i}")
                break

        return self

    def _assign_clusters(self, X: np.ndarray) -> np.ndarray:
        """Helper to find the nearest centroid for each point."""
        labels = []
        for point in X:
            # Reshape point to (1, features) to broadcast distance calc against all centroids
            distances = self._euclidean_distance(point, self.centroids)
            labels.append(np.argmin(distances))
        return np.array(labels)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict the closest cluster for new incoming data points."""
        return self._assign_clusters(X)