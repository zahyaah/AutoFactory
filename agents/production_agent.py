import os
import asyncio
import psycopg2
import json
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent 
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

# -------------------------
# Database Connection
# -------------------------

def get_production_data(target_date):
    """
    Fetches production data for a specific date passed by the Orchestrator.
    """
    conn = psycopg2.connect(
        host="localhost", 
        port=5432,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = conn.cursor()
    # SQL changed from CURRENT_DATE to a parameterized date (%s)
    cursor.execute("""
        SELECT 
            COALESCE(SUM(units_produced), 0),
            COALESCE(SUM(downtime_minutes), 0)
        FROM production_logs
        WHERE date = %s;
    """, (target_date,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "total_units": result[0],
        "total_downtime_minutes": result[1]
    }


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