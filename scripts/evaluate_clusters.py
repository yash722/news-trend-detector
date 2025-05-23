from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pandas as pd


df = pd.read_csv("data/clustered/reduced_embeddings.csv")
reduced_embeddings = df.values
labels = pd.read_csv("data/clustered/clustered_articles.csv")["cluster"].values

silhouette = silhouette_score(reduced_embeddings, labels)
db_score = davies_bouldin_score(reduced_embeddings, labels)
ch_score = calinski_harabasz_score(reduced_embeddings, labels)

print("\n Quantitative Metrics:")
print(f"• Silhouette Score:      {silhouette:.4f}")
print(f"• Davies-Bouldin Index:  {db_score:.4f}")
print(f"• Calinski-Harabasz:     {ch_score:.2f}")
