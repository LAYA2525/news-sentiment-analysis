import pandas as pd
import json
import os
import glob
import time
import pickle
from datetime import datetime

def load_model_and_vectorizer():
    """Load the trained sklearn model and vectorizer"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(script_dir, "models", "tfidf_vectorizer.pkl")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Run train_model_simple.py first.")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer not found at {vectorizer_path}. Run train_model_simple.py first.")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    return model, vectorizer

def predict_sentiment(text, model, vectorizer):
    """Predict sentiment for a single text"""
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)[0]
    probability = model.predict_proba(text_tfidf)[0]
    
    return {
        "prediction": int(prediction),
        "probability_negative": float(probability[0]),
        "probability_positive": float(probability[1]),
        "sentiment": "positive" if prediction == 1 else "negative"
    }

def process_incoming_files():
    """Process JSON files from the incoming directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    incoming_dir = os.path.join(script_dir, "data", "incoming")
    predictions_dir = os.path.join(script_dir, "data", "predictions")
    
    # Create directories if they don't exist
    os.makedirs(incoming_dir, exist_ok=True)
    os.makedirs(predictions_dir, exist_ok=True)
    
    # Load model and vectorizer
    print("Loading model and vectorizer...")
    model, vectorizer = load_model_and_vectorizer()
    print("Model loaded successfully!")
    
    processed_files = set()
    
    while True:
        try:
            # Look for new JSON files in incoming directory
            json_files = glob.glob(os.path.join(incoming_dir, "*.json"))
            
            new_files = [f for f in json_files if f not in processed_files]
            
            if new_files:
                print(f"Found {len(new_files)} new files to process")
                
                for file_path in new_files:
                    try:
                        print(f"Processing {os.path.basename(file_path)}")
                        
                        # Read the JSON file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Handle both single objects and arrays
                        if isinstance(data, dict):
                            data = [data]
                        
                        predictions = []
                        for item in data:
                            if 'text' in item:
                                # Predict sentiment
                                pred_result = predict_sentiment(item['text'], model, vectorizer)
                                
                                # Create prediction record
                                prediction = {
                                    'id': item.get('id', 'unknown'),
                                    'text': item['text'],
                                    'publishedAt': item.get('publishedAt', datetime.now().isoformat()),
                                    'source': item.get('source', 'unknown'),
                                    'url': item.get('url', ''),
                                    'prediction': pred_result['prediction'],
                                    'sentiment': pred_result['sentiment'],
                                    'probability_positive': pred_result['probability_positive'],
                                    'probability_negative': pred_result['probability_negative'],
                                    'processed_at': datetime.now().isoformat()
                                }
                                predictions.append(prediction)
                        
                        # Save predictions
                        if predictions:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            output_file = os.path.join(predictions_dir, f"predictions_{timestamp}.json")
                            
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(predictions, f, indent=2)
                            
                            print(f"Saved {len(predictions)} predictions to {os.path.basename(output_file)}")
                        
                        processed_files.add(file_path)
                        
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
            
            # Sleep for a bit before checking again
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\\nStopping prediction service...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Starting News Sentiment Prediction Service (sklearn version)")
    print("Place JSON files in data/incoming/ directory")
    print("Predictions will be saved to data/predictions/ directory")
    print("Press Ctrl+C to stop")
    process_incoming_files()