#!/usr/bin/env python3
"""
DirectAdmin MCP Client

A command-line client for interacting with the DirectAdmin MCP server.
"""

import asyncio
import json
import logging
import os
import sys
import argparse
from typing import Dict, Any, List, Optional
import aiohttp
import sseclient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("directadmin-mcp-client")

class DirectAdminMCPClient:
    """Client for the DirectAdmin MCP Server."""
    
    def __init__(
        self, 
        server_url: str = None, 
        api_key: str = None,
        timeout: int = 60,
        verify_ssl: bool = True
    ):
        """
        Initialize the MCP client.
        
        Args:
            server_url: MCP server URL (default: from environment variable)
            api_key: API key for authentication (default: from environment variable)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.server_url = server_url or os.environ.get("MCP_SERVER_URL", "http://localhost:8888")
        self.api_key = api_key or os.environ.get("MCP_API_KEY", "")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Strip trailing slash from server URL
        self.server_url = self.server_url.rstrip("/")
        
        # Setup headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
            
        logger.info(f"Initialized client for server: {self.server_url}")
    
    async def check_server_health(self) -> Dict[str, Any]:
        """
        Check if the MCP server is healthy.
        
        Returns:
            Health check information
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(
                    f"{self.server_url}/health",
                    timeout=self.timeout,
                    ssl=self.verify_ssl
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Health check failed: {str(e)}")
                return {"status": "unhealthy", "error": str(e)}
    
    async def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the MCP server.
        
        Returns:
            Server information
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(
                    f"{self.server_url}/about",
                    timeout=self.timeout,
                    ssl=self.verify_ssl
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Failed to get server info: {str(e)}")
                return {"error": str(e)}
    
    async def connect_sse(self, message: str) -> None:
        """
        Connect to the SSE endpoint and process events.
        
        Args:
            message: Message to send to the MCP server
        """
        url = f"{self.server_url}/sse"
        
        # Initial data
        initial_data = {
            "message": {
                "role": "user",
                "content": message
            }
        }
        
        # Headers for SSE connection
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            # Initialize session and post initial message
            async with aiohttp.ClientSession() as session:
                # Convert data to JSON
                json_data = json.dumps(initial_data)
                
                # Initial POST request
                async with session.post(
                    url, 
                    data=json_data,
                    headers=headers,
                    timeout=self.timeout,
                    ssl=self.verify_ssl
                ) as response:
                    response.raise_for_status()
                    
                    # Process SSE events
                    client = sseclient.SSEClient(response.content)
                    
                    # Process events
                    for event in client.events():
                        if event.event == "message":
                            try:
                                data = json.loads(event.data)
                                if "message" in data:
                                    if data["message"]["role"] == "assistant":
                                        print(f"\nASSISTANT: {data['message']['content']}")
                                elif "error" in data:
                                    print(f"\nERROR: {data['error']}")
                            except json.JSONDecodeError:
                                print(f"\nRaw event data: {event.data}")
                        elif event.event == "context":
                            try:
                                data = json.loads(event.data)
                                # Process context data
                                if data.get("items"):
                                    print("\nContext items received:")
                                    for item in data["items"]:
                                        print(f"  - Type: {item.get('type', 'unknown')}")
                            except json.JSONDecodeError:
                                print(f"\nRaw context data: {event.data}")
                        elif event.event == "done":
                            print("\nConversation complete")
                            break
                        else:
                            print(f"\nEvent: {event.event}, Data: {event.data}")
        
        except aiohttp.ClientError as e:
            logger.error(f"SSE connection error: {str(e)}")
            print(f"\nError connecting to MCP server: {str(e)}")
        except KeyboardInterrupt:
            print("\nConnection closed by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(f"\nUnexpected error: {str(e)}")

async def main():
    """Main entry point for the client."""
    parser = argparse.ArgumentParser(description="DirectAdmin MCP Client")
    
    # Add arguments
    parser.add_argument("--server", "-s", help="MCP server URL")
    parser.add_argument("--key", "-k", help="API key for authentication")
    parser.add_argument("--no-verify", action="store_true", help="Disable SSL verification")
    parser.add_argument("--timeout", "-t", type=int, default=60, help="Request timeout in seconds")
    parser.add_argument("--info", "-i", action="store_true", help="Get server info")
    parser.add_argument("--health", action="store_true", help="Check server health")
    parser.add_argument("message", nargs="?", help="Message to send to MCP server")
    
    args = parser.parse_args()
    
    # Create client
    client = DirectAdminMCPClient(
        server_url=args.server,
        api_key=args.key,
        timeout=args.timeout,
        verify_ssl=not args.no_verify
    )
    
    # Check what operation to perform
    if args.health:
        # Health check
        health = await client.check_server_health()
        print(json.dumps(health, indent=2))
    elif args.info:
        # Get server info
        info = await client.get_server_info()
        print(json.dumps(info, indent=2))
    elif args.message:
        # Connect to SSE and send message
        await client.connect_sse(args.message)
    else:
        # Interactive mode
        print("DirectAdmin MCP Client (Interactive Mode)")
        print("Enter 'exit' or 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                message = input("\nYou: ")
                if message.lower() in ["exit", "quit"]:
                    break
                
                if message.strip():
                    await client.connect_sse(message)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error: {str(e)}", exc_info=True)
                print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())