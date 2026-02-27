import asyncio
import json
import random
from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.theme import Theme
from dotenv import load_dotenv

load_dotenv()

# Import your agents/functions
from production_agent import production_agent, get_production_data
from inventory_agent import inventory_agent, get_inventory_data
from quality_agent import quality_agent, get_quality_data

JSON_DATA_DIR = (Path(__file__).resolve().parent.parent / "json-data")
QUALITY_DATA_PATH = JSON_DATA_DIR / "quality_data.json"
PRODUCTION_DATA_PATH = JSON_DATA_DIR / "production_data.json"
INVENTORY_DATA_PATH = JSON_DATA_DIR / "inventory_data.json"

class FactoryReport(BaseModel):
    simulated_date: str
    production: str
    inventory: str
    quality: str

def get_shared_simulated_date():
    """Pick one random date from the dataset to sync all agents."""
    start_date = "2026-01-01"
    end_date = "2026-01-31"

    quality_dates = {
        str(row.get("date"))
        for row in _load_quality_rows()
        if start_date <= str(row.get("date")) <= end_date
    }
    production_dates = {
        str(row.get("date"))
        for row in _load_production_rows()
        if start_date <= str(row.get("date")) <= end_date
    }

    # Inventory is a snapshot (no date in dataset) but we still load it
    # so we're utilizing all json-data sources consistently.
    _ = _load_inventory_rows()

    shared_dates = sorted(quality_dates & production_dates)
    if not shared_dates:
        shared_dates = sorted(quality_dates or production_dates)
    if not shared_dates:
        raise ValueError("No simulated dates found in json-data datasets.")

    return random.choice(shared_dates)

@lru_cache(maxsize=1)
def _load_quality_rows():
    with open(QUALITY_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {QUALITY_DATA_PATH}, got {type(data).__name__}")
    return data

@lru_cache(maxsize=1)
def _load_production_rows():
    with open(PRODUCTION_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {PRODUCTION_DATA_PATH}, got {type(data).__name__}")
    return data

@lru_cache(maxsize=1)
def _load_inventory_rows():
    with open(INVENTORY_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of rows in {INVENTORY_DATA_PATH}, got {type(data).__name__}")
    return data

async def run_factory_report() -> FactoryReport:
    sim_date = get_shared_simulated_date()

    production_data = get_production_data(sim_date)
    inventory_data = get_inventory_data(sim_date)
    quality_data = get_quality_data(sim_date)

    prod_result = await production_agent.run(task=f"Date: {sim_date}. Data: {json.dumps(production_data)}")
    inv_result = await inventory_agent.run(task=f"Date: {sim_date}. Data: {json.dumps(inventory_data)}")
    qual_result = await quality_agent.run(task=f"Date: {sim_date}. Data: {json.dumps(quality_data)}")

    return FactoryReport(
        simulated_date=sim_date,
        production=prod_result.messages[-1].content,
        inventory=inv_result.messages[-1].content,
        quality=qual_result.messages[-1].content
    )

def display_pretty_report(report: FactoryReport):
    console = Console(theme=Theme({"repr.str": "white"}))
    
    console.print("\n" + "="*70, style="bold cyan")
    console.print(f"🚀 [bold white]AI FACTORY CONTROL CENTER[/bold white] 🚀", justify="center")
    console.print(f"📅 [bold yellow]SIMULATED OPERATIONAL DATE:[/bold yellow] [u]{report.simulated_date}[/u]", justify="center")
    console.print("="*70 + "\n", style="bold cyan")


    prod_panel = Panel(
        report.production, 
        title="[bold green] PRODUCTION STATUS[/bold green]", 
        subtitle=f"Ref: {report.simulated_date}",
        border_style="green", 
        padding=(1, 2)
    )
    
    inv_panel = Panel(
        report.inventory, 
        title="[bold blue] INVENTORY LEVELS[/bold blue]", 
        border_style="blue",
        padding=(1, 2)
    )
    
    qual_panel = Panel(
        report.quality, 
        title="[bold yellow] QUALITY CONTROL[/bold yellow]", 
        border_style="yellow",
        padding=(1, 2)
    )


    console.print(prod_panel)
    console.print(Columns([inv_panel, qual_panel], expand=True))
    
    console.print(f"\n[italic gray70]End of report for {report.simulated_date}. All values synchronized across 3 agents.[/italic gray70]\n")


if __name__ == "__main__":
    print("🚀 Initializing Factory Control Center...")
    try:
        report_data = asyncio.run(run_factory_report())
        display_pretty_report(report_data)
    except Exception as e:
        print(f"❌ Critical System Error: {e}")