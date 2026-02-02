import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Absolute path to ensure reliability across your environment
DB_PATH = "D:/Kelly-1.0.0/jarvis/data/chroma_db"

# Initialize embeddings (keeping it consistent with ingest.py)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def query_knowledge_base(query: str):
    """Searches the Vector DB for semantic matches in MarketMind & TownLink projects."""
    
    if not os.path.exists(DB_PATH):
        return "System Error: Knowledge database not found at the specified path, sir."

    try:
        # Load the existing database
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        
        # We use similarity_search_with_relevance_scores to filter out bad matches
        # k=5 gives a broader context for complex code logic
        results = db.similarity_search_with_relevance_scores(query, k=5)
        
        # Filter: Only keep results with a decent confidence score (e.g., > 0.3)
        relevant_results = [res for res, score in results if score > 0.3]
        
        if not relevant_results:
            return "I have searched my long-term memory, but I couldn't find a high-confidence match for that query, sir."

        # Prepare the context with source metadata so Jarvis knows which file he is reading
        context_blocks = []
        for res in relevant_results:
            source_file = res.metadata.get('source', 'Unknown Source')
            block = f"[Source: {source_file}]\n{res.page_content}"
            context_blocks.append(block)

        context = "\n\n---\n\n".join(context_blocks)
        return f"INTERNAL KNOWLEDGE RETRIEVED:\n{context}"

    except Exception as e:
        return f"Error accessing knowledge base: {str(e)}"