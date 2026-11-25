
from agents.base_agent import run_agent


def run_ai_tech_agent():

    domain = "AI and Technology"

    queries = [
        "Latest artificial intelligence news and developments",
        "Latest AI model releases and technology research breakthroughs",
        "Latest semiconductor chips and hardware industry news",
        "Global technology regulations and major tech company developments"
    ]

    instructions = """
    Focus on:
    1. New AI models and their capabilities.
    2. AI research and scientific breakthroughs.
    3. Semiconductor chips and computing hardware.
    4. Technology developments by major companies.
    5. AI regulations and government policies.
    6. Important innovations in global technology.

    Distinguish product announcements from independently
    verified research findings.
    Include publication dates wherever available.
    """

    return run_agent(
        domain=domain,
        queries=queries,
        instructions=instructions
    )
