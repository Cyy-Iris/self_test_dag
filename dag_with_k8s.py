from datetime import datetime, timedelta
import numpy as np
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
import logging

default_args = {
    'owner': 'yiyu',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_log():
    logger.info("Task started.")
    try:
        print("The task is started")
        result = np.roots([1,-3,2])
        logger.info("Task completed successfully. Result: %s", result)
    except Exception as e:
        logger.error("Task failed: %s", str(e))
        raise

with DAG(
    default_args=default_args,
    dag_id="dag_with_k8s",
    start_date=datetime(2023, 10, 26),
    schedule_interval='0 3 * * Tue-Fri'
) as dag:
    task1 = KubernetesPodOperator(
    name="k8s_Operator_test",
    namespace="airflow",
    image="debian",
    cmds=["echo", "Hello, World!"],
    labels={"app":"k8s_operator_test"},
    task_id="k8s_Operator_demo",
    do_xcom_push=True,
    python_callable=test_log,
    )
    task1
