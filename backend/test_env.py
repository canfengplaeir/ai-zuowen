import os
from dotenv import load_dotenv

load_dotenv()

def test_env():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"API Key: {'Set' if api_key else 'Not Set'}")
    print(f"Base URL: {'Set' if base_url else 'Not Set'}")

if __name__ == "__main__":
    test_env() 