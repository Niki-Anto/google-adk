import os
import litellm
import chromadb
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
EMBEDDING_MODEL = "openrouter/openai/text-embedding-3-small"
COLLECTION_NAME = "ecombot_catalog"
TOP_K = 5

#Initialize the ChromaDB client
chroma_client = chromadb.PersistentClient(path=os.getenv("VECTOR_DB_PATH"))
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# Function to generate embeddings using the LiteLlm model
def embed(texts: str):
    response = litellm.embedding(
        model=EMBEDDING_MODEL,
        input=texts,
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    return response['data'][0]['embedding']

def retrieve(query: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : Retrieving relevant chunks for the query: {query}")
    query_embedding = embed(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas"]
    )
    retrieved_chunks = []
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]): # bundle the retrieved documents and their metadata together
        retrieved_chunks.append({"text": doc, "metadata": metadata}) 
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : Retrieved {len(retrieved_chunks)} relevant chunks.")
    return retrieved_chunks

#if __name__ == "__main__":
#    user_query = "Benefits of Offer by OPPO Mobiles"
#    retrieved_chunks = retrieve(user_query)
#    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : Retrieved Chunks: {retrieved_chunks}")



















