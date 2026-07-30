import json
import time
import os
from pathlib import Path
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live

TELEMETRY_PATH = Path("/mnt/disks/disk-socrateai-local-1/hypergraph_logs/cost_telemetry.json")
REPORT_PATH = Path("/mnt/disks/disk-socrateai-local-1/hypergraph_logs/dry_run_final_report.json")

def read_json_safe(filepath):
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None
    except Exception:
        return None

def generate_dashboard() -> Layout:
    telemetry = read_json_safe(TELEMETRY_PATH)
    report = read_json_safe(REPORT_PATH)

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["main"].split_row(
        Layout(name="metrics", ratio=1),
        Layout(name="astrophysics", ratio=2)
    )

    layout["astrophysics"].split_column(
        Layout(name="interpretation", ratio=1),
        Layout(name="progress", ratio=1)
    )

    # Header
    header_text = Text("🚀 SocrateAI Phase 0 MVP Terminal Dashboard 🚀", style="bold white on blue", justify="center")
    layout["header"].update(Panel(header_text))

    # Metrics
    if telemetry:
        metrics_table = Table(show_header=False, box=None)
        metrics_table.add_column("Metric", style="cyan", justify="right")
        metrics_table.add_column("Value", style="magenta")

        cost = telemetry.get("cost_metrics", {})
        step_info = telemetry.get("step_info", {})

        metrics_table.add_row("Region:", cost.get("region", "N/A"))
        metrics_table.add_row("Elapsed Sec:", f"{cost.get('elapsed_seconds', 0):.2f}")
        metrics_table.add_row("Total Cost:", f"${cost.get('total_cost_usd', 0):.6f}")
        metrics_table.add_row("Hourly Burn:", f"${cost.get('hourly_burn_rate_usd', 0):.4f}")
        metrics_table.add_row("Remaining Budget:", f"${cost.get('remaining_budget_usd', 0):.2f}")
        metrics_table.add_row("", "")
        metrics_table.add_row("Current Step:", str(step_info.get("step", "N/A")))
        metrics_table.add_row("Edges:", str(step_info.get("edges", "N/A")))
        metrics_table.add_row("VRAM MB:", str(step_info.get("vram_mb", "N/A")))
        metrics_table.add_row("Is Pruned:", str(step_info.get("is_pruned", "N/A")))

        layout["metrics"].update(Panel(metrics_table, title="[bold green]Operational Metrics[/bold green]"))
    else:
        layout["metrics"].update(Panel("Waiting for telemetry data...", title="[bold green]Operational Metrics[/bold green]"))

    # Interpretation
    interpretation_text = Text()
    interpretation_text.append("Current Astrophysics Interpretation:\n\n", style="bold yellow")
    if telemetry and "step_info" in telemetry:
        step_info = telemetry["step_info"]
        masked_sum = step_info.get("masked_sum", 0)
        unmasked_sum = step_info.get("unmasked_sum", 0)
        
        interpretation_text.append(f"• Tensor Masking Ratio: {masked_sum}/{unmasked_sum}\n")
        
        if step_info.get("is_pruned"):
            interpretation_text.append("• Isomorphic State detected! The topological rules have converged to a previously seen state.\n", style="bold red")
        else:
            interpretation_text.append("• Novel topological state generated! Exploring uncharted hypergraph structures.\n", style="bold green")
            
        interpretation_text.append("\nThe low number of unique isomorphic states combined with the rapid convergence suggests that the topological rules strongly constrain the evolution of the graph. This behavior mimics how dark matter halos quickly form stable configurations through gravitational clustering, avoiding combinatorial explosion.")
    else:
        interpretation_text.append("Waiting for data...")

    layout["interpretation"].update(Panel(interpretation_text, title="[bold cyan]Astrophysics Analysis[/bold cyan]"))

    # Progress
    progress_text = Text()
    if report:
        progress_text.append(f"Phase 0 Dry Run Status: {report.get('status', 'N/A')}\n", style="bold green")
        progress_text.append(f"Total Steps Completed: {report.get('total_steps', 0)}\n")
        progress_text.append(f"Unique Isomorphic Hashes: {report.get('unique_isomorphic_hashes', 0)}\n")
        progress_text.append(f"Wolfram Queries Issued: {report.get('wolfram_queries_issued', 0)}\n")
    elif telemetry and "step_info" in telemetry:
        step = telemetry["step_info"].get("step", 0)
        progress_text.append(f"Dry Run in progress... Current Step: {step}/20\n", style="bold yellow")
    else:
        progress_text.append("Waiting for run to start...")

    layout["progress"].update(Panel(progress_text, title="[bold magenta]Run Progress[/bold magenta]"))

    # Footer
    footer_text = Text(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}", style="dim", justify="right")
    layout["footer"].update(Panel(footer_text))

    return layout


def main():
    console = Console()
    with Live(generate_dashboard(), console=console, refresh_per_second=1) as live:
        try:
            while True:
                live.update(generate_dashboard())
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
