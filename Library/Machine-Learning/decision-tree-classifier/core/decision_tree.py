"""
Decision Tree Classifier - CART Implementation

This module implements the Classification and Regression Trees (CART) algorithm
for building decision trees using impurity-based splitting (Gini impurity or entropy).

Algorithm:
- Recursively split data based on feature that maximizes information gain
- Use Gini impurity or entropy for split quality measurement
- Build tree until stopping criteria met (max depth, min samples, pure nodes)
- Predict by traversing tree from root to leaf

Time Complexity: O(n * m * log n) where n=samples, m=features
Space Complexity: O(n * log n) for tree storage

Author: Algorithm Library
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter


class TreeNode:
    """
    Represents a node in the decision tree.
    
    Attributes:
        feature: Feature index to split on (None for leaf nodes)
        threshold: Threshold value for split (None for leaf nodes)
        left: Left child node (feature <= threshold)
        right: Right child node (feature > threshold)
        value: Class label for leaf nodes (None for internal nodes)
        samples: Number of samples in this node
        impurity: Gini impurity or entropy of this node
    """
    
    def __init__(self, feature: Optional[int] = None, threshold: Optional[float] = None,
                 left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None,
                 value: Optional[Any] = None, samples: int = 0, impurity: float = 0.0):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.samples = samples
        self.impurity = impurity
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf node."""
        return self.value is not None


