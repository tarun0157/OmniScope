
from agents.geopolitics import run_geopolitics_agent

print("\nStarting OmniScope Geopolitics Test...")

try:
    result = run_geopolitics_agent()

    print("\n========== RESEARCH REPORT ==========\n")
    print(result["report"])

    print("\n========== SOURCES ==========\n")

    for i, source in enumerate(result["sources"], start=1):
        print(f"[{i}] {source['title']}")
        print(source["url"])
        print()

    print("GEOPOLITICS AGENT: SUCCESS")

except Exception as error:
    print("\nGEOPOLITICS AGENT: FAILED")
    print("Error:", str(error))
