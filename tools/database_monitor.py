"""
MCP tools for monitoring database processes in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_db_monitor_list():
    """
Get database processes list

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/db-monitor/processes", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_db_monitor_kill_process(id):
    """
Kill database thread

Args:
    id (integer): Thread ID.

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/db-monitor/processes/{id}/kill", method="POST")
    return format_response(response)