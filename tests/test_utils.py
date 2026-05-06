import pytest
import io
import sys
from azuredemo.utils import (
    AzureResource,
    parse_resource_line,
    analyze_resources,
    get_top_unused,
    format_report
)
from azuredemo.main import main, load_sample_data, parse_resource_line as main_parse

class TestAzureResource:
    def test_resource_creation(self):
        resource = AzureResource(
            name="Test Resource",
            usage_percent=10.5,
            usage=5.0,
            limit=50.0,
            unit="GB",
            status="使用中"
        )
        
        assert resource.name == "Test Resource"
        assert resource.usage_percent == 10.5
        assert resource.usage == 5.0
        assert resource.limit == 50.0
        assert resource.unit == "GB"
        assert resource.status == "使用中"

    def test_resource_to_dict(self):
        resource = AzureResource(
            name="Test Resource",
            usage_percent=10.5,
            usage=5.0,
            limit=50.0,
            unit="GB",
            status="使用中"
        )
        
        result = resource.to_dict()
        assert result["name"] == "Test Resource"
        assert result["usage_percent"] == 10.5
        assert result["usage"] == 5.0
        assert result["limit"] == 50.0
        assert result["unit"] == "GB"
        assert result["status"] == "使用中"

class TestParseResourceLine:
    def test_parse_valid_line(self):
        line = "Azure Cosmos DB, Free Data Stored|0%|0 / 25|1 GB/Month|非使用中"
        resource = parse_resource_line(line)
        
        assert resource.name == "Azure Cosmos DB, Free Data Stored"
        assert resource.usage_percent == 0.0
        assert resource.usage == 0.0
        assert resource.limit == 25.0
        assert resource.unit == "1 GB/Month"
        assert resource.status == "非使用中"

    def test_parse_line_with_commas(self):
        line = "Storage, Files, LRS Data Stored|50%|50 / 100|1 GB/Month|使用中"
        resource = parse_resource_line(line)
        
        assert resource.name == "Storage, Files, LRS Data Stored"
        assert resource.usage_percent == 50.0
        assert resource.usage == 50.0
        assert resource.limit == 100.0

    def test_parse_line_with_large_numbers(self):
        line = "Virtual Machines, BS Series, B1s|10%|75 / 750|1 Hour|使用中"
        resource = parse_resource_line(line)
        
        assert resource.usage == 75.0
        assert resource.limit == 750.0

    def test_parse_invalid_line(self):
        with pytest.raises(ValueError):
            parse_resource_line("Invalid line")

    def test_parse_line_with_percentage(self):
        line = "Test Resource|25.5%|25 / 100|GB|使用中"
        resource = parse_resource_line(line)
        assert resource.usage_percent == 25.5

class TestAnalyzeResources:
    def test_analyze_empty_list(self):
        result = analyze_resources([])
        assert result["total_resources"] == 0
        assert result["avg_usage_percent"] == 0.0

    def test_analyze_single_resource(self):
        resources = [
            AzureResource("Test", 10.0, 1.0, 10.0, "GB", "使用中")
        ]
        result = analyze_resources(resources)
        
        assert result["total_resources"] == 1
        assert result["used_resources"] == 1
        assert result["unused_resources"] == 0
        assert result["avg_usage_percent"] == 10.0

    def test_analyze_multiple_resources(self):
        resources = [
            AzureResource("Storage, Test", 0.0, 0.0, 100.0, "GB", "非使用中"),
            AzureResource("Virtual Machines, Test", 50.0, 375.0, 750.0, "Hour", "使用中"),
            AzureResource("Cognitive Services, Test", 25.0, 2.5, 10.0, "K", "使用中"),
        ]
        result = analyze_resources(resources)
        
        assert result["total_resources"] == 3
        assert result["used_resources"] == 2
        assert result["unused_resources"] == 1
        assert result["avg_usage_percent"] == pytest.approx(25.0)

    def test_categorization(self):
        resources = [
            AzureResource("Azure Cosmos DB, Test", 0.0, 0.0, 10.0, "GB", "非使用中"),
            AzureResource("Storage, Test", 0.0, 0.0, 100.0, "GB", "非使用中"),
            AzureResource("Virtual Machines, Test", 0.0, 0.0, 750.0, "Hour", "非使用中"),
            AzureResource("Cognitive Services, Test", 0.0, 0.0, 10.0, "K", "非使用中"),
            AzureResource("Azure Database for PostgreSQL", 0.0, 0.0, 32.0, "GB", "非使用中"),
            AzureResource("Networking, Test", 0.0, 0.0, 15.0, "GB", "非使用中"),
            AzureResource("Other Service", 0.0, 0.0, 10.0, "Unit", "非使用中"),
        ]
        result = analyze_resources(resources)
        
        categories = result["categories"]
        assert categories["cosmos_db"] == 1
        assert categories["storage"] == 1
        assert categories["vms"] == 1
        assert categories["cognitive"] == 1
        assert categories["databases"] == 1
        assert categories["networking"] == 1
        assert categories["other"] == 1

