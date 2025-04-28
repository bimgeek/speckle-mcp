[![MseeP Badge](https://mseep.net/pr/bimgeek-speckle-mcp-badge.jpg)](https://mseep.ai/app/bimgeek-speckle-mcp)

# Speckle MCP Server

A Model Context Protocol (MCP) server for interacting with Speckle, the collaborative data hub that connects with your AEC tools.

## Overview

This MCP server acts as a bridge between Speckle's API and client applications and exposes a set of tools that allow users to:

- List and search Speckle projects
- Retrieve detailed project information
- Access model versions within projects
- Retrieve and query objects and their properties from specific versions

## Installation

### Prerequisites

- Python 3.13 or higher
- Speckle account with a personal access token
- uv for dependency management and virtual environments

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/bimgeek/speckle-mcp.git
   cd speckle-mcp
   ```

2. Ensure you have Python 3.13 installed:
   ```bash
   python --version  # Should show Python 3.13.x
   ```

3. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```


## Configuration

### Environment Variables

The server requires the following environment variables:

- `SPECKLE_TOKEN`: Your Speckle personal access token (required)
- `SPECKLE_SERVER`: The Speckle server URL (defaults to https://app.speckle.systems)

### MCP Configuration

To use this server with Claude, you need to update your MCP configuration file. The configuration file is typically located at:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add or update the "speckle" entry in the `mcpServers` section:

```json
{
  "mcpServers": {
    "speckle": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/speckle-mcp",
        "run",
        "speckle_server.py"
      ],
      "env": {
        "SPECKLE_TOKEN": "YOUR_SPECKLE_API_TOKEN_HERE",
        "SPECKLE_SERVER": "https://app.speckle.systems"
      }
    }
  }
}
```


Replace `/path/to/speckle-mcp` with the actual path to the directory containing the `speckle_mcp` package.

## Available Tools

### Projects

- `list_projects`: Lists all accessible Speckle projects
  - Parameters:
    - `limit` (optional): Maximum number of projects to retrieve (default: 20)

- `get_project_details`: Retrieves detailed information about a specific project
  - Parameters:
    - `project_id`: The ID of the Speckle project to retrieve
    - `limit` (optional): Maximum number of models to retrieve (default: 20)

- `search_projects`: Searches for projects by name or description
  - Parameters:
    - `query`: The search term to look for in project names and descriptions

### Models

- `get_model_versions`: Lists all versions for a specific model
  - Parameters:
    - `project_id`: The ID of the Speckle project
    - `model_id`: The ID of the model to retrieve versions for
    - `limit` (optional): Maximum number of versions to retrieve (default: 20)

### Objects

- `get_version_objects`: Retrieves objects from a specific version
  - Parameters:
    - `project_id`: The ID of the Speckle project
    - `version_id`: The ID of the version to retrieve objects from
    - `include_children` (optional): Whether to include children objects in the response (default: false)

- `query_object_properties`: Queries specific properties from objects in a version
  - Parameters:
    - `project_id`: The ID of the Speckle project
    - `version_id`: The ID of the version to retrieve objects from
    - `property_path`: The dot-notation path to the property (e.g., "elements.0.name")

## Troubleshooting

- If you encounter authentication issues, make sure your Speckle token is valid and has the necessary permissions
- Check the server logs for detailed error messages
- Ensure the environment variables are correctly set in the MCP configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
