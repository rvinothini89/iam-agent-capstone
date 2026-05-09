from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def get_relevant_docs(query):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("rag/faiss_index", embeddings, allow_dangerous_deserialization=True)

    results = db.similarity_search(query, k=3)
    return [doc.page_content for doc in results]
