import argparse
import sys
from pathlib import Path
from typing import Dict, List

from .reader import parse_numeric_string, read_csv_columns
from .reporter import console, display_profile, export_profiles_json
from .stats import calculate_profile


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="profiler",
        description="A statistical data profiler and outlier detection utility.",
    )
    parser.add_argument("file", nargs="?", default=None, help="Path to input CSV file")
    parser.add_argument("-d", "--data", type=str, default=None, help="Comma-separated numbers directly from command line")
    parser.add_argument("-c", "--column", type=str, default=None, help="Specific column to analyze")
    parser.add_argument("-o", "--output", type=str, default=None, help="Export results to a JSON file")
    return parser


def main(args: list = None) -> int:
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    datasets: Dict[str, List[float]] = {}

    if parsed_args.data:
        nums = parse_numeric_string(parsed_args.data)
        if not nums:
            console.print("[bold red]Error:[/bold red] No valid numbers found in the provided input.")
            return 1
        datasets["Manual Input"] = nums

    elif parsed_args.file:
        file_path = Path(parsed_args.file)
        if not file_path.exists():
            console.print(f"[bold red]Error:[/bold red] File '{parsed_args.file}' not found.")
            return 1
        try:
            columns = read_csv_columns(file_path)
            if not columns:
                console.print("[bold red]Error:[/bold red] No numeric data found in CSV file.")
                return 1
            if parsed_args.column:
                if parsed_args.column not in columns:
                    console.print(f"[bold red]Error:[/bold red] Column '{parsed_args.column}' not found.")
                    return 1
                datasets[parsed_args.column] = columns[parsed_args.column]
            else:
                datasets = columns
        except Exception as exc:
            console.print(f"[bold red]Failed to read CSV:[/bold red] {exc}")
            return 1

    else:
        sample_path = Path(__file__).parent / "sample_data.csv"
        if sample_path.exists():
            console.print(f"[cyan]No input provided. Profiling default sample dataset: '{sample_path.name}'[/cyan]\n")
            datasets = read_csv_columns(sample_path)
        else:
            parser.print_help()
            return 0

    profiles = {}
    for col_name, values in datasets.items():
        if len(values) < 2:
            console.print(f"[dim]Skipping '{col_name}': insufficient data points (minimum 2 needed).[/dim]")
            continue
        profile = calculate_profile(values)
        profiles[col_name] = profile
        display_profile(col_name, profile)
        console.print("")

    if parsed_args.output and profiles:
        export_profiles_json(profiles, parsed_args.output)
        console.print(f"[bold green]✓[/bold green] Profiles exported successfully to '{parsed_args.output}'.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

