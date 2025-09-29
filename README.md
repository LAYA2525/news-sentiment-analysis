# 📰 Real-Time News Sentiment Analysis System

A complete real-time news sentiment analysis pipeline that fetches live news articles, analyzes their sentiment using machine learning, and displays results in an interactive web dashboard.

![System Architecture](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red) ![ML](https://img.shields.io/badge/ML-Scikit--learn-green)

## 🌟 Features

- **Real-time News Fetching**: Automatically fetches live news from NewsAPI.org
- **AI Sentiment Analysis**: Uses trained machine learning models to classify news as positive/negative
- **Interactive Dashboard**: Beautiful Streamlit web interface with live updates
- **Scalable Architecture**: Modular design with separate services for fetching, processing, and visualization
- **Easy Deployment**: Ready for deployment on Streamlit Cloud, Heroku, or other platforms

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   News Fetcher  │───▶│ Prediction Engine│───▶│   Dashboard     │
│  (news_fetcher) │    │(stream_predict)  │    │ (app_streamlit) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   NewsAPI.org              ML Model               Web Browser
                         (scikit-learn)          (localhost:8501)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- NewsAPI.org API key (free at https://newsapi.org/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/news-sentiment-analysis.git
   cd news-sentiment-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your NewsAPI key:
   ```
   NEWS_API_KEY=your_api_key_here
   POLL_INTERVAL_SECONDS=30
   NEWS_QUERY=technology
   PAGE_SIZE=10
   ```

4. **Train the ML model:**
   ```bash
   python train_model_simple.py
   ```

5. **Run the system:**
   
   **Option A: All-in-one (recommended for development):**
   ```bash
   # Terminal 1 - Start dashboard
   streamlit run app_streamlit.py
   
   # Terminal 2 - Start news fetcher
   python news_fetcher.py
   
   # Terminal 3 - Start prediction service
   python stream_predict_simple.py
   ```
   
   **Option B: Single command (if available):**
   ```bash
   python run_all.py  # If you create this orchestrator
   ```

6. **Open your browser:**
   Visit `http://localhost:8501` to see the dashboard!

## 📊 Dashboard Features

- **Live News Feed**: Shows latest news articles with sentiment predictions
- **Sentiment Charts**: Visual representation of positive vs negative news
- **Real-time Updates**: Automatically refreshes as new articles are processed
- **Source Attribution**: Shows original news sources and publication dates
- **Confidence Scores**: Displays ML model confidence for each prediction

## 🛠️ Project Structure

```
news-sentiment/
├── app_streamlit.py          # Main dashboard application
├── news_fetcher.py           # News fetching service
├── stream_predict_simple.py  # ML prediction service
├── train_model_simple.py     # Model training script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md               # This file
├── data/
│   ├── train.csv           # Training data for ML model
│   ├── incoming/           # Raw news articles (JSON)
│   └── predictions/        # Processed predictions (JSON)
├── models/
│   ├── sentiment_model.pkl     # Trained ML model
│   └── tfidf_vectorizer.pkl   # Text vectorizer
└── checkpoints/            # Model checkpoints (if using Spark)
```

## 🔧 Configuration

### Environment Variables (.env)
- `NEWS_API_KEY`: Your NewsAPI.org API key
- `POLL_INTERVAL_SECONDS`: How often to fetch news (default: 30)
- `NEWS_QUERY`: News search query (default: "technology")
- `PAGE_SIZE`: Number of articles per fetch (default: 10)

### Model Training Data
The system includes sample training data in `data/train.csv`. You can:
- Use the provided sample data for testing
- Replace with your own labeled dataset
- Expand the training data for better accuracy

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your NewsAPI key in Streamlit Cloud secrets
5. Deploy!

### Option 2: Heroku
1. Create `Procfile`:
   ```
   web: streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Set environment variables in Heroku dashboard
3. Deploy via Git or GitHub integration

### Option 3: Docker
1. Create `Dockerfile` (contact for template)
2. Build and deploy to any container platform

## 🤖 Machine Learning Details

- **Algorithm**: Logistic Regression with TF-IDF features
- **Framework**: scikit-learn
- **Input**: News article text
- **Output**: Binary sentiment (Positive/Negative) + confidence scores
- **Training Data**: Labeled news articles (expandable)

## 🔍 API Integration

The system uses NewsAPI.org for fetching live news:
- **Free Tier**: 1000 requests/day
- **Supported Sources**: 80,000+ news sources worldwide
- **Categories**: Technology, business, sports, etc.
- **Real-time**: Updates every 15 minutes

## 🛡️ Security & Best Practices

- API keys stored in environment variables
- `.env` file excluded from version control
- Rate limiting for API calls
- Error handling and graceful degradation
- Modular architecture for easy maintenance

## 🔧 Troubleshooting

### Common Issues:
1. **Model not found error**: Run `python train_model_simple.py` first
2. **API key error**: Check your `.env` file and NewsAPI key
3. **Dashboard not loading**: Ensure all services are running
4. **No predictions**: Check if news fetcher is getting articles

### Debug Mode:
Set environment variable `DEBUG=True` for verbose logging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] Multi-language sentiment analysis
- [ ] Advanced NLP models (BERT, GPT)
- [ ] Real-time notifications for significant sentiment changes
- [ ] Historical trend analysis
- [ ] Multiple news sources integration
- [ ] Automated model retraining
- [ ] Mobile-responsive design

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NewsAPI.org](https://newsapi.org/) for providing news data
- [Streamlit](https://streamlit.io/) for the amazing dashboard framework
- [scikit-learn](https://scikit-learn.org/) for machine learning capabilities

## 📞 Support

- Create an issue for bug reports
- Start a discussion for feature requests
- Contact: [your-email@example.com]

---

⭐ **Star this repository if you found it helpful!** ⭐