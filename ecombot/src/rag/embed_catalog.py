from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import litellm
import os
import chromadb
from datetime import datetime

load_dotenv()

EMBEDDING_MODEL = "openrouter/openai/text-embedding-3-small"
COLLECTION_NAME = "ecombot_catalog"

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

for filename in os.listdir(os.getenv("DATA_FOLDER_PATH")):
    if filename.endswith(".pdf"):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : Processing file: {filename}")
        # Load the PDF file
        loader = PyPDFLoader(os.path.join(os.getenv("DATA_FOLDER_PATH"), filename))
        documents = loader.load()

        # Initialize the splitter with chunk size and overlap
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        # Create the chunks
        chunks = splitter.split_documents(documents)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : Total chunks created: {len(chunks)}")

        # Generate embeddings for each chunk and store them in ChromaDB
        for i, chunk in enumerate(chunks):
            # Generate an embedding for the chunk
            embedding = embed(chunk.page_content)
            metadata= chunk.metadata  # You can include any relevant metadata from the chunk, such as page number, source, etc.

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG : {filename.replace('.pdf', '')}_chunk_{i}")
            #print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG : metadata : {metadata}")
            
            # Add the chunk and its embedding to the ChromaDB collection
            collection.add(
                documents=[chunk.page_content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[f"{filename.replace('.pdf', '')}_chunk_{i}"]  # Unique ID for each chunk
            )
