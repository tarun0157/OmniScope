
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI

# Load API credentials from .env
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Check whether required values are present
if not all([NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL, TAVILY_API_KEY]):
    raise ValueError("Missing configuration. Check your .env file.")

# ---------------------------------
# TEST 1: TAVILY SEARCH API
# ---------------------------------
print("\n========== TEST 1: TAVILY ==========")

try:
    tavily = TavilyClient(api_key=TAVILY_API_KEY)

    search_response = tavily.search(
        query="Latest artificial intelligence news",
        max_results=3
    )

    for i, result in enumerate(search_response["results"], start=1):
        print(f"\n{i}. {result['title']}")
        print("URL:", result["url"])
        print("Content:", result["content"][:300])

    print("\nTAVILY TEST: SUCCESS")

except Exception as e:
    search_response = None
    print("\nTAVILY TEST: FAILED")
    print("Error:", str(e))


# ---------------------------------
# TEST 2: NVIDIA NEMOTRON API
# ---------------------------------
print("\n========== TEST 2: NEMOTRON ==========")

try:
    client = OpenAI(
        api_key=NVIDIA_API_KEY,
        base_url=NVIDIA_BASE_URL
    )

    response = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Explain artificial intelligence in 3 simple sentences."
            }
        ],
        temperature=0.2,
        max_tokens=200
    )

    print("\nNemotron Response:")
    print(response.choices[0].message.content)

    print("\nNVIDIA TEST: SUCCESS")

except Exception as e:
    print("\nNVIDIA TEST: FAILED")
    print("Error:", str(e))
