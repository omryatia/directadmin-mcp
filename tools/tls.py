"""
Auto-generated module for TLS endpoints.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_server_tls_acme_config():
    """
    Get main server's TLS ACME configuration.
    """
    try:
        response = await call_da_api("/api/server-tls/acme-config", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_acme_config: {e}")
        raise

@mcp.tool()
async def api_server_tls_acme_config_update(data):
    """
    Set main server's TLS ACME configuration.
    
    Args:
        data: Dictionary containing ACME config values.
    """
    try:
        response = await call_da_api("/api/server-tls/acme-config", method="PUT", data={"data": data})
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_acme_config_update: {e}")
        raise

@mcp.tool()
async def api_server_tls_certificate():
    """
    Get main server's TLS certificate.
    """
    try:
        response = await call_da_api("/api/server-tls/certificate", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_certificate: {e}")
        raise

@mcp.tool()
async def api_server_tls_enable(force):
    """
    Enable SSL for main server.
    
    Args:
        force: Boolean to force SSL enablement.
    """
    try:
        response = await call_da_api("/api/server-tls/enable", method="POST", data={"force": force})
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_enable: {e}")
        raise

@mcp.tool()
async def api_server_tls_files():
    """
    Retrieve server TLS certificates.
    """
    try:
        response = await call_da_api("/api/server-tls/files", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_files: {e}")
        raise

@mcp.tool()
async def api_server_tls_files_update(data, force):
    """
    Replace server TLS certificates.
    
    Args:
        data: Certificate data.
        force: Whether to overwrite existing certs.
    """
    try:
        response = await call_da_api("/api/server-tls/files", method="PUT", data={"data": data, "force": force})
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_files_update: {e}")
        raise

@mcp.tool()
async def api_server_tls_obtain():
    """
    Queues action to force obtain TLS certificate for main server.
    """
    try:
        response = await call_da_api("/api/server-tls/obtain", method="POST")
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_obtain: {e}")
        raise

@mcp.tool()
async def api_server_tls_status():
    """
    Get main server's TLS certificate status.
    """
    try:
        response = await call_da_api("/api/server-tls/status", method="GET")
        return response
    except Exception as e:
        logger.error(f"Error in api_server_tls_status: {e}")
        raise