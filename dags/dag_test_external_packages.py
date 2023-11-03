import llama_index
import flake8
import langchain
from airflow.decorators import dag, task
from airflow.models.param import Param
import pendulum
from dotenv import load_dotenv
import os

load_dotenv()

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
        from langchain.chat_models import AzureChatOpenAI

        llm = AzureChatOpenAI(
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            openai_api_version=os.getenv("OPENAI_API_VERSION"),
            deployment_name="PDFtoCCwithOpenAI",
            openai_api_key=os.getenv("AZURE_OPEN_AI_KEY"),
            openai_api_type=os.getenv("OPENAI_API_TYPE"),
        )

        from langfuse.callback import CallbackHandler

        handler = CallbackHandler(
            public_key=os.getenv("ENV_PUBLIC_KEY"),
            secret_key=os.getenv("ENV_SECRET_KEY"),
            host=os.getenv("ENV_HOST"),
        )

        from langchain.chains import LLMChain
        from langchain.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
        chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

        joke = chain.invoke({"topic": "an elephant and a flying saucer"})
        print(joke)
        
main()
