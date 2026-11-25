
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI

load_dotenv()

# Load API credentials
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL")


def run_agent(domain, queries, instructions):
    """
    Reusable research engine for all OmniScope agents.

    domain: Research category
    queries: List of search queries
    instructions: Special instructions for the agent
    """

    print(f"\nStarting research: {domain}")

    # Step 1: Search the web using Tavily
    tavily = TavilyClient(api_key=TAVILY_API_KEY)

    all_results = []
    seen_urls = set()

    for query in queries:
        print(f"Searching: {query}")

        response = tavily.search(
            query=query,
            max_results=4
        )

        for result in response["results"]:
            url = result["url"]

            if url not in seen_urls:
                seen_urls.add(url)
                all_results.append(result)

            if len(all_results) >= 8:
                break

        if len(all_results) >= 8:
            break

    if not all_results:
        raise RuntimeError("No search results found.")

    # Step 2: Prepare numbered sources
    research_data = ""

    for i, result in enumerate(all_results, start=1):
        research_data += f"""
SOURCE [{i}]
Title: {result['title']}
URL: {result['url']}
Content: {result['content']}

"""

    # Step 3: Prepare instructions for Nemotron
    prompt = f"""
You are an evidence-based research analyst for OmniScope.

Research Domain: {domain}

Special Instructions:
{instructions}

Use ONLY the supplied search results.

Rules:
1. Add source numbers like [1] after factual statements.
2. Separate information supported by multiple sources from single-source claims.
3. Identify different perspectives and disagreements.
4. Do not invent facts or sources.
5. If information is unclear, say "Not enough information".
6. Use a neutral and clear tone.

Prepare the report in this format:

1. Summary (3-4 lines)
2. Key Developments (5 bullet points)
3. Facts vs Claims
4. Different Perspectives
5. What Is Unclear
6. Sources (title and URL)
7. Confidence (Low/Medium/High with reason)

SEARCH RESULTS:
{research_data}
"""

    # Step 4: Send research to Nemotron
    client = OpenAI(
        api_key=NVIDIA_API_KEY,
        base_url=NVIDIA_BASE_URL
    )

    response = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1800
    )

    report = response.choices[0].message.content

    # Step 5: Return report and original sources
    sources = [
        {
            "title": result["title"],
            "url": result["url"]
        }
        for result in all_results
    ]

    print(f"Research completed: {domain}")

    return {
        "domain": domain,
        "report": report,
        "sources": sources
    }
