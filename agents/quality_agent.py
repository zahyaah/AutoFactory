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

def get_quality_data(target_date):
    """
    Fetches quality data for a specific date provided by the orchestrator.
    """
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = conn.cursor()
    
    # We replace CURRENT_DATE with %s to accept the date from the orchestrator
    query = """
        SELECT 
            COALESCE(SUM(defects), 0),
            COALESCE(SUM(total_units), 0)
        FROM quality_reports
        WHERE date = %s;
    """
    
    cursor.execute(query, (target_date,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "total_defects": result[0],
        "total_units": result[1]
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