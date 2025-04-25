"""
MCP tools for managing ClamAV antivirus operations in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_clamav_get():
    """
Get clamAV processes

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/clamav", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_clamav_scan(payload):
    """
Scan directories in the specified path

Args:
    params (object): ClamAV params

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/clamav", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_clamav_pid(pid):
    """
Cancel the clamAV process by PID

Args:
    pid (string): PID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/clamav/{pid}", method="DELETE")
    return format_response(response)