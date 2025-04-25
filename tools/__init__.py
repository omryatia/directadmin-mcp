"""
DirectAdmin MCP Tool Registry.

This package contains all the tool modules for DirectAdmin MCP integration.
Tools are automatically imported and registered with the MCP instance.
"""

import os
import importlib
import logging
import glob
from typing import List

logger = logging.getLogger(__name__)

def load_all_tools() -> List[str]:
    """
    Load all tool modules from the tools directory.
    
    Returns:
        List of loaded module names
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tool_files = glob.glob(os.path.join(current_dir, "*.py"))
    
    # Filter out __init__.py and common.py
    tool_modules = []
    for file_path in tool_files:
        filename = os.path.basename(file_path)
        module_name = os.path.splitext(filename)[0]
        
        if module_name not in ["__init__", "common"]:
            tool_modules.append(module_name)
    
    # Import each module - this will register the tools with MCP
    loaded_modules = []
    for module_name in tool_modules:
        try:
            importlib.import_module(f"tools.{module_name}")
            loaded_modules.append(module_name)
            logger.info(f"Loaded tool module: tools.{module_name}")
        except Exception as e:
            logger.error(f"Error loading tool module tools.{module_name}: {str(e)}")
    
    return loaded_modules

# Import common utilities
from tools.common import log_tool_call, format_response, parse_args