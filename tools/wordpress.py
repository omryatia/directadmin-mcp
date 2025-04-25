"""
MCP tools for managing WordPress installations in DirectAdmin.
"""

import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

logger = logging.getLogger(__name__)


@mcp.tool()
@log_tool_call
async def api_wordpress_install(payload):
    """
Performs new wordpress installation in a given location

Args:
    payload (object): New wordpress installation configuration

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/install", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_install_quick(payload):
    """
Performs quick new wordpress installation in a given location

Args:
    payload (object): New wordpress installation configuration

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/install-quick", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations(domain):
    """
Returns list of known wordpress installations and potential installation locations.

Args:
    domain (string): Filter locations by domain name, sub-domains are not accepted

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id(location_id):
    """
Remove wordpress installation.

Args:
    location_id (string): WordPress location ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}", method="DELETE")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_config(location_id):
    """
Retrieve wordpress database configuration for a single installation.

Args:
    location_id (string): WordPress location ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/config", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_config(location_id, payload):
    """
Change wordpress database configuration for a single installation.

Args:
    location_id (string): WordPress location ID
    payload (object): New configuration

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/config", method="PUT", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wp_cfg_autoupdate(location_id, payload):
    """
Change wordpress core auto update state.

Args:
    location_id (string): WordPress location ID
    payload (object): New configuration

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/config/auto-update", method="PUT", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_options(location_id):
    """
Retrieve all wordpress options for a single installation.

Args:
    location_id (string): WordPress location ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/options", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_options(location_id, payload):
    """
Change wordpress options for a given installation.

Args:
    location_id (string): WordPress location ID
    payload (object): Set of options to change, nil value deletes option

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/options", method="PATCH", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_users(location_id):
    """
Retrieve all wordpress user accounts

Args:
    location_id (string): WordPress location ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/users", method="GET")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wp_user_pwd_change(location_id, user_id, payload):
    """
Change wordpress user account password

Args:
    location_id (string): WordPress location ID
    user_id (integer): User ID
    payload (object): payload

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/users/{user_id}/change-password", method="POST", data=payload)
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wp_user_sso_login(location_id, user_id):
    """
Create magic login URL.

Args:
    location_id (string): WordPress location ID
    user_id (integer): User ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/users/{user_id}/sso-login", method="POST")
    return format_response(response)

@mcp.tool()
@log_tool_call
async def api_wordpress_locations_location_id_wordpress(location_id):
    """
Retrieve information about a single WordPress installation

Args:
    location_id (string): WordPress location ID

Returns:
    dict: API response from DirectAdmin.
"""
    response = await call_da_api(f"/api/wordpress/locations/{location_id}/wordpress", method="GET")
    return format_response(response)