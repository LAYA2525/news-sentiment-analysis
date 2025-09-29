# stream_predict.py
"""
Spark Structured Streaming app:
- Reads JSON files created by news_fetcher in data/incoming/
- Applies saved PipelineModel to produce predictions
- Writes predicted records as JSON to data/predictions/ (append)
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.ml import PipelineModel

def main():
    spark = SparkSession.builder \
        .appName("NewsSentimentStreaming") \
        .master("local[*]") \
        .getOrCreate()

    # Define schema matching news_fetcher output
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("text", StringType(), True),
        StructField("publishedAt", StringType(), True),
        StructField("source", StringType(), True),
        StructField("url", StringType(), True)
    ])

    incoming_dir = "data/incoming"
    predictions_dir = "data/predictions"
    checkpoint_dir = "checkpoints/stream_predict"

    os.makedirs(incoming_dir, exist_ok=True)
    os.makedirs(predictions_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Read streaming JSON files
    stream_df = spark.readStream.schema(schema).json(incoming_dir)

    # Load trained PipelineModel (transformer only)
    model_path = "models/news_sentiment_pipeline"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Run train_model.py first.")

    model = PipelineModel.load(model_path)

    # Apply model to streaming dataframe
    transformed = model.transform(stream_df)

    # Select useful columns and map prediction numeric -> label
    # LogisticRegression uses prediction 0.0 or 1.0
    selected = transformed.selectExpr(
        "id", "text", "publishedAt", "source", "url",
        "prediction as pred"
    ).withColumnRenamed("pred", "prediction")

    # write predictions to disk as JSON (append). Each micro-batch will produce files.
    query = selected.writeStream \
        .format("json") \
        .option("path", predictions_dir) \
        .option("checkpointLocation", checkpoint_dir) \
        .outputMode("append") \
        .start()

    print("Streaming predictions started. Writing to", predictions_dir)
    query.awaitTermination()

if __name__ == "__main__":
    main()
