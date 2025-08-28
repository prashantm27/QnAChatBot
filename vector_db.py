from uuid import uuid4
import os
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter

from utils import util

from dotenv import load_dotenv
load_dotenv()

azure_embedding_deployment = os.getenv("AZURE_EMBED_MODEL")
embeddings = AzureOpenAIEmbeddings(azure_deployment=azure_embedding_deployment)

vector_store = Chroma(
    collection_name="performance_report",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

def _prepare_document(markdown_document):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    md_header_splits = markdown_splitter.split_text(markdown_document)
    return md_header_splits

def _update_source_metadata(documents, filename):
    for doc in documents:
        doc.metadata['source'] = filename
    return documents


def _add_documents_db(documents, filename):
    try:
        uuids = [str(uuid4()) for _ in range(len(documents))]
        documents = _update_source_metadata(documents, filename)
        vector_store.add_documents(documents=documents, ids=uuids)
        return True
    except Exception as e:
        print(f'** {e} **')
        return False
    
def store_to_vector(save_path, filename):
    text = util.extract_text(save_path) 
    prepared_document = _prepare_document(text)
    is_success = _add_documents_db(prepared_document, filename)
    return is_success

def _query_vector_db(query, source):
    results = vector_store.similarity_search(
        query,
        k=5,
        filter={'source':source}
    )
    return results

def match_context(query, source):
    results = _query_vector_db(query, source)
    context = ''
    for result in results:
        context += f'** {result.page_content} **\n'
    return context
