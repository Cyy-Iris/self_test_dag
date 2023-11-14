from langchain.document_loaders import PyPDFLoader
from utils import (
    remove_pages,
    merge_pages,
    POST_PROCESSING_STEPS,
)


def pdf_to_md(fpath: str) -> str:
    loader = PyPDFLoader(fpath)
    pages = loader.load_and_split()
    pages = remove_pages(pages)
    md = merge_pages(pages)
    for post_processing_step in POST_PROCESSING_STEPS:
        md = post_processing_step(md)

    return md
