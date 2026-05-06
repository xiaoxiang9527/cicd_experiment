from typing import List, Dict, Tuple

class AzureResource:
    def __init__(self, name: str, usage_percent: float, usage: float, limit: float, unit: str, status: str):
        self.name = name
        self.usage_percent = usage_percent
        self.usage = usage
        self.limit = limit
        self.unit = unit
        self.status = status

    def to_dict(self) -> Dict[str, float]:
        return {
            "name": self.name,
            "usage_percent": self.usage_percent,
            "usage": self.usage,
            "limit": self.limit,
            "unit": self.unit,
            "status": self.status
        }

def parse_resource_line(line: str) -> AzureResource:
    parts = line.strip().split("|")
    if len(parts) < 5:
        raise ValueError(f"Invalid resource line format: {line}")
    
    name = parts[0].strip()
    usage_percent = float(parts[1].strip().replace("%", ""))
    usage_limit = parts[2].strip()
    unit = parts[3].strip()
    status = parts[4].strip()
    
    usage_str, limit_str = usage_limit.split("/")
    usage = float(usage_str.strip().replace(",", ""))
    limit = float(limit_str.strip().replace(",", ""))
    
    return AzureResource(name, usage_percent, usage, limit, unit, status)

def analyze_resources(resources: List[AzureResource]) -> Dict[str, float]:
    total_resources = len(resources)
    used_resources = sum(1 for r in resources if r.usage > 0)
    avg_usage = sum(r.usage_percent for r in resources) / total_resources if total_resources > 0 else 0
    
    categorized = {
        "cosmos_db": sum(1 for r in resources if "Cosmos DB" in r.name),
        "storage": sum(1 for r in resources if "Storage" in r.name),
        "vms": sum(1 for r in resources if "Virtual Machines" in r.name),
        "cognitive": sum(1 for r in resources if "Cognitive Services" in r.name),
        "databases": sum(1 for r in resources if "Database for" in r.name),
        "networking": sum(1 for r in resources if "Networking" in r.name),
        "other": 0
    }
    
    categorized["other"] = total_resources - sum(categorized.values())
    
    return {
        "total_resources": total_resources,
        "used_resources": used_resources,
        "unused_resources": total_resources - used_resources,
        "avg_usage_percent": round(avg_usage, 2),
        "categories": categorized
    }

def get_top_unused(resources: List[AzureResource], limit: int = 5) -> List[Tuple[str, float]]:
    unused = [(r.name, r.limit) for r in resources if r.usage == 0]
    unused.sort(key=lambda x: x[1], reverse=True)
    return unused[:limit]

def format_report(analysis: Dict[str, float]) -> str:
    report = []
    report.append("=" * 60)
    report.append("Azure Resource Usage Report")
    report.append("=" * 60)
    report.append(f"Total Resources: {analysis['total_resources']}")
    report.append(f"Used Resources: {analysis['used_resources']}")
    report.append(f"Unused Resources: {analysis['unused_resources']}")
    report.append(f"Average Usage: {analysis['avg_usage_percent']}%")
    report.append("-" * 60)
    report.append("Resource Categories:")
    
    categories = analysis['categories']
    for cat, count in categories.items():
        if count > 0:
            report.append(f"  {cat.replace('_', ' ').title()}: {count}")
    
    report.append("=" * 60)
    return "\n".join(report)