"""
MCP tools for backend search endpoints in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_search_multi_user(q, limit):
    """
Searches for resources globally, results are for user accounts and domains.

Args:
    q (string): query
    limit (number): Query limit

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/search/multi-user", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_search_single_user(q):
    """
Searches for single user account owned resources.

Args:
    q (string): query

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/search/single-user", method="GET")
    return format_response(response)