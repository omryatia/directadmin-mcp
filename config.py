"""
Configuration module for DirectAdmin MCP server.
"""
import os
import logging
from typing import Optional

# For Pydantic v2, BaseSettings has moved to pydantic-settings
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables with sane defaults."""
    # DirectAdmin Settings
    DA_URL: str = Field(..., description="DirectAdmin server URL with port (e.g., https://example.com:2222)")
    DA_USERNAME: str = Field(..., description="DirectAdmin username (admin)")
    DA_LOGIN_KEY: str = Field(..., description="DirectAdmin login key")
    
    # Server Settings
    PORT: int = Field(8888, description="Port to run the MCP server on")
    LOG_LEVEL: str = Field("INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    DEBUG: bool = Field(False, description="Enable debug mode")
    
    # MCP Settings
    MCP_NAME: str = Field("directadmin", description="Name of the MCP instance")
    
    # SSL Settings
    SSL_VERIFY: bool = Field(True, description="Verify SSL certificates for DirectAdmin API calls")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

# Create settings instance
settings = Settings()

# Configure logging
def setup_logging():
    """Set up logging configuration."""
    log_level = getattr(logging, settings.LOG_LEVEL)
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # File handler for all logs
    file_handler = logging.FileHandler('logs/directadmin_mcp.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Error file handler
    error_file_handler = logging.FileHandler('logs/error.log')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(file_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates when reloading in development
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)
    
    # Set specific levels for noisy libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    
    return root_logger

# Initialize logger
logger = setup_logging()