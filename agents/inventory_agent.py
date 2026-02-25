import os
import asyncio
import psycopg2
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

# -------------------------
# Database Query
# -------------------------

def get_inventory_data(target_date):
    """
    Fetches inventory data. Note: In a real scenario, you'd query 
    stock levels as they were on target_date.
    """
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = conn.cursor()
    # While inventory is a snapshot, we fetch it here to keep 
    # the function signature consistent with other agents.
    cursor.execute("""
        SELECT material_name, current_stock, reorder_level
        FROM inventory;
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    materials = [
        {
            "material_name": row[0], 
            "current_stock": row[1], 
            "reorder_level": row[2]
        } for row in rows
    ]

    return materials


# -------------------------
# Azure Model Client
# -------------------------

model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4o-2024-05-13",
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
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