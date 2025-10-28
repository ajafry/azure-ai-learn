"""
Remote MCP Client Example

This module demonstrates how to use the Model Context Protocol (MCP) with a remote HTTP server
to create an AI agent that can answer Microsoft documentation questions. The agent uses
Azure OpenAI services and connects to Microsoft Learn's MCP endpoint to provide enhanced
responses with access to Microsoft's documentation.

Dependencies:
    - agent_framework: Framework for building AI agents with tool capabilities
    - azure.identity: Azure authentication library
    - dotenv: Environment variable management
"""

import asyncio
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows configuration of Azure credentials and endpoints without hardcoding
load_dotenv()

async def remote_mcp_example():
    """
    Demonstrates using a remote MCP (Model Context Protocol) server via HTTP.
    
    This function creates a chat agent that can answer Microsoft documentation questions
    by connecting to Microsoft Learn's MCP endpoint. The agent uses Azure OpenAI for
    language processing and the MCP server for accessing Microsoft's documentation.
    
    The function sets up:
    1. An MCPStreamableHTTPTool connected to Microsoft Learn's API
    2. A ChatAgent with Azure OpenAI backend and specific instructions
    3. Executes a sample query about Azure Container Apps
    
    Returns:
        None: Prints the agent's response to the console
        
    Raises:
        Exception: May raise exceptions related to network connectivity, 
                  authentication, or Azure service availability
    """
    # Use async context managers to ensure proper resource cleanup
    async with (
        # Initialize the MCP tool for connecting to Microsoft Learn's documentation API
        # This tool enables the agent to access and search Microsoft's documentation
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",  # Human-readable name for the tool
            url="https://learn.microsoft.com/api/mcp"  # Microsoft Learn MCP endpoint
        ) as mcp_server,
        
        # Create a chat agent with Azure OpenAI backend
        ChatAgent(
            # Azure OpenAI client with CLI-based authentication
            # Uses the Azure CLI credentials from the current session
            chat_client=AzureOpenAIChatClient(credential=AzureCliCredential()),
            name="MSLearnAgent",
            instructions="You help with Microsoft documentation questions.",  # System prompt
        ) as agent,
    ):
        # Execute a query using the agent with access to the MCP server tools
        # The agent will use the MCP server to search Microsoft documentation
        # and provide a comprehensive answer
        result = await agent.run(
            "What is the Azure Container Apps service",  # User query
            tools=mcp_server  # Provide the MCP server as available tooling
        )
        
        # Output the agent's response to the console
        print(result)

# Entry point for the script
if __name__ == "__main__":
    asyncio.run(remote_mcp_example())