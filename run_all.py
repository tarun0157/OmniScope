
from agents.geopolitics import run_geopolitics_agent
from agents.ai_tech import run_ai_tech_agent
from agents.economy import run_economy_agent

from db import initialize_database, save_report
from coordinator import run_coordinator


def main():

    print("\n========== OMNISCOPE STARTED ==========\n")

    initialize_database()

    agents = [
        ("Geopolitics", run_geopolitics_agent),
        ("AI and Technology", run_ai_tech_agent),
        ("Global Economy and Business", run_economy_agent)
    ]

    for domain, agent_function in agents:

        print(f"\nRunning {domain} Agent...")

        try:
            result = agent_function()

            save_report(
                domain=result["domain"],
                report=result["report"],
                sources=result["sources"],
                status="success"
            )

            print(f"{domain}: SUCCESS - Report saved!")

        except Exception as error:

            print(f"{domain}: FAILED")
            print("Error:", str(error))

    print("\n========== STARTING COORDINATOR ==========\n")

    try:
        briefing = run_coordinator()

        print("\n========== FINAL BRIEFING ==========\n")
        print(briefing)

        print("\nOMNISCOPE: SUCCESS")

    except Exception as error:

        print("\nCOORDINATOR FAILED")
        print("Error:", str(error))


if __name__ == "__main__":
    main()
