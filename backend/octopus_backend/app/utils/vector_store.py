from langchain_astradb.vectorstores import AstraDBVectorStore as AstraDB
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector_store = AstraDB(
    collection_name="notes",
    embedding=embeddings,
    api_endpoint="-",
    token="-"
)
