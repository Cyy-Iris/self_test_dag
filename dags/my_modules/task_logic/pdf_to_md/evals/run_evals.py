from dags.my_modules.task_logic.pdf_to_md.evals import eval_page_nr_removed
from dags.my_modules.task_logic.utils.dataset import load_data



def run():
    dataset_page_num = load_data("data/evals/pdf_to_md/page_number")
    eval_page_nr_removed(dataset_page_num)


if __name__ == "__main__":
    run()
