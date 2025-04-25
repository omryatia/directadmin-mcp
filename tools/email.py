"""
MCP tools for interacting with DirectAdmin's email-related endpoints.
"""

import logging
from mcp_instance import mcp
from da import call_da_api

logger = logging.getLogger(__name__)

@mcp.tool()
async def api_email_config_mobileconfig(email, format):
    """
    Download Apple Mail configuration profile.

    Args:
        email: The email address for which to generate the profile.
        format: The format of the profile (e.g., 'mac', 'ios').

    Returns:
        The mobileconfig profile.
    """
    try:
        response = await call_da_api("/api/email-config/mobileconfig", method="GET", data={"email": email, "format": format})
        return response
    except Exception as e:
        logger.error(f"Error in api_email_config_mobileconfig: {e}")
        raise

@mcp.tool()
async def api_email_logs(e_from, e_to, address, domain, state, type):
    """
    Retrieve email log entries.

    Args:
        e_from: Start time filter.
        e_to: End time filter.
        address: Specific email address.
        domain: Domain name.
        state: Email state (sent, deferred, etc.).
        type: Type of email (incoming, outgoing, etc.).

    Returns:
        List of email log entries.
    """
    try:
        response = await call_da_api("/api/email-logs", method="GET", data={"from": e_from, "to": e_to, "address": address, "domain": domain, "state": state, "type": type})
        return response
    except Exception as e:
        logger.error(f"Error in api_email_logs: {e}")
        raise

@mcp.tool()
async def api_email_logs_summary(e_from, e_to):
    """
    Retrieve summary of email log statistics.

    Args:
        e_from: Start time filter.
        e_to: End time filter.

    Returns:
        Summary statistics of email logs.
    """
    try:
        response = await call_da_api("/api/email-logs-summary", method="GET", data={"from": e_from, "to": e_to})
        return response
    except Exception as e:
        logger.error(f"Error in api_email_logs_summary: {e}")
        raise