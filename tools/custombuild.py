"""
MCP tools for DirectAdmin CustomBuild management.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_custombuild_actions():
    """
Get available custombuild actions

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/actions", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_compile_scripts():
    """
Get all custombuild's apps' compile scripts metadata

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/compile-scripts", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_compile_custom_app(app):
    """
Get custombuild's app's customized compile script

Args:
    app (string): Application name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/compile-scripts-custom/{app}", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_compile_custom_app(app, payload):
    """
Set custombuild's app's custom compile script

Args:
    app (string): Application name
    data (object): Request Data

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/compile-scripts-custom/{app}", method="PUT", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_compile_custom_app(app):
    """
Delete custombuild's app's custom compile script (reset to default)

Args:
    app (string): Application name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/compile-scripts-custom/{app}", method="DELETE")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_compile_app(app):
    """
Get custombuild's app's default compile script

Args:
    app (string): Application name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/compile-scripts/{app}", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_kill():
    """
Kill custombuild

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/kill", method="POST")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_logs():
    """
Get all custombuild log files metadata

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/logs", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_logs_logname(logname):
    """
Delete custombuild log

Args:
    logname (string): Log file name.

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/logs/{logname}", method="DELETE")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_log_sse(logname, last_event_id):
    """
Stream custombuild log file

Args:
    logname (string): Log file name
    Last-Event-Id (string): Read from position.

Returns:
    dict: API response from DirectAdmin.
"""
    headers = {}
    headers["Last-Event-Id"] = last_event_id
    response = await call_da_api(f"/api/custombuild/logs/{logname}/sse", method="GET", headers=headers)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_options_get():
    """
Get custombuild options

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/options", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_options_get(payload):
    """
Patch custombuild options

Args:
    data (object): Request Data

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/options", method="PATCH", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_options_v2_get():
    """
Get custombuild options

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/options-v2", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_options_v2_get(payload):
    """
Patch custombuild options

Args:
    data (object): List of key and value pairs to change

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/options-v2", method="PATCH", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_options_validate():
    """
Get custombuild options validation message

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/options/validate", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_removals():
    """
List of custombuild commands to remove no longer needed software

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/removals", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_run(payload):
    """
Run Custombuild

Args:
    data (object): Request Data

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/run", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_software():
    """
Get available custombuild software

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/software", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_state():
    """
Get custombuild state

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/state", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_state_sse():
    """
Get custombuild state stream

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/state/sse", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_updates():
    """
Get available custombuild updates

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/updates", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_versions():
    """
Get all custombuild's apps default versions

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/versions", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_custombuild_versions_custom():
    """
Get all custombuild's apps custom versions

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/versions-custom", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_version_custom_app(app, payload):
    """
Set custombuild's app's custom version

Args:
    app (string): Application name
    data (object): Request Data

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/versions-custom/{app}", method="PUT", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_cb_version_custom_app(app):
    """
Delete custombuild's app's custom version

Args:
    app (string): Application name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/custombuild/versions-custom/{app}", method="DELETE")
    return format_response(response)