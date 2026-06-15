from rag.retriever import retrieve

def retrieve_relevant_chunks(query: str):
    """
    Retrieve relevant chunks for a given query using the RAG retriever.

    Args:
        query (str): The query string for which to retrieve relevant chunks.

    Returns:
        list: A list of dictionaries containing the retrieved chunks and their metadata.
    """
    return retrieve(query)