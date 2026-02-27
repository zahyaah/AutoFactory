import os
import json
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

PRODUCTION_DATA_PATH = (Path(__file__).resolve().parent.parent / "json-data" / "production_data.json")

def get_production_data(target_date):
    """
    Fetches production data for a specific date passed by the Orchestrator.
    """
    target_date_str = str(target_date)
    total_units = 0
    total_downtime_minutes = 0

    for row in _load_production_rows():
        if str(row.get("date")) != target_date_str:
            continue
        total_units += int(row.get("units_produced", 0) or 0)
        total_downtime_minutes += int(row.get("downtime_minutes", 0) or 0)

    return {
        "total_units": total_units,
        "total_downtime_minutes": total_downtime_minutes
    }

@lru_cache(maxsize=1)
def _load_production_rows():
    """
    Loads production rows from json-data/production_data.json.
    Cached to avoid re-reading the file on repeated calls.
    """
    with open(PRODUCTION_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {PRODUCTION_DATA_PATH}, got {type(data).__name__}")
    return data


# -------------------------
# Azure Model Client
# -------------------------

model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4o-2024-05-13",
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)


# -------------------------
# Production Agent
# -------------------------

production_agent = AssistantAgent(
    name="ProductionAgent",
    model_client=model_client,
    system_message="""
You are a Production Monitoring Agent in a manufacturing plant.

You will receive production statistics as JSON:
{
  "total_units": number,
  "total_downtime_minutes": number
}

Respond strictly in structured JSON format:

{
  "summary": "...",
  "status": "Normal | Warning | Critical",
  "recommendation": "..."
}

Rules:
- If downtime > 120 minutes → Critical
- If downtime between 60 and 120 → Warning
- Else → Normal
"""
)