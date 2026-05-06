# Azure DevOps CI/CD Demo Project

A Python project demonstrating CI/CD integration with Azure DevOps Pipelines.

## Features

- **Azure Resource Usage Analyzer**: Analyzes Azure free tier resource usage
- **uv Package Manager**: Modern Python package management
- **Unit Testing**: pytest with code coverage
- **Azure DevOps Pipeline**: Complete CI/CD workflow

## Getting Started

### Prerequisites

- Python 3.10+
- uv (package manager)

### Installation

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <repository-url>
cd azure-devops-demo

# Install dependencies
uv sync
```

### Usage

```bash
# Run the application with sample data
uv run azuredemo

# Run with custom data file
uv run azuredemo -f resources.txt
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest tests/ --cov=azuredemo --cov-report=term-missing --cov-report=html
```

## Project Structure

```
azure-devops-demo/
├── src/
│   └── azuredemo/
│       ├── __init__.py      # Package init
│       ├── main.py          # CLI entry point
│       └── utils.py         # Core utilities
├── tests/
│   ├── __init__.py
│   └── test_utils.py        # Unit tests
├── azure-pipelines.yml      # Azure DevOps Pipeline config
├── pyproject.toml           # Project configuration
└── README.md
```

## Azure DevOps Pipeline

The pipeline includes:

1. **Build Stage**:
   - Checkout code
   - Install Python
   - Install uv
   - Install dependencies
   - Run unit tests with coverage
   - Publish coverage results
   - Archive and publish artifacts

2. **Deploy Stage**:
   - Download artifacts
   - Extract deployment package
   - Install application on target VM
   - Verify installation

## Azure Resources Used

- **Virtual Machines**: For deployment target
- **Azure Pipelines**: For CI/CD automation
- **Azure Artifacts**: For storing build artifacts

## License

MIT License