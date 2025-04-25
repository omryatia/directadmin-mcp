"""
MCP instance configuration with enhanced setup and error handling.
"""
import logging
from mcp.server.fastmcp import FastMCP
from config import settings

logger = logging.getLogger(__name__)

# Initialize the MCP instance with detailed logging
logger.info(f"Initializing DirectAdmin MCP instance with name: {settings.MCP_NAME}")

try:
    # Create the MCP instance
    mcp = FastMCP(settings.MCP_NAME)
    
    logger.info("MCP instance initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize MCP instance: {str(e)}", exc_info=True)
    raise