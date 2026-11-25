
from agents.base_agent import run_agent


def run_economy_agent():

    domain = "Global Economy and Business"

    queries = [
        "Latest global economic developments and financial news",
        "Latest India economy business and trade news",
        "Latest inflation interest rates and central bank decisions",
        "Latest global markets and major company developments"
    ]

    instructions = """
    Focus on:
    1. Global economic conditions and growth.
    2. India's economy, trade and business environment.
    3. Inflation, interest rates and central bank policies.
    4. Financial markets and major business developments.
    5. International trade and supply chains.
    6. Important company announcements and industry trends.

    Clearly distinguish official economic data from forecasts
    and opinions.
    Include publication dates wherever available.
    """

    return run_agent(
        domain=domain,
        queries=queries,
        instructions=instructions
    )
