import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import pickle
import os

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "train.csv")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Please put training CSV at {data_path}")
    
    # Load data using pandas
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} rows of training data")
    
    # Clean data
    df = df.dropna(subset=['text', 'label'])
    print(f"After cleaning: {len(df)} rows")
    
    X = df['text']
    y = df['label']
    
    # Create TF-IDF features
    print("Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', lowercase=True)
    X_tfidf = vectorizer.fit_transform(X)
    
    # For small datasets, we'll use the entire dataset for training
    if len(df) < 20:
        print("Small dataset: using all data for training and evaluation")
        X_train, X_test = X_tfidf, X_tfidf
        y_train, y_test = y, y
    else:
        X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
    
    # Train model
    print("Training logistic regression model...")
    model = LogisticRegression(max_iter=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    models_dir = os.path.join(script_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "sentiment_model.pkl")
    vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    
    print(f"Saving model to {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Saving vectorizer to {vectorizer_path}")
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Training completed successfully!")

if __name__ == "__main__":
    main()