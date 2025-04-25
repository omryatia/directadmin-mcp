"""
MCP tools for DirectAdmin versioning and updates.
"""
import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)

@mcp.tool()
@log_tool_call
async def api_get_version():
    """
    Get DirectAdmin version information.
    
    This retrieves detailed version information for the DirectAdmin
    installation, including version number, build, and update channel.
    
    Returns:
        Version information for DirectAdmin
    """
    response = await call_da_api("/api/version", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_change_update_channel(channel):
    """
    Change DirectAdmin update channel.
    
    This changes the update channel for DirectAdmin, which determines
    which version stream is used for updates (e.g., stable, beta).
    
    Args:
        channel: Update channel to switch to (e.g., "stable", "beta", "alpha")
        
    Returns:
        Result of the channel change operation
    """
    response = await call_da_api("/api/version", method="PATCH", data={"channel": channel})
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_version_update():
    """
    Update DirectAdmin to the latest version.
    
    This initiates an update of DirectAdmin to the latest version available
    in the currently selected update channel. This may cause a brief service
    interruption while DirectAdmin is restarting.
    
    Returns:
        Result of the update operation
    """
    response = await call_da_api("/api/version/update", method="POST")
    return format_response(response)