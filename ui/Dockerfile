# ui/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the dashboard
CMD ["streamlit", "run", "streamlit_dashboard.py", "--server.port=8501", "--server.enableCORS=false"]
