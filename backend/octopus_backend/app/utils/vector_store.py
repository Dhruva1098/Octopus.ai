from langchain_astradb.vectorstores import AstraDBVectorStore as AstraDB
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector_store = AstraDB(
    collection_name="notes",
    embedding=embeddings,
    api_endpoint="https://a60fc762-9900-43a7-aaa0-960d922701c2-us-east1.apps.astra.datastax.com",
    token="AstraCS:YvcuIhMNkEXCCAhpBlcCvMmD:0f87a0072a0aa81ab99f3d7b3a4943243ae12cfac75ec79d0af980d2a41a9d21"
)
