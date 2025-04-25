"""
MCP tools for managing cPanel import endpoints in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_cpanel_check_remote(payload):
    """
Checks SSH connection to remote cPanel server and returns list of remote users

Args:
    params (object): Remote cPanel server credentials

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/check-remote", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_import_tasks():
    """
List all cPanel import tasks

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_start_import(payload):
    """
Starts remote cPanel account import to local DirectAdmin server

Args:
    params (object): Remote cPanel server credentials and list of accounts to import

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks/start", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_import_tasks_id(id):
    """
Get single cPanel import task

Args:
    id (string): Task ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks/{id}", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_import_tasks_id(id):
    """
Delete single pending cPanel import task

Args:
    id (string): Task ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks/{id}", method="DELETE")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_task_log(id):
    """
Retrieve single import task log

Args:
    id (string): Task ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks/{id}/log", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cpanel_task_log_sse(id, lastSeen):
    """
Stream import task log

Args:
    id (string): Task ID
    lastSeen (string): Last-Event-Id

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/cpanel-import/tasks/{id}/log-sse", method="GET")
    return format_response(response)