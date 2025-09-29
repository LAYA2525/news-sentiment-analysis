# train_model.py
"""
Train a PySpark ML pipeline on data/train.csv and save the PipelineModel to models/
"""

import os
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

def main():
    spark = SparkSession.builder \
        .appName("NewsSentimentTraining") \
        .master("local[*]") \
        .getOrCreate()

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "train.csv")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Please put training CSV at {data_path}")

    df = spark.read.csv(data_path, header=True, inferSchema=True)
    # Expect df columns: 'id', 'text', 'label' (label: 1 for positive, 0 for negative)
    df = df.select("text", "label").na.drop()
    
    print(f"Total rows in dataset: {df.count()}")
    
    # Pipeline stages
    tokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W+")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=1000)  # Reduced for small dataset
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)  # Reduced iterations

    pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, lr])

    # For small datasets, use the entire dataset for training and evaluation
    row_count = df.count()
    if row_count < 20:
        print("Small dataset detected. Using entire dataset for training and evaluation.")
        train = df
        test = df  # Use same data for evaluation in small datasets
    else:
        train, test = df.randomSplit([0.8, 0.2], seed=42)
    
    print(f"Training on {train.count()} rows")
    model = pipeline.fit(train)

    predictions = model.transform(test)
    print(f"Evaluating on {test.count()} rows")
    
    # Show some predictions for debugging
    print("\nSample predictions:")
    predictions.select("text", "label", "prediction", "probability").show(5, truncate=False)
    
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
    try:
        auc = evaluator.evaluate(predictions)
        print(f"AUC on evaluation set = {auc:.4f}")
    except Exception as e:
        print("Could not compute AUC (maybe small evaluation set).", e)
        # Try accuracy instead
        try:
            from pyspark.ml.evaluation import MulticlassClassificationEvaluator
            accuracy_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
            accuracy = accuracy_evaluator.evaluate(predictions)
            print(f"Accuracy = {accuracy:.4f}")
        except Exception as e2:
            print("Could not compute accuracy either:", e2)

    model_path = os.path.join(script_dir, "models", "news_sentiment_pipeline")
    print("Saving model to", model_path)
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    model.write().overwrite().save(model_path)

    spark.stop()

if __name__ == "__main__":
    main()
