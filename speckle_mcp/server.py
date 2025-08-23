#!/usr/bin/env python3
"""
Speckle MCP Server

A Model Context Protocol server that provides tools for interacting with Speckle projects.
"""

import os
from typing import Optional
from mcp.server.fastmcp import FastMCP
from specklepy.api import operations
from specklepy.api.client import SpeckleClient


# Initialize server
mcp = FastMCP("speckle-mcp")


@mcp.tool()
def list_speckle_projects(
    token: Optional[str] = None,
    server_url: Optional[str] = None
) -> str:
    """List all Speckle projects accessible to the authenticated user.
    
    Configuration can be provided via:
    1. Environment variables (recommended): SPECKLE_TOKEN, SPECKLE_SERVER_URL
    2. Function parameters (override environment variables)
    
    Args:
        token: Personal access token for authentication (optional if SPECKLE_TOKEN env var set)
        server_url: Speckle server URL (optional, defaults to SPECKLE_SERVER_URL env var or app.speckle.systems)
        
    Returns:
        Formatted list of projects with names, IDs, descriptions, and update dates
    """
    try:
        # Get configuration from environment variables or parameters
        # Parameters override environment variables
        actual_token = token or os.getenv("SPECKLE_TOKEN")
        actual_server_url = server_url or os.getenv("SPECKLE_SERVER_URL", "https://app.speckle.systems")
        
        # Validate required configuration
        if not actual_token:
            return "Error: No authentication token provided. Set SPECKLE_TOKEN environment variable or provide token parameter."
        
        # Initialize Speckle client
        client = SpeckleClient(host=actual_server_url)
        client.authenticate_with_token(actual_token)
        
        # Fetch user's projects
        projects = client.active_user.get_projects().items
        
        # Format results
        if not projects:
            return "No projects found for the authenticated user."
        
        project_list = []
        for project in projects:
            project_info = f"• **{project.name}** (ID: {project.id})"
            if hasattr(project, 'description') and project.description:
                project_info += f"\n  Description: {project.description}"
            if hasattr(project, 'updatedAt'):
                project_info += f"\n  Last updated: {project.updatedAt}"
            project_list.append(project_info)
        
        return f"Found {len(projects)} Speckle projects:\n\n" + "\n\n".join(project_list)
        
    except Exception as e:
        return f"Error fetching Speckle projects: {str(e)}"


@mcp.tool()
def list_models_from_project(
    project_id: str,
    token: Optional[str] = None,
    server_url: Optional[str] = None
) -> str:
    """List all models within a specified Speckle project.
    
    Configuration can be provided via:
    1. Environment variables (recommended): SPECKLE_TOKEN, SPECKLE_SERVER_URL
    2. Function parameters (override environment variables)
    
    Args:
        project_id: The ID of the Speckle project to query
        token: Personal access token for authentication (optional if SPECKLE_TOKEN env var set)
        server_url: Speckle server URL (optional, defaults to SPECKLE_SERVER_URL env var or app.speckle.systems)
        
    Returns:
        Formatted list of models with names, IDs, descriptions, and update dates
    """
    try:
        # Get configuration from environment variables or parameters
        # Parameters override environment variables
        actual_token = token or os.getenv("SPECKLE_TOKEN")
        actual_server_url = server_url or os.getenv("SPECKLE_SERVER_URL", "https://app.speckle.systems")
        
        # Validate required configuration
        if not actual_token:
            return "Error: No authentication token provided. Set SPECKLE_TOKEN environment variable or provide token parameter."
        
        if not project_id:
            return "Error: No project ID provided."
        
        # Initialize Speckle client
        client = SpeckleClient(host=actual_server_url)
        client.authenticate_with_token(actual_token)
        
        # Fetch streams in the specified project
        models = client.model.get_models(project_id=project_id).items
        
        # Format results
        if not models:
            return f"No models found in project ID {project_id}."
        
        model_list = []
        for model in models:
            model_info = f"• **{model.name}** (ID: {model.id})"
            if hasattr(model, 'description') and model.description:
                model_info += f"\n  Description: {model.description}"
            if hasattr(model, 'updatedAt'):
                model_info += f"\n  Last updated: {model.updatedAt}"
            model_list.append(model_info)
        
        return f"Found {len(models)} models in project ID {project_id}:\n\n" + "\n\n".join(model_list)
    except Exception as e:
        return f"Error fetching models from project ID {project_id}: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")