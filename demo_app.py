# demo_app.py - Streamlit Cloud compatible version
"""
Demo version of the news sentiment dashboard with sample data
This version works on Streamlit Cloud without requiring background services
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

st.set_page_config(page_title="News Sentiment Dashboard - Demo", layout="wide")
st.title("📰 Real-time News Sentiment Dashboard (Demo)")

# Generate demo data
def generate_demo_data():
    sample_news = [
        {"text": "Tech giants report record quarterly earnings", "sentiment": "Positive", "source": "TechNews", "prediction": 1},
        {"text": "Major data breach affects millions of users", "sentiment": "Negative", "source": "CyberDaily", "prediction": 0},
        {"text": "Revolutionary AI breakthrough announced", "sentiment": "Positive", "source": "AI Times", "prediction": 1},
        {"text": "Stock market crashes amid economic uncertainty", "sentiment": "Negative", "source": "Finance Today", "prediction": 0},
        {"text": "New renewable energy project shows promising results", "sentiment": "Positive", "source": "Green Tech", "prediction": 1},
        {"text": "Company layoffs hit tech sector hard", "sentiment": "Negative", "source": "Business Wire", "prediction": 0},
        {"text": "Startup raises $100M in Series A funding", "sentiment": "Positive", "source": "Startup News", "prediction": 1},
        {"text": "Cybersecurity threat targets major infrastructure", "sentiment": "Negative", "source": "Security Alert", "prediction": 0},
        {"text": "Innovation in healthcare technology saves lives", "sentiment": "Positive", "source": "Health Tech", "prediction": 1},
        {"text": "Supply chain disruptions continue to impact industry", "sentiment": "Negative", "source": "Supply Chain Today", "prediction": 0},
    ]
    
    # Add timestamps
    base_time = datetime.now()
    for i, item in enumerate(sample_news):
        item["publishedAt"] = (base_time - timedelta(minutes=i*15)).strftime("%Y-%m-%d %H:%M:%S")
        item["probability_positive"] = random.uniform(0.6, 0.9) if item["prediction"] == 1 else random.uniform(0.1, 0.4)
        item["probability_negative"] = 1 - item["probability_positive"]
        item["id"] = f"demo_{i}"
        item["url"] = f"https://example.com/news/{i}"
    
    return sample_news

# Load demo data
@st.cache_data
def load_demo_predictions():
    return generate_demo_data()

# Auto refresh checkbox
auto_refresh = st.checkbox("🔄 Auto refresh every 5 seconds", value=True)
if auto_refresh:
    st.rerun()

# Last refresh time
st.text(f"Last refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load demo data
demo_data = load_demo_predictions()

if demo_data:
    df = pd.DataFrame(demo_data)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Articles", len(df))
    with col2:
        positive_count = len(df[df['prediction'] == 1])
        st.metric("😊 Positive", positive_count)
    with col3:
        negative_count = len(df[df['prediction'] == 0])
        st.metric("😟 Negative", negative_count)
    
    # Charts
    st.subheader("📈 Sentiment Distribution")
    sentiment_counts = df['sentiment'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(sentiment_counts)
    with col2:
        st.pie_chart(sentiment_counts)
    
    # Latest predictions table
    st.subheader("📰 Latest News Predictions (Demo Data)")
    
    # Prepare display dataframe
    display_df = df[['publishedAt', 'text', 'source', 'sentiment']].copy()
    display_df['publishedAt'] = pd.to_datetime(display_df['publishedAt'])
    display_df = display_df.sort_values('publishedAt', ascending=False)
    
    # Add color coding
    def highlight_sentiment(row):
        if row['sentiment'] == 'Positive':
            return ['background-color: #d4edda'] * len(row)
        else:
            return ['background-color: #f8d7da'] * len(row)
    
    styled_df = display_df.style.apply(highlight_sentiment, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Show sample prediction details
    st.subheader("🔍 Sample Prediction Details")
    selected_idx = st.selectbox("Select article to view details:", 
                               range(len(df)), 
                               format_func=lambda x: f"{df.iloc[x]['text'][:50]}...")
    
    if selected_idx is not None:
        selected_item = df.iloc[selected_idx]
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Article Text:**", selected_item['text'])
            st.write("**Source:**", selected_item['source'])
            st.write("**Published:**", selected_item['publishedAt'])
        with col2:
            st.write("**Sentiment:**", selected_item['sentiment'])
            st.write("**Confidence:**", f"{selected_item['probability_positive']:.2%}" if selected_item['prediction'] == 1 else f"{selected_item['probability_negative']:.2%}")
            st.progress(selected_item['probability_positive'] if selected_item['prediction'] == 1 else selected_item['probability_negative'])

else:
    st.info("🔄 Loading demo data...")

# Information section
st.sidebar.header("ℹ️ About This Demo")
st.sidebar.write("""
This is a **demo version** of the News Sentiment Analysis system.

**🎯 Features:**
- Real-time sentiment analysis simulation
- Interactive dashboard
- Positive/Negative classification
- Confidence scores

**⚙️ Technology Stack:**
- Python & Streamlit
- Machine Learning (scikit-learn)
- TF-IDF Text Processing
- Real-time Data Processing

**🚀 Deployment:**
- Hosted on Streamlit Cloud
- Automatic updates from GitHub
- Responsive web interface
""")

st.sidebar.header("📊 Demo Statistics")
if demo_data:
    df = pd.DataFrame(demo_data)
    avg_confidence = df.apply(lambda row: row['probability_positive'] if row['prediction'] == 1 else row['probability_negative'], axis=1).mean()
    st.sidebar.metric("Average Confidence", f"{avg_confidence:.1%}")
    st.sidebar.metric("Positive Ratio", f"{(df['prediction'] == 1).mean():.1%}")

# Footer
st.markdown("---")
st.markdown("**🔗 GitHub:** [View Source Code](https://github.com/LAYA2525/news-sentiment-analysis)")
st.markdown("**💡 Note:** This is a demonstration version with sample data. The full version includes live news fetching from NewsAPI.org")