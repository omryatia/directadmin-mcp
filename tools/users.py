"""
MCP tools for DirectAdmin user-related operations.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_login_history():
    """
    Get login history.

    Retrieves the login history for the current session or user.

    Returns:
        List of login events and associated metadata.
    """
    try:
        response = await call_da_api("/api/login-history", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_login_history: {e}")
        raise

@mcp.tool()
async def api_users_username_config(username):
    """
    Get user configuration.

    Retrieves configuration details for the specified user.

    Args:
        username: Username of the account.

    Returns:
        Configuration information for the specified user.
    """
    try:
        response = await call_da_api(f"/api/users/{username}/config", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_users_username_config: {e}")
        raise

@mcp.tool()
async def api_users_username_login_history(username):
    """
    Get user login history.

    Retrieves login activity logs for a specific user.

    Args:
        username: Username whose login history is to be retrieved.

    Returns:
        List of login entries for the user.
    """
    try:
        response = await call_da_api(f"/api/users/{username}/login-history", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_users_username_login_history: {e}")
        raise

@mcp.tool()
async def api_users_username_usage(username):
    """
    Get user usage statistics.

    Fetches usage statistics such as disk, bandwidth, and database usage for the given user.

    Args:
        username: Username of the account.

    Returns:
        Usage metrics for the user.
    """
    try:
        response = await call_da_api(f"/api/users/{username}/usage", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_users_username_usage: {e}")
        raise