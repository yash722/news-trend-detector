# News Trend Detector And Summarizer

A fully automated pipeline to scrape, embed, cluster, summarize, and display summaries with WhatsApp notifications.

## Features
- Scrape articles daily
- Embed with MiniLM and cluster with UMAP + HDBSCAN/KMeans
- Summarize each cluster using Facebook BART CNN
- Streamlit dashboard with auto-refresh
- WhatsApp notifications via Twilio

## Tech Stack
- Apache Airflow
- Python + Transformers
- UMAP, HDBSCAN, KMeans
- Streamlit
- MLflow (for experiment tracking)
- Twilio (for WhatsApp)
- Docker Compose

## Run it Locally

```bash
docker compose up --build
```

Visit:
- Airflow: http://localhost:8080
- Streamlit: http://localhost:8501

## Folder Structure

```
.
├── dags/                   # Airflow DAGs
├── data/                   # Raw, clustered news (ignored)
├── logs/                   # Airflow logs (ignored)
├── scripts/                # All processing logic
├── ui/                     # Streamlit app
├── docker-compose.yml
├── Dockerfile              # Airflow container
├── .env.example            # Environment config (safe template)
├── README.md
└── .gitignore
```
