import streamlit as st
import pandas as pd
import os
import time
from streamlit_autorefresh import st_autorefresh



st.set_page_config(page_title="News Trend Dashboard", layout="wide")
st.title("News Cluster Summaries")
count = st_autorefresh(interval=60 * 1000, limit=None, key="dashboard_refresh")

st.caption(f"Page reload count: {count}")

file_path = "data/clustered/cluster_summaries.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    # Show last modified timestamp
    updated_time = time.ctime(os.path.getmtime(file_path))
    st.caption(f"Last updated: {updated_time}")

    st.dataframe(df, use_container_width=True)
else:
    st.warning("Wait for a min!")

