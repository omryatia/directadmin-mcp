"""
MCP tools for managing DirectAdmin configuration settings.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_da_conf_active():
    """
    Get active DirectAdmin config.

    Returns:
        JSON with the currently active directadmin.conf settings.
    """
    try:
        response = await call_da_api(
            "/api/server-settings/directadmin-conf/active",
            method="GET"
        )
        return response
    except Exception as e:
        logger.error(f"Error in api_da_conf_active: {e}")
        raise

@mcp.tool()
async def api_da_conf_default():
    """
    Get default DirectAdmin config.

    Returns:
        JSON with the default values of directadmin.conf.
    """
    try:
        response = await call_da_api(
            "/api/server-settings/directadmin-conf/default",
            method="GET"
        )
        return response
    except Exception as e:
        logger.error(f"Error in api_da_conf_default: {e}")
        raise

@mcp.tool()
async def api_da_conf_local():
    """
    Get local DirectAdmin config.

    Returns:
        JSON with local overrides in directadmin.conf.
    """
    try:
        response = await call_da_api(
            "/api/server-settings/directadmin-conf/local",
            method="GET"
        )
        return response
    except Exception as e:
        logger.error(f"Error in api_da_conf_local: {e}")
        raise

@mcp.tool()
async def api_da_conf_local_replace(skip_unknown: bool, data: dict):
    """
    Replace local DirectAdmin config.

    Args:
        skip_unknown (bool): If true, ignore unknown config values.
        data (dict): Configuration key-value pairs.

    Returns:
        JSON with status of the replacement operation.
    """
    try:
        response = await call_da_api(
            "/api/server-settings/directadmin-conf/local",
            method="PUT",
            data={"skip-unknown": skip_unknown, "data": data}
        )
        return response
    except Exception as e:
        logger.error(f"Error in api_da_conf_local_replace: {e}")
        raise

@mcp.tool()
async def api_da_conf_local_patch(skip_unknown: bool, data: dict):
    """
    Patch local DirectAdmin config.

    Args:
        skip_unknown (bool): If true, ignore unknown config values.
        data (dict): Partial configuration to update.

    Returns:
        JSON with status of the patch operation.
    """
    try:
        response = await call_da_api(
            "/api/server-settings/directadmin-conf/local",
            method="PATCH",
            data={"skip-unknown": skip_unknown, "data": data}
        )
        return response
    except Exception as e:
        logger.error(f"Error in api_da_conf_local_patch: {e}")
        raise