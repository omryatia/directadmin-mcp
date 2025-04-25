"""
MCP tools for accessing admin usage in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_admin_usage():
    """
Get admin's usage

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/admin-usage", method="GET")
    return format_response(response)