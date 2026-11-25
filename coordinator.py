
import os
from dotenv import load_dotenv
from openai import OpenAI

from db import get_latest_reports, save_briefing

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL")


def run_coordinator():

    print("\nStarting OmniScope Coordinator...")

    # Step 1: Get reports from the database
    all_reports = get_latest_reports()

    required_domains = [
        "Geopolitics",
        "AI and Technology",
        "Global Economy and Business"
    ]

    # Keep only the latest successful report for each domain
    latest_by_domain = {}

    for report in all_reports:
        domain = report["domain"]

        if (
            domain in required_domains
            and report["status"] == "success"
            and domain not in latest_by_domain
        ):
            latest_by_domain[domain] = report

    # Step 2: Prepare available reports
    research_data = ""

    for domain in required_domains:

        if domain in latest_by_domain:
            report = latest_by_domain[domain]

            research_data += f"""
DOMAIN: {domain}

REPORT:
{report['report']}

SOURCES:
{report['sources']}

"""

        else:
            research_data += f"""
DOMAIN: {domain}
STATUS: No successful report available.
"""

    if not latest_by_domain:
        raise RuntimeError("No successful agent reports found.")

    # Step 3: Prepare coordinator instructions
    prompt = f"""
You are the Coordinator Agent of OmniScope.

Your task is to combine the supplied specialist research reports
into one evidence-based intelligence briefing.

IMPORTANT RULES:

1. Use ONLY the supplied agent reports.
2. Do not introduce new facts or external information.
3. Preserve source numbers and URLs.
4. Do not hide disagreements between reports.
5. Clearly distinguish facts from claims.
6. Mention missing agent reports honestly.
7. Never invent connections between unrelated events.
8. Use a neutral and clear tone.

Prepare the briefing using these sections:

1. DAILY BRIEFING - TOP 5
Five important developments supported by the reports.

2. WHERE REPORTS AGREE
Points supported by multiple reports, if any.

3. CONFLICTS / CONTRADICTIONS
Different or conflicting information, if any.

4. CROSS-DOMAIN LINKS
Connections between geopolitics, technology and economy,
only when supported by the supplied reports.

5. AGENT STATUS
Mention which agents provided reports and which were missing.

6. WATCH NEXT
List 2-3 developments worth monitoring, only when supported
by the reports.

AGENT REPORTS:
{research_data}
"""

    # Step 4: Ask Nemotron to create the briefing
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
        max_tokens=2500
    )

    briefing = response.choices[0].message.content

    # Step 5: Save final briefing in SQLite
    save_briefing(briefing)

    print("\nCoordinator briefing generated and saved!")

    return briefing
