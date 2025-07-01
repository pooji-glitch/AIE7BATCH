# Complete setup to avoid NameError
import os
import openai
import asyncio
import nest_asyncio
from aimakerspace.text_utils import TextFileLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase

# Enable async in Jupyter
nest_asyncio.apply()

# API Key setup (using environment variable if available)
if "OPENAI_API_KEY" not in os.environ:
    print("⚠️  OPENAI_API_KEY not found in environment variables.")
    print("Please set your API key using one of these methods:")
    print("1. Run: ./set_api_key.sh")
    print("2. Or in terminal: export OPENAI_API_KEY='your-key-here'")
    print("3. Or manually enter it below:")
    from getpass import getpass
    openai.api_key = getpass("OpenAI API Key: ")
    os.environ["OPENAI_API_KEY"] = openai.api_key
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    print("✅ Using OpenAI API key from environment variable")

# Load and split documents
print("📄 Loading documents...")
text_loader = TextFileLoader("data/PMarcaBlogs.txt")
documents = text_loader.load_documents()
print(f"Loaded {len(documents)} document(s)")

print("✂️  Splitting documents...")
text_splitter = CharacterTextSplitter()
split_documents = text_splitter.split_texts(documents)
print(f"Split into {len(split_documents)} chunks")

# Create vector database
print("🗄️  Creating vector database...")
vector_db = VectorDatabase()
vector_db = asyncio.run(vector_db.abuild_from_list(split_documents))
print("✅ Vector database created successfully!") 