class TestGetTopUnused:
    def test_get_top_unused(self):
        resources = [
            AzureResource("Resource A", 0.0, 0.0, 100.0, "GB", "非使用中"),
            AzureResource("Resource B", 0.0, 0.0, 200.0, "GB", "非使用中"),
            AzureResource("Resource C", 50.0, 50.0, 100.0, "GB", "使用中"),
            AzureResource("Resource D", 0.0, 0.0, 150.0, "GB", "非使用中"),
        ]
        result = get_top_unused(resources, 2)
        
        assert len(result) == 2
        assert result[0][0] == "Resource B"
        assert result[1][0] == "Resource D"

    def test_get_top_unused_no_unused(self):
        resources = [
            AzureResource("Resource A", 50.0, 50.0, 100.0, "GB", "使用中"),
        ]
        result = get_top_unused(resources)
        assert len(result) == 0

    def test_get_top_unused_with_default_limit(self):
        resources = [AzureResource(f"Resource {i}", 0.0, 0.0, float(i), "GB", "非使用中") for i in range(10)]
        result = get_top_unused(resources)
        assert len(result) == 5

class TestFormatReport:
    def test_format_report(self):
        analysis = {
            "total_resources": 10,
            "used_resources": 2,
            "unused_resources": 8,
            "avg_usage_percent": 15.5,
            "categories": {
                "cosmos_db": 2,
                "storage": 3,
                "vms": 2,
                "cognitive": 2,
                "databases": 1,
                "networking": 0,
                "other": 0
            }
        }
        
        report = format_report(analysis)
        assert "Azure Resource Usage Report" in report
        assert "Total Resources: 10" in report
        assert "Used Resources: 2" in report
        assert "Unused Resources: 8" in report
        assert "Average Usage: 15.5%" in report
        assert "Cosmos Db: 2" in report
        assert "Storage: 3" in report

    def test_format_report_empty_categories(self):
        analysis = {
            "total_resources": 0,
            "used_resources": 0,
            "unused_resources": 0,
            "avg_usage_percent": 0.0,
            "categories": {
                "cosmos_db": 0,
                "storage": 0,
                "vms": 0,
                "cognitive": 0,
                "databases": 0,
                "networking": 0,
                "other": 0
            }
        }
        report = format_report(analysis)
        assert "Total Resources: 0" in report

class TestMain:
    def test_load_sample_data(self):
        data = load_sample_data()
        assert len(data) > 0
        assert "|" in data[0]

    def test_main_with_sample_data(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.argv = ["azuredemo"]
        try:
            result = main()
            assert result == 0
            output = captured_output.getvalue()
            assert "Azure Resource Usage Report" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_main_help(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.argv = ["azuredemo", "--help"]
        try:
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
        finally:
            sys.stdout = sys.__stdout__