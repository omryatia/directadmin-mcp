"""
This module provides tools to query system and server information from
DirectAdmin, including system resources and uptime.

Each tool is decorated with `@mcp.tool()` and leverages `call_da_api`
for HTTP requests.

"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)


@mcp.tool()
async def api_info():
    """Get basic server info."""
    try:
        response = await call_da_api("/api/info", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_info: {e}")
        raise


@mcp.tool()
async def api_system_info_cpu():
    """Get system CPU."""
    try:
        response = await call_da_api("/api/system-info/cpu", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_cpu: {e}")
        raise


@mcp.tool()
async def api_system_info_fs():
    """Get file system space usage."""
    try:
        response = await call_da_api("/api/system-info/fs", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_fs: {e}")
        raise


@mcp.tool()
async def api_system_info_load():
    """Get system load."""
    try:
        response = await call_da_api("/api/system-info/load", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_load: {e}")
        raise


@mcp.tool()
async def api_system_info_memory():
    """Get system memory."""
    try:
        response = await call_da_api("/api/system-info/memory", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_memory: {e}")
        raise


@mcp.tool()
async def api_system_info_services():
    """Get system services."""
    try:
        response = await call_da_api("/api/system-info/services", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_services: {e}")
        raise


@mcp.tool()
async def api_system_info_uptime():
    """Get system uptime."""
    try:
        response = await call_da_api("/api/system-info/uptime", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_system_info_uptime: {e}")
        raise