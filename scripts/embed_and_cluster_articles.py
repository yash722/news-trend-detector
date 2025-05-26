import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import os
import umap.umap_ as umap
import mlflow
import hdbscan
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def cluster_articles(
    input_path=None,
    output_path="data/clustered/clustered_articles.csv",
    n_clusters=5,
    use_hdbscan=False
):
    if not input_path:
        input_path = sorted(os.listdir("data/raw"))[-1]
        input_path = os.path.join("data/raw", input_path)

    df = pd.read_csv(input_path)
    print("Read articles:", len(df))

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)
    print("Embedded articles")

    reducer = umap.UMAP(n_components=5, random_state=42)
    reduced_embeddings = reducer.fit_transform(embeddings)
    pd.DataFrame(reduced_embeddings).to_csv("data/clustered/reduced_embeddings.csv", index=False)

    if use_hdbscan:
        print("Using HDBSCAN for clustering...")
        clusterer = hdbscan.HDBSCAN(min_cluster_size=5)
        clusters = clusterer.fit_predict(reduced_embeddings)
    else:
        print(f"Using KMeans (k={n_clusters}) for clustering...")
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(reduced_embeddings)

    df['cluster'] = clusters
    os.makedirs("data/clustered", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved clustered articles to: {output_path}")

    # Evaluate metrics (only if at least 2 valid clusters)
    valid_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
    if valid_clusters >= 2:
        silhouette = silhouette_score(reduced_embeddings, clusters)
        db_score = davies_bouldin_score(reduced_embeddings, clusters)
        ch_score = calinski_harabasz_score(reduced_embeddings, clusters)

        print("\nClustering Metrics:")
        print(f"• Silhouette Score:      {silhouette:.4f}")
        print(f"• Davies-Bouldin Index:  {db_score:.4f}")
        print(f"• Calinski-Harabasz:     {ch_score:.2f}")
    else:
        silhouette = db_score = ch_score = None
        print("\nNot enough clusters to compute metrics.")

    # MLflow logging
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("News Clustering")

    with mlflow.start_run(run_name="daily_cluster_run_hdbscan" if use_hdbscan else "daily_cluster_run_kmeans"):
         mlflow.log_param("embedding_model", "all-MiniLM-L6-v2")
         mlflow.log_param("clustering_algo", "HDBSCAN" if use_hdbscan else "KMeans")
         if not use_hdbscan:
             mlflow.log_param("n_clusters", n_clusters)
         if silhouette is not None:
             mlflow.log_metric("silhouette_score", silhouette)
             mlflow.log_metric("davies_bouldin_index", db_score)
             mlflow.log_metric("calinski_harabasz_score", ch_score)
         mlflow.log_artifact(output_path)
         mlflow.log_artifact("data/clustered/reduced_embeddings.csv")

         print("MLflow tracking logged successfully.")

# if __name__ == "__main__":
#    cluster_articles(use_hdbscan=True)
