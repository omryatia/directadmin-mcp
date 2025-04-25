"""
MCP tools for managing session-related tasks in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_session():
    """
Get current session info

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_login_as_return():
    """
Drop out of Login-as session

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/login-as/return", method="POST")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_login_as_switch(payload):
    """
Swich to a new session that impersonating another account

Args:
    params (object): Authentication attributes

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/login-as/switch", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_login_as_user_list(q, limit):
    """
Search for users when in login-as session

Args:
    q (string): query
    limit (number): Query limit

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/login-as/user-list", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_reseller_config():
    """
Get reseller config

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/reseller-config", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_skin_customization_skin(skin):
    """
Get list of active skin customizations

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_skin_img_favicon(skin):
    """
Get skin favicon image

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/images/favicon", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_skin_customization_skin_images_logo(skin):
    """
Get skin logo image

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/images/logo", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_skin_customization_skin_images_logo2(skin):
    """
Get skin logo2 image

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/images/logo2", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_skin_img_symbol(skin):
    """
Get skin symbol image

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/images/symbol", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_skin_img_symbol2(skin):
    """
Get skin symbol2 image

Args:
    skin (string): Skin's name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/images/symbol2", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_skin_customization_skin_filename(skin, filename):
    """
Download active skin customization file

Args:
    skin (string): Skin's name
    filename (string): Skin customization file name

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/skin-customization/{skin}/{filename}", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_state():
    """
Get server state

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/state", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_switch_active_domain(payload):
    """
Switch active domain for current session

Args:
    request (object): Request data.

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/switch-active-domain", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_user_config():
    """
Current user config

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/user-config", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_session_user_usage():
    """
Get user's usage

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/session/user-usage", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_sessions():
    """
List active user sessions

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/sessions", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_sessions_destroy_all_other():
    """
Destroy all active sessions except current

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/sessions/destroy-all-other", method="POST")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_sessions_destroy_public_id(public_id):
    """
Destroy an active session

Args:
    public_id (string): Session's public ID.

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/sessions/destroy/{public_id}", method="POST")
    return format_response(response)