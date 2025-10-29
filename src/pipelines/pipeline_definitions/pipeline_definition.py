# pipeline_definitions.py
import sys

sys.path.append('../../src')
from components_py.pull_data_component.pull_data_component import pull_data
from components_py.preprocess_component.preprocess_component import preprocess
from components_py.train_component.train_component import train
from components_py.deploy_model_component.deploy_model_component import deploy_model
from components_py.inference_component.inference_component import inference
from components_py.evaluate_component.evaluate_component import evaluate

from kfp.aws import use_aws_secret


from kfp import dsl

@dsl.pipeline(
    name='demo-pipeline',
    description='An example pipeline for wine quality prediction.'
)

def pipeline(
    url: str,
    target: str,
    mlflow_experiment_name: str,
    mlflow_tracking_uri: str,
    mlflow_s3_endpoint_url: str,
    model_name: str,
    alpha: float,
    l1_ratio: float,
    threshold_metrics: dict,
):
    
    pull_task = pull_data(url=url)

    preprocess_task = preprocess(data=pull_task.outputs["data"])

    train_task = train(
        train_set=preprocess_task.outputs["train_set"],
        test_set=preprocess_task.outputs["test_set"],
        target=target,
        mlflow_experiment_name=mlflow_experiment_name,
        mlflow_tracking_uri=mlflow_tracking_uri,
        mlflow_s3_endpoint_url=mlflow_s3_endpoint_url,
        model_name=model_name,
        alpha=alpha,
        l1_ratio=l1_ratio
    )
    train_task.apply(use_aws_secret(secret_name="aws-secret"))

    evaluate_task = evaluate(
        run_id=train_task.outputs["run_id"],
        mlflow_tracking_uri=mlflow_tracking_uri,
        threshold_metrics=threshold_metrics
    )

    eval_passed = evaluate_task.output

    with dsl.Condition(eval_passed == "true"):
        deploy_model_task = deploy_model(
            model_name=model_name,
            storage_uri=train_task.outputs["storage_uri"],
        )

        inference_task = inference(
            model_name=model_name,
            scaler_in=preprocess_task.outputs["scaler_out"]
        )
        inference_task.after(deploy_model_task)
