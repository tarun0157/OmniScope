
from agents.base_agent import run_agent


def run_geopolitics_agent():

    domain = "Geopolitics"

    queries = [
        "Latest international geopolitical developments",
        "Recent international conflicts and diplomatic relations",
        "Latest international sanctions treaties and agreements"
    ]

    instructions = """
    Focus on:
    1. International conflicts and their developments.
    2. Diplomatic relations between countries.
    3. International sanctions and treaties.
    4. Government and foreign policy decisions.
    5. Statements from important international organizations.

    Clearly distinguish confirmed developments from political claims.
    Include different country perspectives wherever available.
    """

    return run_agent(
        domain=domain,
        queries=queries,
        instructions=instructions
    )
