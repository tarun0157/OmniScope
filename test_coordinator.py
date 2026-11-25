
from coordinator import run_coordinator

print("\n========== OMNISCOPE COORDINATOR TEST ==========")

try:
    briefing = run_coordinator()

    print("\n========== FINAL INTELLIGENCE BRIEFING ==========\n")
    print(briefing)

    print("\nCOORDINATOR TEST: SUCCESS")

except Exception as error:
    print("\nCOORDINATOR TEST: FAILED")
    print("Error:", str(error))
