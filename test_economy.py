
from agents.economy import run_economy_agent

print("\nStarting OmniScope Economy Test...")

try:
    result = run_economy_agent()

    print("\n========== RESEARCH REPORT ==========\n")
    print(result["report"])

    print("\n========== SOURCES ==========\n")

    for i, source in enumerate(result["sources"], start=1):
        print(f"[{i}] {source['title']}")
        print(source["url"])
        print()

    print("ECONOMY AGENT: SUCCESS")

except Exception as error:
    print("\nECONOMY AGENT: FAILED")
    print("Error:", str(error))
