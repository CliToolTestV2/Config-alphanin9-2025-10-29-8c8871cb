eval_threshold_metrics = {'rmse': 0.9, 'r2': 0.3, 'mae': 0.8}

# Define pipeline arguments
arguments = {
    "url": "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    "target": "quality",
    "mlflow_tracking_uri": "http://mlflow.mlflow.svc.cluster.local:5000",
    "mlflow_s3_endpoint_url": "http://mlflow-minio-service.mlflow.svc.cluster.local:9000",
    "mlflow_experiment_name": "demo-notebook",
    "model_name": "wine-quality",
    "alpha": 0.5,
    "l1_ratio": 0.5,
    "threshold_metrics": eval_threshold_metrics
}