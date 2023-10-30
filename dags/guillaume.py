"""Main Automodeling Airflow DAG.

This module contains the main apache airflow DAG taking as input parameter a PDF path of
a file in S3 and outputting a graph representation of that PDF. Each task in the DAG
write its intermediary results to S3 and share dependencies with the following one.

It exposes:
    * :DAG:main: actual apache airflow DAG.
"""
import os

import pendulum
from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.operators.python import get_current_context


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    name="Gauillaume_code_test",
    tags=["k8s_python"],
    params={"pdf_path": Param("path to a pdf to run the DAG on.")},
)
def main():
    """Main Automodeling pipeline DAG for computable contracts.

    it takes as parameter a full path to a pdf file in s3. If the pdf_path parameter
    provided is only a file it will use the following folder `"s3://raw_pdf/"`.
    """
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    #def starting_task() -> dict[str, str]:
    def starting_task():
        """Starting task initiating the chain of dependency based on the DAG params.

        it loads the pdf file path provided as parameter of the DAG using the context
        provided by airflow.

        Returns:

            A dict with key corresponding to an s3 folder path and the value an actual
            filename within that path. It corresponds to the `airflow_inputs` of the
            next task and help the downstream task perform input file resolution from
            s3 folder path inputs definition.
        """
        context = get_current_context()
        if "params" not in context:
            raise KeyError("DAG parameters couldn't be retrieved in current context.")
        filename: str = os.path.basename(context["params"]["pdf_path"])
        return {"s3://raw_pdf/": filename}

    # TODO (Guillaume): DAG could be generated automatically: a function could inspect
    # the content of the `tasks` package and resolve a DAG based on s3 folder path
    # dependencies.

    # step 0: initiates airflow io to resolve file using the starting task.
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def starting_func():
        return starting_task()

    # step 1: 1st task converting PDF to MD
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def pdf_to_md_func(local_pdf_path: str):
        from automodeling.tasks.pdf_to_md import pdf_to_md_task
        return pdf_to_md_task(local_pdf_path)


    # step 2: 2 tasks in parallel using previously generated MD
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def md_to_ontology_func(md_local_path: str):
        from automodeling.tasks.pdf_to_md import md_to_ontology_task
        return md_to_ontology_task(md_local_path)
    
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def md_to_scenarios_func(md_local_path:str):
        from automodeling.tasks.pdf_to_md import md_to_scenarios_task
        return md_to_scenarios_task(md_local_path)

    # step 3: Final tasks using both outputs of previous tasks
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def all_to_graph_func(ontology_local_path: str, scenarios_local_path: str):
        from automodeling.tasks.pdf_to_md import all_to_graph_task
        return all_to_graph_task(ontology_local_path, scenarios_local_path)

    # return airflow_io_graph


    airflow_io_pdf = starting_task()

    # step 1: 1st task converting PDF to MD
    airflow_io_md = pdf_to_md_func(airflow_io_pdf)

    # step 2: 2 tasks in parallel using previously generated MD
    airflow_io_ontology = md_to_ontology_func(airflow_io_md)
    airflow_io_scenarios = md_to_scenarios_func(airflow_io_md)

    # step 3: Final tasks using both outputs of previous tasks
    airflow_io_graph = all_to_graph_func(airflow_io_ontology, airflow_io_scenarios)

dag_run=main()