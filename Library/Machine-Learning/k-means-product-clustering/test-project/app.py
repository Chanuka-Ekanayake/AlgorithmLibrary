import sys
import os
import numpy as np

# Add the parent directory to the path to import the core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.kmeans import KMeans

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def product_clustering_simulation():
    clear_screen()
    print("==================================================")
    print("🤖 ML MARKETPLACE: AUTOMATED PRODUCT TIERING 🤖")
    print("==================================================\n")

    # 1. THE DATASET
    # Representing ML Models as [Complexity Score, Compute Requirement] (1-10 scale)
    products = {
        "Linear Regression": [1.5, 1.2],
        "Logistic Regression": [1.8, 1.5],
        "Decision Tree": [3.0, 2.5],
        "Random Forest": [5.5, 6.0],
        "XGBoost": [6.5, 7.5],
        "Llama-3-8B": [8.5, 9.0],
        "GPT-4-Turbo": [9.5, 10.0],
        "Stable Diffusion": [8.0, 8.5],
        "K-Means Tool": [2.5, 2.0]
    }

    product_names = list(products.keys())
    # Convert dictionary values to a NumPy array for the algorithm
    X = np.array(list(products.values()))

    print(f"📊 Dataset Loaded: {len(product_names)} software models indexed.")
    print("Each model is scored on 'Logic Complexity' and 'Hardware Demand'.\n")

    # 2. USER INPUT
    try:
        k = int(input("How many categories/tiers should we create? (Default 3): ") or 3)
    except ValueError:
        k = 3

    # 3. INITIALIZING AND FITTING THE MODEL
    print(f"\n🚀 Clustering products into {k} tiers...")
    model = KMeans(k=k, max_iters=50)
    model.fit(X)

    # 4. RESULTS DISPLAY
    clear_screen()
    print("✅ CLUSTERING COMPLETE\n")
    
    clusters = {}
    for i in range(k):
        clusters[i] = []

    # Map product names to their calculated labels
    for name, label in zip(product_names, model.labels):
        clusters[label].append(name)

    # Display the "Market Tiers"
    for cluster_id, items in clusters.items():
        centroid = model.centroids[cluster_id]
        tier_type = "Unclassified"
        
        # Simple heuristic to name tiers based on centroid position
        avg_score = np.mean(centroid)
        if avg_score < 4: tier_type = "Tier 1: Lightweight / Entry-Level"
        elif avg_score < 7: tier_type = "Tier 2: Professional / Mid-Range"
        else: tier_type = "Tier 3: Enterprise / High-Performance"

        print(f"🔹 {tier_type}")
        print(f"   (Avg Complexity: {centroid[0]:.1f}, Avg Compute: {centroid[1]:.1f})")
        for item in items:
            print(f"    - {item}")
        print("-" * 40)

    # 5. PREDICTION SIMULATION
    print("\n🔮 TEST: Predict tier for a new model")
    try:
        comp = float(input("Enter new model complexity (1-10): "))
        res = float(input("Enter new model compute demand (1-10): "))
        
        new_point = np.array([[comp, res]])
        prediction = model.predict(new_point)[0]
        
        print(f"\n➡️ This new model belongs in Cluster Group: {prediction}")
    except ValueError:
        print("Invalid input for prediction.")

if __name__ == "__main__":
    product_clustering_simulation()