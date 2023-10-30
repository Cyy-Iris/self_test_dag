from airflow.decorators import task, dag
from kubernetes import config
from datetime import datetime
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 10, 30, tz="UTC"),
    catchup=False,
    tags=["k8s_python"],
    dag_id="dag_k8s_python",
)
@task.kubernetes(
    image="python:3.8-slim-buster",
    name="k8s_test",
    namespace="default",
    in_cluster=False,
)
def execute_in_k8s_pod():
    import time

    print("Hello from k8s pod")
    time.sleep(2)

@task.kubernetes(image="python:3.8-slim-buster", namespace="default", in_cluster=False)
def print_pattern():
    n = 5
    for i in range(0, n):
        # inner loop to handle number of columns
        # values changing acc. to outer loop
        for j in range(0, i + 1):
            # printing stars
            print("* ", end="")

        # ending line after each row
        print("\r")

execute_in_k8s_pod_instance = execute_in_k8s_pod()
print_pattern_instance = print_pattern()
