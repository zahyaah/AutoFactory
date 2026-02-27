import os
import json
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

QUALITY_DATA_PATH = (Path(__file__).resolve().parent.parent / "json-data" / "quality_data.json")

def get_quality_data(target_date):
    """
    Fetches quality data for a specific date provided by the orchestrator.
    """
    target_date_str = str(target_date)
    total_defects = 0
    total_units = 0

    for row in _load_quality_rows():
        if str(row.get("date")) != target_date_str:
            continue
        total_defects += int(row.get("defects", 0) or 0)
        total_units += int(row.get("total_units", 0) or 0)

    return {
        "total_defects": total_defects,
        "total_units": total_units
    }

@lru_cache(maxsize=1)
def _load_quality_rows():
    """
    Loads quality rows from json-data/quality_data.json.
    Cached to avoid re-reading the file on repeated calls.
    """
    with open(QUALITY_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {QUALITY_DATA_PATH}, got {type(data).__name__}")
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
# Quality Agent
# -------------------------

quality_agent = AssistantAgent(
    name="QualityAgent",
    model_client=model_client,
    system_message="""
You are a Quality Control Agent.

You will receive:
{
  "total_defects": number,
  "total_units": number
}

Calculate defect rate: (total_defects / total_units) * 100.

Respond strictly in JSON format:
{
  "defect_rate_percentage": number,
  "status": "Normal | Warning | Critical",
  "recommendation": "..."
}

Rules:
- If defect_rate > 5% → Critical
- If defect_rate between 2% and 5% → Warning
- Else → Normal
"""
)