import langchain
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
import llama_index
import flake8
from airflow.decorators import dag, task
from airflow.models.param import Param

@dag(
    dag_id="External-python-packages",
    schedule=None,
    start_date=pendulum.datetime(2023, 10,31, tz="UTC"),
    catchup=False,
    tags=["k8s_python"],
)
def main():
    @task()
    def test_package():
        print("Successful!")
        
main()