class DecisionTreeClassifier:
    """
    Decision Tree Classifier using CART algorithm.
    
    Supports both Gini impurity and entropy for split criteria.
    Handles categorical and numerical features.
    """
    
    def __init__(self, max_depth: Optional[int] = None, min_samples_split: int = 2,
                 min_samples_leaf: int = 1, criterion: str = 'gini'):
        """
        Initialize Decision Tree Classifier.
        
        Args:
            max_depth: Maximum depth of tree (None for unlimited)
            min_samples_split: Minimum samples required to split node
            min_samples_leaf: Minimum samples required in leaf node
            criterion: Split criterion - 'gini' or 'entropy'
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.root = None
        self.n_features = None
        self.classes = None
    
    def _calculate_impurity(self, y: List[Any]) -> float:
        """
        Calculate impurity of labels using specified criterion.
        
        Args:
            y: List of class labels
            
        Returns:
            Impurity value (Gini or entropy)
        """
        if len(y) == 0:
            return 0.0
        
        # Count class frequencies
        class_counts = Counter(y)
        n_samples = len(y)
        
        if self.criterion == 'gini':
            # Gini impurity: 1 - sum(p_i^2)
            impurity = 1.0
            for count in class_counts.values():
                prob = count / n_samples
                impurity -= prob ** 2
            return impurity
        
        elif self.criterion == 'entropy':
            # Entropy: -sum(p_i * log2(p_i))
            entropy = 0.0
            for count in class_counts.values():
                prob = count / n_samples
                if prob > 0:
                    entropy -= prob * math.log2(prob)
            return entropy
        
        else:
            raise ValueError(f"Unknown criterion: {self.criterion}")
    
    def _split_data(self, X: List[List[float]], y: List[Any], 
                    feature: int, threshold: float) -> Tuple[Tuple[List, List], Tuple[List, List]]:
        """
        Split dataset based on feature and threshold.
        
        Args:
            X: Feature matrix
            y: Labels
            feature: Feature index to split on
            threshold: Threshold value
            
        Returns:
            ((X_left, y_left), (X_right, y_right))
        """
        left_indices = []
        right_indices = []
        
        for i, sample in enumerate(X):
            if sample[feature] <= threshold:
                left_indices.append(i)
            else:
                right_indices.append(i)
        
        X_left = [X[i] for i in left_indices]
        y_left = [y[i] for i in left_indices]
        X_right = [X[i] for i in right_indices]
        y_right = [y[i] for i in right_indices]
        
        return (X_left, y_left), (X_right, y_right)
    
    def _information_gain(self, y: List[Any], y_left: List[Any], y_right: List[Any]) -> float:
        """
        Calculate information gain from split.
        
        Args:
            y: Parent labels
            y_left: Left child labels
            y_right: Right child labels
            
        Returns:
            Information gain value
        """
        n = len(y)
        n_left = len(y_left)
        n_right = len(y_right)
        
        if n_left == 0 or n_right == 0:
            return 0.0
        
        # Information gain = parent_impurity - weighted_child_impurity
        parent_impurity = self._calculate_impurity(y)
        left_impurity = self._calculate_impurity(y_left)
        right_impurity = self._calculate_impurity(y_right)
        
        weighted_child_impurity = (n_left / n) * left_impurity + (n_right / n) * right_impurity
        
        return parent_impurity - weighted_child_impurity
    
    def _best_split(self, X: List[List[float]], y: List[Any]) -> Tuple[Optional[int], Optional[float], float]:
        """
        Find best feature and threshold to split on.
        
        Args:
            X: Feature matrix
            y: Labels
            
        Returns:
            (best_feature, best_threshold, best_gain)
        """
        best_gain = -float('inf')
        best_feature = None
        best_threshold = None
        
        n_samples = len(X)
        
        # Try each feature
        for feature in range(self.n_features):
            # Get unique values for this feature
            feature_values = sorted(set(sample[feature] for sample in X))
            
            # Try thresholds between consecutive unique values
            for i in range(len(feature_values) - 1):
                threshold = (feature_values[i] + feature_values[i + 1]) / 2
                
                # Split data
                (X_left, y_left), (X_right, y_right) = self._split_data(X, y, feature, threshold)
                
                # Check minimum samples constraint
                if len(y_left) < self.min_samples_leaf or len(y_right) < self.min_samples_leaf:
                    continue
                
                # Calculate information gain
                gain = self._information_gain(y, y_left, y_right)
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold, best_gain
    
    def _build_tree(self, X: List[List[float]], y: List[Any], depth: int = 0) -> TreeNode:
        """
        Recursively build decision tree.
        
        Args:
            X: Feature matrix
            y: Labels
            depth: Current depth in tree
            
        Returns:
            TreeNode representing root of subtree
        """
        n_samples = len(y)
        n_classes = len(set(y))
        
        # Create node
        node = TreeNode(samples=n_samples, impurity=self._calculate_impurity(y))
        
        # Stopping criteria
        if (depth >= self.max_depth if self.max_depth is not None else False) or \
           n_classes == 1 or \
           n_samples < self.min_samples_split:
            # Make leaf node - assign most common class
            node.value = Counter(y).most_common(1)[0][0]
            return node
        
        # Find best split
        best_feature, best_threshold, best_gain = self._best_split(X, y)
        
        # If no good split found, make leaf
        if best_feature is None or best_gain <= 0:
            node.value = Counter(y).most_common(1)[0][0]
            return node
        
        # Split data and build children
        (X_left, y_left), (X_right, y_right) = self._split_data(X, y, best_feature, best_threshold)
        
        node.feature = best_feature
        node.threshold = best_threshold
        node.left = self._build_tree(X_left, y_left, depth + 1)
        node.right = self._build_tree(X_right, y_right, depth + 1)
        
        return node
    
    def fit(self, X: List[List[float]], y: List[Any]) -> 'DecisionTreeClassifier':
        """
        Train decision tree on dataset.
        
        Args:
            X: Training features (n_samples x n_features)
            y: Training labels (n_samples)
            
        Returns:
            self
        """
        self.n_features = len(X[0]) if X else 0
        self.classes = sorted(set(y))
        
        # Build tree
        self.root = self._build_tree(X, y)
        
        return self
    
    def _predict_sample(self, sample: List[float], node: TreeNode) -> Any:
        """
        Predict class for single sample by traversing tree.
        
        Args:
            sample: Feature vector
            node: Current node
            
        Returns:
            Predicted class label
        """
        # Reached leaf node
        if node.is_leaf():
            return node.value
        
        # Traverse tree based on feature value
        if sample[node.feature] <= node.threshold:
            return self._predict_sample(sample, node.left)
        else:
            return self._predict_sample(sample, node.right)
    
    def predict(self, X: List[List[float]]) -> List[Any]:
        """
        Predict classes for samples.
        
        Args:
            X: Feature matrix (n_samples x n_features)
            
        Returns:
            List of predicted class labels
        """
        # Ensure the tree has been trained before making predictions
        if not hasattr(self, "root") or self.root is None:
            raise ValueError(
                "DecisionTreeClassifier instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using 'predict'."
            )
        return [self._predict_sample(sample, self.root) for sample in X]
    
    def predict_proba(self, X: List[List[float]]) -> List[Dict[Any, float]]:
        """
        Predict class probabilities for samples.
        
        Args:
            X: Feature matrix
            
        Returns:
            List of dictionaries mapping class to probability
        """
        # For simplicity, return 1.0 for predicted class, 0.0 for others
        predictions = self.predict(X)
        probas = []
        
        for pred in predictions:
            proba = {cls: 0.0 for cls in self.classes}
            proba[pred] = 1.0
            probas.append(proba)
        
        return probas
    
    def get_depth(self, node: Optional[TreeNode] = None) -> int:
        """
        Get depth of tree.
        
        Args:
            node: Current node (None to start from root)
            
        Returns:
            Maximum depth of tree
        """
        if node is None:
            node = self.root
        
        if node is None or node.is_leaf():
            return 0
        
        return 1 + max(self.get_depth(node.left), self.get_depth(node.right))
    
    def get_n_leaves(self, node: Optional[TreeNode] = None) -> int:
        """
        Count number of leaf nodes.
        
        Args:
            node: Current node (None to start from root)
            
        Returns:
            Number of leaf nodes
        """
        if node is None:
            node = self.root
        
        if node is None:
            return 0
        
        if node.is_leaf():
            return 1
        
        return self.get_n_leaves(node.left) + self.get_n_leaves(node.right)
    
    def feature_importances(self) -> List[float]:
        """
        Calculate feature importance based on information gain.
        
        Returns:
            List of importance values for each feature
        """
        importances = [0.0] * self.n_features
        
        def traverse(node):
            if node is None or node.is_leaf():
                return
            
            # Add this node's contribution to feature importance based on
            # the weighted impurity decrease from this split.
            if node.left is not None and node.right is not None and node.samples > 0:
                weighted_child_impurity = (
                    (node.left.samples * node.left.impurity) +
                    (node.right.samples * node.right.impurity)
                ) / node.samples
                impurity_decrease = node.impurity - weighted_child_impurity
                importances[node.feature] += node.samples * impurity_decrease
            
            traverse(node.left)
            traverse(node.right)
        
        traverse(self.root)
        
        # Normalize
        total = sum(importances)
        if total > 0:
            importances = [imp / total for imp in importances]
        
        return importances


def accuracy_score(y_true: List[Any], y_pred: List[Any]) -> float:
    """
    Calculate classification accuracy.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Accuracy (fraction of correct predictions)
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true)


if __name__ == "__main__":
    # Example usage
    print("Decision Tree Classifier Demo")
    print("=" * 50)
    
    # Sample dataset: Iris-like data
    X_train = [
        [5.1, 3.5], [4.9, 3.0], [4.7, 3.2],  # Class 0
        [7.0, 3.2], [6.4, 3.2], [6.9, 3.1],  # Class 1
        [6.5, 3.0], [6.2, 2.2], [5.9, 3.0]   # Class 1
    ]
    y_train = [0, 0, 0, 1, 1, 1, 1, 1, 1]
    
    X_test = [
        [5.0, 3.4],  # Should be class 0
        [6.7, 3.1]   # Should be class 1
    ]
    
    # Train tree
    clf = DecisionTreeClassifier(max_depth=3, criterion='gini')
    clf.fit(X_train, y_train)
    
    # Predict
    predictions = clf.predict(X_test)
    
    print(f"\nTest samples: {X_test}")
    print(f"Predictions: {predictions}")
    print(f"\nTree depth: {clf.get_depth()}")
    print(f"Number of leaves: {clf.get_n_leaves()}")
    print(f"Feature importances: {clf.feature_importances()}")
