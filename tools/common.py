"""
Common utilities for DirectAdmin MCP tools.
"""
import logging
import functools
import inspect
import json
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from da import call_da_api, DirectAdminError

logger = logging.getLogger(__name__)

# Type variable for tool functions
T = TypeVar('T', bound=Callable)

def log_tool_call(func: T) -> T:
    """
    Decorator to log tool calls with parameters and results.
    
    Args:
        func: The tool function to decorate
        
    Returns:
        Decorated function with logging
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get function signature for better logging
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # Sanitize args for logging (remove sensitive data)
        safe_args = {}
        for key, value in bound_args.arguments.items():
            if key == 'self':
                continue
                
            if any(sensitive in key.lower() for sensitive in ['pass', 'key', 'token', 'secret']):
                safe_args[key] = '********'
            else:
                safe_args[key] = value
        
        # Log the call
        logger.info(f"Tool call: {func.__name__} with args: {safe_args}")
        
        try:
            # Execute the function
            result = await func(*args, **kwargs)
            
            # Log result summary (not the full result to avoid log spam)
            if isinstance(result, dict):
                logger.info(f"Tool {func.__name__} result: {len(result)} keys - {list(result.keys())[:5]}")
            elif isinstance(result, list):
                logger.info(f"Tool {func.__name__} result: list with {len(result)} items")
            else:
                logger.info(f"Tool {func.__name__} result: {type(result)}")
                
            return result
        except DirectAdminError as e:
            # Log DirectAdmin errors with details
            logger.error(f"DirectAdmin API error in tool {func.__name__}: {str(e)}", exc_info=True)
            
            # Return structured error
            return {
                "error": True,
                "message": str(e),
                "status_code": getattr(e, 'status_code', None),
                "response_data": getattr(e, 'response_data', None)
            }
        except Exception as e:
            # Log general errors
            logger.error(f"Error in tool {func.__name__}: {str(e)}", exc_info=True)
            
            # Return structured error
            return {
                "error": True,
                "message": str(e),
                "type": type(e).__name__
            }
    
    return cast(T, wrapper)

def format_response(data: Any) -> Dict[str, Any]:
    """
    Format tool response data consistently.
    
    Args:
        data: The data to format
        
    Returns:
        Formatted response dictionary
    """
    if isinstance(data, dict) and "error" in data:
        # Already formatted error
        return data
        
    return {
        "success": True,
        "data": data
    }

def parse_args(args_str: str) -> Dict[str, Any]:
    """
    Parse string arguments into a dictionary.
    
    Args:
        args_str: Arguments string (can be JSON or key=value pairs)
        
    Returns:
        Parsed arguments as dictionary
    """
    if not args_str:
        return {}
        
    # Try to parse as JSON first
    try:
        return json.loads(args_str)
    except json.JSONDecodeError:
        # Fall back to key=value parsing
        args_dict = {}
        for arg in args_str.split():
            if '=' in arg:
                key, value = arg.split('=', 1)
                args_dict[key.strip()] = value.strip()
        return args_dict