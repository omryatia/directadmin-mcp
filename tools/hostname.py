"""
MCP tools for managing DirectAdmin server hostname.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_server_settings_change_hostname(data):
    """
    Change the server hostname.

    This endpoint updates the DirectAdmin server hostname to a new value
    as provided in the request payload.

    Args:
        data: Dictionary containing the new hostname value under the key "hostname".

    Returns:
        A confirmation message or error from the DirectAdmin API.
    """
    try:
        response = await call_da_api("/api/server-settings/change-hostname", method="POST", data={"data": data})
        return response
    except Exception as e:
        logger.error(f"Error in api_server_settings_change_hostname: {e}")
        raise