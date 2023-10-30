# Automodeling Data Pipeline Documentation

## How-to guide

* how to run the pipeline locally ?

-> Recommend docker-compose approach ? or venv ok ?
-> 

* how to setup my dev environment ?

-> black, mypy, isort, pytest, sphinx ?

* how to debug the pipeline ?

-> airflow UI, view the DAG

* how to develop a new task in the pipeline ?

A new task starts from a new module in the `tasks` python package. The first step is always to define the logic independently from any other layer such as file storage in s3 or airflow. Download an run experiments. When satifisfied with the result wrap the defined logic in a new function decorated with `@airflow_task`.

* 