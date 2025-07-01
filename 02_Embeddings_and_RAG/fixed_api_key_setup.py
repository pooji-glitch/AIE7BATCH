import os
import openai

# Try to get API key from environment variable first
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