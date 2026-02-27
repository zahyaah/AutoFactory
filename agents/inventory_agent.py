import os
import json
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

INVENTORY_DATA_PATH = (Path(__file__).resolve().parent.parent / "json-data" / "inventory_data.json")

def get_inventory_data(target_date):
    """
    Fetches inventory data. Note: In a real scenario, you'd query 
    stock levels as they were on target_date.
    """
    _ = target_date  # kept for signature consistency with other agents
    rows = _load_inventory_rows()

    materials = []
    for row in rows:
        materials.append(
            {
                "material_name": row.get("material_name"),
                "current_stock": int(row.get("current_stock", 0) or 0),
                "reorder_level": int(row.get("reorder_level", 0) or 0),
            }
        )

    return materials

@lru_cache(maxsize=1)
def _load_inventory_rows():
    """
    Loads inventory rows from json-data/inventory_data.json.
    Cached to avoid re-reading the file on repeated calls.
    """
    with open(INVENTORY_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {INVENTORY_DATA_PATH}, got {type(data).__name__}")
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
# Inventory Agent
# -------------------------

inventory_agent = AssistantAgent(
    name="InventoryAgent",
    model_client=model_client,
    system_message="""
You are an Inventory Monitoring Agent.

You will receive a list of materials with current_stock and reorder_level.

Respond strictly in JSON format:
{
  "low_stock_materials": ["name1", "name2"],
  "status": "Normal | Warning | Critical",
  "recommendation": "..."
}

Rules:
- If current_stock < (0.5 * reorder_level) for any item → Critical
- Else if current_stock < reorder_level for any item → Warning
- Else → Normal
"""
)