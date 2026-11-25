
import streamlit as st

import smtplib
import ssl
from email.message import EmailMessage

from db import get_latest_reports, get_latest_briefing, initialize_database
from run_all import main


# Page configuration
st.set_page_config(
    page_title="OmniScope",
    page_icon="🌐",
    layout="wide"
)

initialize_database()
def send_briefing_email(briefing):
    msg = EmailMessage()

    sender = st.secrets["SMTP_EMAIL"]
    receiver = st.secrets["RECEIVER_EMAIL"]

    msg["Subject"] = "OmniScope Intelligence Briefing"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(briefing)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=context
    ) as server:
        server.login(
            sender,
            st.secrets["SMTP_APP_PASSWORD"]
        )
        server.send_message(msg)

# Dashboard heading
st.title("🌐 OmniScope")
st.caption("Multi-Agent Research & Intelligence Platform")

st.divider()

# Create four main tabs
briefing_tab, agents_tab, activity_tab, about_tab = st.tabs([
    "📊 Briefing",
    "🤖 Agents",
    "📜 Activity Log",
    "ℹ️ About"
])


# ==================================
# TAB 1: BRIEFING
# ==================================
with briefing_tab:

    st.header("Daily Intelligence Briefing")

    if st.button("🚀 Run Research Now", type="primary"):

    with st.spinner(
        "Researching... Running all agents and preparing briefing."
    ):
        try:
            main()

            latest_briefing = get_latest_briefing()

            if latest_briefing:
                send_briefing_email(
                    latest_briefing["briefing"]
                )
                st.success(
                    "Research completed and email sent successfully!"
                )
            else:
                st.warning("Research completed, but briefing was not found.")

        except Exception as error:
            st.error(f"Research or email error: {error}")

        st.rerun()

    latest_briefing = get_latest_briefing()

    if latest_briefing:
        st.caption(
            f"Last updated: {latest_briefing['created_at']}"
        )
        st.markdown(latest_briefing["briefing"])
    else:
        st.info(
            "No briefing available yet. Click 'Run Research Now' to begin."
        )


# ==================================
# TAB 2: AGENTS
# ==================================
with agents_tab:

    st.header("Research Agents")



    reports = get_latest_reports()

    domains = [
        "Geopolitics",
        "AI and Technology",
        "Global Economy and Business"
    ]

    agent_tabs = st.tabs([
        "🌍 Geopolitics",
        "💻 AI & Technology",
        "📈 Economy & Business"
    ])

    for agent_tab, domain in zip(agent_tabs, domains):

        with agent_tab:

            domain_reports = [
                report for report in reports
                if report["domain"] == domain
            ]

            if domain_reports:

                latest = domain_reports[0]

                st.subheader(domain)
                st.caption(
                    f"Last updated: {latest['created_at']}"
                )

                st.markdown(latest["report"])

                st.subheader("Sources")

                for i, source in enumerate(
                    latest["sources"], start=1
                ):
                    st.markdown(
                        f"{i}. [{source['title']}]({source['url']})"
                    )

                with st.expander("Report History"):

                    for old_report in domain_reports:
                        st.markdown(
                            f"**Date:** {old_report['created_at']}"
                        )
                        st.markdown(
                            f"**Status:** {old_report['status']}"
                        )
                        st.divider()

            else:
                st.info("No reports available for this agent yet.")


# ==================================
# TAB 3: ACTIVITY LOG
# ==================================
with activity_tab:

    st.header("Research Activity")

    reports = get_latest_reports()

    if reports:

        activity_data = []

        for report in reports:
            activity_data.append({
                "Agent": report["domain"],
                "Date": report["created_at"],
                "Status": report["status"]
            })

        st.dataframe(
            activity_data,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "This table shows saved report activity. "
            "Full pipeline run tracking will be added separately."
        )

    else:
        st.info("No research activity recorded yet.")


# ==================================
# TAB 4: ABOUT
# ==================================
with about_tab:

    st.header("About OmniScope")

    st.write("""
    OmniScope is a multi-agent research and intelligence platform.

    It uses specialized AI agents to research different domains
    and a Coordinator Agent to combine their reports into one
    evidence-based briefing.
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - **Python:** Backend
    - **Streamlit:** Web dashboard
    - **NVIDIA Nemotron:** AI analysis
    - **Tavily:** Web research
    - **SQLite:** Report storage
    - **Coordinator:** Combined intelligence briefing
    """)

    st.info(
        "OmniScope aims to provide multi-source balanced "
        "and source-transparent research."
    )
