"""
DirectAdmin API client with improved error handling and logging.
"""
import os
import httpx
import base64
import logging
from typing import Dict, Any, Optional, Union
import json
from config import settings

logger = logging.getLogger(__name__)

class DirectAdminError(Exception):
    """Custom exception for DirectAdmin API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Any] = None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class DirectAdminClient:
    """Enhanced DirectAdmin API client with better error handling and logging."""
    
    def __init__(
        self, 
        base_url: str = settings.DA_URL,
        username: str = settings.DA_USERNAME, 
        login_key: str = settings.DA_LOGIN_KEY,
        verify_ssl: bool = settings.SSL_VERIFY
    ):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.login_key = login_key
        self.verify_ssl = verify_ssl
        
        # Create auth token
        self.token = base64.b64encode(f"{username}:{login_key}".encode()).decode()
        
        # Default headers
        self.headers = {
            "Authorization": f"Basic {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        logger.debug(f"DirectAdmin client initialized for {self.base_url} with user {self.username}")
    
    async def call_api(
        self, 
        path: str, 
        method: str = "GET", 
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Make a request to the DirectAdmin API with improved logging and error handling.
        
        Args:
            path: API endpoint path (without base URL)
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            data: Request data/parameters
            timeout: Request timeout in seconds
            
        Returns:
            Response data as dictionary
            
        Raises:
            DirectAdminError: On API errors or unexpected responses
        """
        url = f"{self.base_url}{path}"
        method = method.upper()
        
        # Log request details (with sensitive data redacted)
        log_data = None
        if data:
            # Create a copy to avoid modifying the original
            log_data = data.copy() if isinstance(data, dict) else data
            # Redact sensitive fields for logging
            if isinstance(log_data, dict):
                for key in ['password', 'passwd', 'login_key', 'token', 'key']:
                    if key in log_data:
                        log_data[key] = '********'
        
        logger.debug(f"API Request: {method} {url} - Data: {log_data}")
        
        try:
            async with httpx.AsyncClient(
                follow_redirects=False, 
                verify=self.verify_ssl,
                timeout=timeout
            ) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=data if method == "GET" else None,
                    json=data if method != "GET" else None,
                )
                
                # Check for redirects (often auth issues)
                if response.status_code == 302:
                    location = response.headers.get('location', 'unknown')
                    logger.error(f"API redirect detected: {url} -> {location}")
                    raise DirectAdminError(
                        f"Redirected! Likely auth issue or HTTP/HTTPS mismatch. Location: {location}",
                        status_code=302
                    )
                
                # Try to get JSON response for better error messages
                error_data = None
                try:
                    error_data = response.json()
                except Exception:
                    if response.content:
                        error_data = response.text[:200]  # Truncate long error messages
                
                # Raise exception for error status codes
                response.raise_for_status()
                
                # Parse JSON response
                result = response.json()
                logger.debug(f"API Response: {method} {url} - Status: {response.status_code}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"API HTTP error: {method} {url} - Status: {e.response.status_code} - {str(e)}")
            raise DirectAdminError(
                f"API error: {str(e)}",
                status_code=e.response.status_code,
                response_data=error_data
            )
        except httpx.RequestError as e:
            logger.error(f"API request error: {method} {url} - {str(e)}")
            raise DirectAdminError(f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"API unexpected error: {method} {url} - {str(e)}")
            raise DirectAdminError(f"Unexpected error: {str(e)}")


# Create a default client instance
client = DirectAdminClient()

# Backwards compatible function for existing code
async def call_da_api(path: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Backwards compatible function to call the DirectAdmin API.
    """
    return await client.call_api(path, method, data)