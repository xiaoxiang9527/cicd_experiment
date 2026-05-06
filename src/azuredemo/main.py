#!/usr/bin/env python3
import argparse
import sys
from azuredemo.utils import (
    parse_resource_line,
    analyze_resources,
    format_report,
    get_top_unused,
    AzureResource
)

def load_sample_data() -> list:
    sample_data = [
        "Azure Cosmos DB, Free Data Stored|0%|0 / 25|1 GB/Month|非使用中",
        "Azure Cosmos DB, Free 100 RU/s|0%|0 / 2976|1/Hour|非使用中",
        "Storage, Files, LRS Data Stored|0%|0 / 100|1 GB/Month|非使用中",
        "Storage, Premium Page Blob, P6 Disks|0%|0 / 2.2|1/Month|非使用中",
        "Virtual Machines, BS Series, B1s|0%|0 / 750|1 Hour|非使用中",
        "Virtual Machines, BS Series Windows, B1s|0%|0 / 750|1 Hour|非使用中",
        "Networking, Data Transfer Out (GB)|0%|0 / 15|1 GB|非使用中",
        "SQL Database, Single Standard, S0 DTUs|0%|0 / 31|1/Day|非使用中",
        "Cognitive Services, Custom Vision, S0 Transactions|0%|0 / 10|1K|非使用中",
        "Cognitive Services, Computer Vision, S1 Transactions|0%|0 / 5|1K|非使用中",
    ]
    return sample_data

def main():
    parser = argparse.ArgumentParser(
        prog='azuredemo',
        description='Azure Resource Usage Analyzer - Analyze Azure free tier resource usage'
    )
    parser.add_argument(
        '-f', '--file',
        help='Path to resource data file (default: use sample data)'
    )
    parser.add_argument(
        '-t', '--top-unused',
        type=int,
        default=5,
        help='Number of top unused resources to show'
    )
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = load_sample_data()

        resources = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                resources.append(parse_resource_line(line))

        analysis = analyze_resources(resources)
        print(format_report(analysis))

        top_unused = get_top_unused(resources, args.top_unused)
        if top_unused:
            print("\nTop Unused Resources by Limit:")
            for i, (name, limit) in enumerate(top_unused, 1):
                print(f"{i}. {name}: {limit}")

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())