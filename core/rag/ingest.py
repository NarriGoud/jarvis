import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONFIGURATION ---
DB_PATH = "D:/Kelly-1.0.0/jarvis/data/chroma_db"
# Use a lightweight, high-performance embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_folder(folder_path):
    """Vectorizes Python, PDF, HTML, CSS, and JS files with UTF-8 support."""
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    print(f"🔍 Scanning: {folder_path}...")
    
    # 1. Define loaders for different file types
    # We use a list of extensions for web files
    web_extensions = ["*.html", "*.css", "*.js"]
    
    docs = []
    
    # Load PDFs
    pdf_loader = DirectoryLoader(folder_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    
    # Load Python files with UTF-8 encoding
    code_loader = DirectoryLoader(
        folder_path, 
        glob="./*.py", 
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        silent_errors=True
    )
    
    docs.extend(pdf_loader.load())
    docs.extend(code_loader.load())
    
    # Load Web Files (.html, .css, .js)
    for ext in web_extensions:
        web_loader = DirectoryLoader(
            folder_path, 
            glob=f"./{ext}", 
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'},
            silent_errors=True
        )
        docs.extend(web_loader.load())
    
    if not docs:
        print(f"⚠️ No relevant files found in {folder_path}")
        return

    # 2. Specialized Splitters
    # These ensure Jarvis understands the 'context' of specific languages
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=100
    )
    js_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=1000, chunk_overlap=100
    )
    html_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=1000, chunk_overlap=100
    )
    # Default splitter for CSS and PDFs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    chunks = []
    for doc in docs:
        source = doc.metadata.get('source', '').lower()
        
        if source.endswith('.py'):
            chunks.extend(python_splitter.split_documents([doc]))
        elif source.endswith('.js'):
            chunks.extend(js_splitter.split_documents([doc]))
        elif source.endswith('.html'):
            chunks.extend(html_splitter.split_documents([doc]))
        else:
            # Covers .css and .pdf
            chunks.extend(text_splitter.split_documents([doc]))

    # 3. Add to the existing ChromaDB
    try:
        # persist_directory creates the DB if it doesn't exist, or loads it if it does
        vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        vector_db.add_documents(chunks)
        print(f"✅ Successfully vectorized {len(chunks)} chunks (Full-Stack) from {folder_path}")
    except Exception as e:
        print(f"❌ Failed to save to ChromaDB: {e}")

if __name__ == "__main__":
    # Your specific MarketMind project paths
    folders_to_learn = [
        rf"D:\MarketMind\github_website",
        rf"D:\MarketMind\marketmind-inference",
        rf"D:\MarketMind\website_backend_render",
        rf"D:\MarketMind\HUB",
        rf"D:\MarketMind\marketmind_hub_backend",
        rf"D:\MarketMind\MarketMind_Main_Backend"
    ]

    for path in folders_to_learn:
        ingest_folder(path)
    
    print("\n🚀 All projects have been successfully synchronized with Jarvis's memory.")