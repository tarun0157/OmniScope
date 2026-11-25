
from agents.ai_tech import run_ai_tech_agent

print("\nStarting OmniScope AI & Technology Test...")

try:
    result = run_ai_tech_agent()

    print("\n========== RESEARCH REPORT ==========\n")
    print(result["report"])

    print("\n========== SOURCES ==========\n")

    for i, source in enumerate(result["sources"], start=1):
        print(f"[{i}] {source['title']}")
        print(source["url"])
        print()

    print("AI & TECHNOLOGY AGENT: SUCCESS")

except Exception as error:
    print("\nAI & TECHNOLOGY AGENT: FAILED")
    print("Error:", str(error))
