# app_streamlit.py
"""
Simple Streamlit dashboard that reads JSON files from data/predictions/
and shows a live table and counts of predictions.
Run: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import glob, os, json
from datetime import datetime

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
PRED_DIR = os.path.join(script_dir, "data", "predictions")

st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")
st.title("Real-time News Sentiment Dashboard (PySpark)")

def load_predictions(limit_files=500):
    if not os.path.exists(PRED_DIR):
        return pd.DataFrame()
    files = glob.glob(os.path.join(PRED_DIR, "*.json"))
    files = sorted(files, key=os.path.getmtime, reverse=True)[:limit_files]
    rows = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                # file may contain JSON lines or a single JSON object
                content = fh.read().strip()
                if not content:
                    continue
                # try parse as JSON array / object / lines
                try:
                    parsed = json.loads(content)
                    # If parsed is a list
                    if isinstance(parsed, list):
                        rows.extend(parsed)
                    elif isinstance(parsed, dict):
                        rows.append(parsed)
                except json.JSONDecodeError:
                    # Fallback: parse line by line
                    with open(f, "r", encoding="utf-8") as fh2:
                        for line in fh2:
                            line=line.strip()
                            if not line:
                                continue
                            try:
                                rows.append(json.loads(line))
                            except:
                                pass
        except Exception as e:
            print("Error reading", f, e)
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    # map numeric predictions to labels if present
    if "prediction" in df.columns:
        df["prediction_label"] = df["prediction"].map({0.0: "Negative", 0: "Negative", 1.0: "Positive", 1: "Positive"})
    else:
        df["prediction_label"] = None
    # nicer timestamp
    if "publishedAt" in df.columns:
        try:
            df["publishedAt_parsed"] = pd.to_datetime(df["publishedAt"], errors="coerce")
        except:
            df["publishedAt_parsed"] = None
    return df

auto_refresh = st.checkbox("Auto refresh every 5 seconds", value=False)
placeholder = st.empty()

refresh = True
while refresh:
    df = load_predictions()
    with placeholder.container():
        st.markdown(f"**Last refresh:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if df.empty:
            st.info("No predictions yet. Start the streaming job and news fetcher.")
        else:
            st.subheader("Latest predictions (top 50)")
            display_df = df.sort_values(by="publishedAt_parsed", ascending=False).head(50)
            st.dataframe(display_df[["publishedAt", "text", "source", "url", "prediction_label"]])

            counts = display_df["prediction_label"].value_counts().reindex(["Positive","Negative"]).fillna(0)
            st.subheader("Counts")
            st.bar_chart(counts)

    if auto_refresh:
        import time
        time.sleep(5)
        # continue loop -> refresh
    else:
        break
