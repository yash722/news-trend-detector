import pandas as pd
from transformers import pipeline
import os

def summarize_clusters(input_path="data/clustered/clustered_articles.csv", output_path="data/clustered/cluster_summaries.csv", max_chunk_tokens=1024):

    df = pd.read_csv(input_path)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")

    cluster_summaries = []

    for cluster_id in sorted(df['cluster'].unique()):
        texts = df[df['cluster'] == cluster_id]['text'].dropna().tolist()

        combined_text = " ".join(texts)
        combined_text = combined_text[:3000]

        try:
            summary = summarizer(combined_text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        except Exception as e:
            summary = f"[Error generating summary: {e}]"

        cluster_summaries.append({
            "cluster": cluster_id,
            "summary": summary,
            "num_articles": len(texts)
        })

    summary_df = pd.DataFrame(cluster_summaries)
    os.makedirs("data/clustered", exist_ok=True)
    summary_df.to_csv(output_path, index=False)
    print(f"Cluster summaries saved to: {output_path}")

if __name__ == "__main__":
    summarize_clusters()


# import pandas as pd
# from transformers import pipeline
# import os

# def summarize_clusters(input_path="data/clustered/clustered_articles.csv", output_path="data/clustered/cluster_summaries.csv", max_articles_per_cluster=5):

#     df = pd.read_csv(input_path)

#     # Use a smaller, faster summarization model
#     summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

#     cluster_summaries = []

#     for cluster_id in sorted(df['cluster'].unique()):
#         texts = df[df['cluster'] == cluster_id]['text'].dropna().tolist()

#         # Sample a few articles to represent the cluster
#         sample_texts = texts[:max_articles_per_cluster]

#         partial_summaries = []

#         for text in sample_texts:
#             try:
#                 input_length = len(text.split())
#                 max_len = min(100, int(input_length * 0.7))  # 70% of input
#                 max_len = max(max_len, 20)
#                 summary = summarizer(
#                     text[:1024], max_length=max_len, min_length=20, do_sample=False
#                 )[0]['summary_text']
#                 partial_summaries.append(summary)
#             except Exception as e:
#                 partial_summaries.append("[Error]")

#         # Combine partial summaries into a final cluster summary
#         final_summary = " ".join(partial_summaries)

#         cluster_summaries.append({
#             "cluster": cluster_id,
#             "summary": final_summary,
#             "num_articles": len(texts)
#         })

#     summary_df = pd.DataFrame(cluster_summaries)
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     summary_df.to_csv(output_path, index=False)
#     print(f"Cluster summaries saved to: {output_path}")


# if __name__ == "__main__":
#     summarize_clusters()