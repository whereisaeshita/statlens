import json
from pathlib import Path
from typing import Any, Dict, List, Union
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def display_profile(column_name: str, profile: Dict[str, Any]) -> None:
    table = Table(title=f"Statistical Profile: {column_name}", header_style="bold cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Sample Count", str(profile["count"]))
    table.add_row("Minimum", str(profile["min"]))
    table.add_row("Maximum", str(profile["max"]))
    table.add_row("Range", str(profile["range"]))
    table.add_row("Mean (Average)", str(profile["mean"]))
    table.add_row("Median (50th %)", str(profile["median"]))
    table.add_row("Variance", str(profile["variance"]))
    table.add_row("Standard Deviation", str(profile["std_dev"]))
    table.add_row("Q1 (25th Percentile)", str(profile["q1"]))
    table.add_row("Q3 (75th Percentile)", str(profile["q3"]))
    table.add_row("IQR (Q3 - Q1)", str(profile["iqr"]))
    table.add_row("Skewness", str(profile["skewness"]))

    console.print(table)

    iqr_outliers = profile.get("iqr_outliers", [])
    z_outliers = profile.get("zscore_outliers", [])

    outlier_text = []
    if iqr_outliers:
        outlier_text.append(f"[bold red]IQR Outliers (1.5x rule):[/bold red] {iqr_outliers}")
    else:
        outlier_text.append("[green]No IQR outliers detected.[/green]")

    if z_outliers:
        outlier_text.append(f"[bold red]Z-Score Outliers (|z| >= 2.5):[/bold red] {z_outliers}")
    else:
        outlier_text.append("[green]No Z-Score outliers detected.[/green]")

    console.print(Panel("\n".join(outlier_text), title="Anomaly & Outlier Analysis", border_style="yellow"))


def export_profiles_json(profiles: Dict[str, Dict[str, Any]], output_path: Union[str, Path]) -> None:
    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)

