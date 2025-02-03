from langchain_astradb.vectorstores import AstraDBVectorStore as AstraDB
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = AstraDB(
    collection_name="notes",
    embedding=embeddings,
    api_endpoint="-",
    token="-",
    metric="cosine",
)
