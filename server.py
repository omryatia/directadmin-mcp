"""
DirectAdmin MCP server with improved configuration and logging.
"""
import logging
import sys
import time
import os
from typing import Dict, Any

from config import settings, setup_logging
from mcp_instance import mcp

# Initialize logger
logger = logging.getLogger(__name__)

def log_startup_info():
    """Log detailed startup information."""
    logger.info("=" * 60)
    logger.info("DirectAdmin MCP Server - Starting up")
    logger.info("=" * 60)
    
    # Log system info
    import platform
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Platform: {platform.platform()}")
    
    # Log configuration (redact sensitive values)
    safe_settings = {
        k: v if not any(secret in k.lower() for secret in ['key', 'password', 'token', 'secret'])
        else '********'
        for k, v in settings.model_dump().items()
    }
    logger.info(f"Configuration: {safe_settings}")
    
    # Log startup message
    logger.info(f"Server will start on port {settings.PORT}")
    logger.info("=" * 60)

def handle_exit(exit_code: int = 0):
    """Handle graceful shutdown."""
    logger.info("=" * 60)
    logger.info(f"DirectAdmin MCP Server - Shutting down (exit code: {exit_code})")
    logger.info("=" * 60)
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        # Configure logging
        setup_logging()
        
        # Log startup info
        log_startup_info()
        
        # Import all tools from the tools package
        import tools
        loaded_modules = tools.load_all_tools()
        logger.info(f"Loaded {len(loaded_modules)} tool modules: {', '.join(loaded_modules)}")
        
        # Start the MCP server
        logger.info(f"Starting MCP server on port {settings.PORT}")
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested (KeyboardInterrupt)")
        handle_exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        handle_exit(1)