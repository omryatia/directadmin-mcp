
"""
This module provides access to the password-related
endpoints in the DirectAdmin API.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_change_password(data):
    """
    Change user password.

    Args:
        data: Dictionary containing the password change details.

    Returns:
        API response after attempting to change the password.
    """
    try:
        response = await call_da_api("/api/change-password", method="POST", data={"data": data})
        return response
    except Exception as e:
        logger.error(f"Error in api_change_password: {e}")
        raise