from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)


# ── NEW: Import your Docker API tools ──
from tools.docker_api_tools import (
    fhir_explore_patient,
    summarize_with_ollama,
    summarize_with_azure,
    analyze_medical_image
)

root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    # ── NEW: Give your agent healthcare superpowers! ──
    tools=[
        fhir_explore_patient,
        summarize_with_ollama,
        summarize_with_azure,
        analyze_medical_image
    ]
)
