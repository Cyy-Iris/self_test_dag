"""Main Automodeling Airflow DAG.

This module contains the main apache airflow DAG taking as input parameter a PDF path of
a file in S3 and outputting a graph representation of that PDF. Each task in the DAG
write its intermediary results to S3 and share dependencies with the following one.

It exposes:
    * :DAG:main: actual apache airflow DAG.
"""
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
    dag_id="Guillaume_code_test",
    schedule=None,
    start_date=pendulum.datetime(2023, 10, 30, tz="UTC"),
    catchup=False,
    tags=["k8b_python"],
    params={"pdf_path": Param("path to a pdf to run the DAG on.")},
)
def main():
    """Main Automodeling pipeline DAG for computable contracts.

    it takes as parameter a full path to a pdf file in s3. If the pdf_path parameter
    provided is only a file it will use the following folder `"s3://raw_pdf/"`.
    """

    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
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

    # step 1: 1st task converting PDF to MD
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def init_io_md():
        from tasks.pdf_to_md import pdf_to_md_task
        pdf_to_md = pdf_to_md_task()
        return pdf_to_md
    

    # step 2: 2 tasks in parallel using previously generated MD
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def init_io_ontology():
        from tasks.md_to_ontology import md_to_ontology_task
        md_to_ontology=md_to_ontology_task()
        return md_to_ontology
    

    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def init_io_scenarios():
        from tasks.md_to_scenarios import md_to_scenarios_task
        md_to_scenarios=md_to_scenarios_task()
        return md_to_scenarios
    

    # step 3: Final tasks using both outputs of previous tasks
    @task.kubernetes(image="python-guillaume:0.0.1", namespace="airflow", in_cluster=True)
    def init_io_all_graph():
        from tasks.all_to_graph import all_to_graph_task
        all_to_graph=all_to_graph_task()
        return all_to_graph
    
    airflow_io_pdf = starting_task()
    airflow_io_md = init_io_md(airflow_io_pdf)
    airflow_io_ontology = init_io_ontology(airflow_io_md)
    airflow_io_scenarios = init_io_scenarios(airflow_io_md)
    airflow_io_graph = init_io_all_graph(airflow_io_ontology, airflow_io_scenarios)

    # return airflow_io_graph
main()
