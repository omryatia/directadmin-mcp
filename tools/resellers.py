"""
MCP tools for managing DirectAdmin resellers.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_resellers_username_config(username):
    """
    Get reseller configuration settings.

    Retrieves configuration details for a specific reseller.

    Args:
        username: The reseller's username.

    Returns:
        The reseller's configuration settings.
    """
    try:
        response = await call_da_api(f"/api/resellers/{username}/config", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_resellers_username_config: {e}")
        raise

@mcp.tool()
async def api_resellers_username_usage(username):
    """
    Get reseller usage information.

    Retrieves resource usage statistics for a specific reseller,
    including their own and all associated user accounts.

    Args:
        username: The reseller's username.

    Returns:
        Usage statistics.
    """
    try:
        response = await call_da_api(f"/api/resellers/{username}/usage", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_resellers_username_usage: {e}")
        raise