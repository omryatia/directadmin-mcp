"""
FastAPI application for DirectAdmin MCP with SSE support and improved error handling.
"""
import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.routing import Mount
import uvicorn

from mcp_instance import mcp
from mcp.server.sse import SseServerTransport
from config import settings, setup_logging
from inspect import getmembers, iscoroutinefunction, signature

# Initialize logger
logger = logging.getLogger(__name__)

# SSE transport
sse = SseServerTransport("/messages/")

# Application startup and shutdown handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Setup phase
    logger.info("=" * 60)
    logger.info("DirectAdmin MCP Server - Application Starting")
    logger.info("=" * 60)
    
    # Create required directories
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Import all tools from the tools package
        import tools
        loaded_modules = tools.load_all_tools()
        logger.info(f"Loaded {len(loaded_modules)} tool modules: {', '.join(loaded_modules)}")
        
        logger.info("Application startup complete")
        yield
    except Exception as e:
        logger.critical(f"Startup error: {str(e)}", exc_info=True)
        sys.exit(1)
    
    # Cleanup phase
    logger.info("=" * 60)
    logger.info("DirectAdmin MCP Server - Application Shutting Down")
    logger.info("=" * 60)

# Create FastAPI application with metadata and lifespan manager
app = FastAPI(
    title="DirectAdmin MCP Server",
    description="Model Context Protocol integration for DirectAdmin control panel",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )

# Mount the /messages path for SSE
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/", tags=["General"])
async def homepage():
    """Root endpoint that returns a simple HTML welcome page."""
    html_content = """
    <!DOCTYPE html>
    <html>
        <head><title>DirectAdmin MCP Server</title></head>
        <body style='font-family:sans-serif;padding:2rem;max-width:800px;margin:auto;'>
            <h1>DirectAdmin MCP Server</h1>
            <p>Welcome to the DirectAdmin MCP integration.</p>
            <div style='background:#f8f9fa;padding:1rem;border-left:4px solid #5bc0de;'>
                <h3>Server Information</h3>
                <p><strong>Status:</strong> Running</p>
                <p><strong>Version:</strong> 1.0.0</p>
                <p><strong>MCP Endpoint:</strong> /sse</p>
                <p><strong>Docs:</strong> <a href='/docs'>/docs</a></p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.get("/about", tags=["General"])
async def about():
    """About endpoint that returns information about the application."""
    return {
        "name": "DirectAdmin MCP Server",
        "version": "1.0.0",
        "description": "Integrating DirectAdmin with Model Context Protocol",
        "endpoints": {
            "mcp": "/sse",
            "docs": "/docs",
            "health": "/health",
        }
    }

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    from da import client
    
    try:
        api_status = await client.call_api("/api/version")
        return {
            "status": "healthy",
            "directadmin": {
                "connected": True,
                "version": api_status.get("version", "unknown")
            },
            "mcp": {
                "status": "running",
                "tools_count": len(await mcp.list_tools())
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "directadmin": {"connected": False, "error": str(e)},
                "mcp": {
                    "status": "running" if mcp else "unknown",
                    "tools_count": len(await mcp.list_tools()) if mcp else 0
                }
            }
        )

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """
    SSE endpoint that connects to the MCP server.
    
    This endpoint establishes a Server-Sent Events connection with the client
    and forwards communication to the Model Context Protocol server.
    """
    logger.info(f"New SSE connection from {request.client.host}")
    try:
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read, write):
            await mcp._mcp_server.run(
                read,
                write,
                mcp._mcp_server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"SSE connection error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"SSE connection error: {str(e)}")

   
@app.get("/mcp/tools", tags=["MCP"])
async def list_all_mcp_tools():
    tools = await mcp.list_tools()
    return {
        "count": len(tools),
        "tools": {
            tool.name: {
                "description": tool.description,
                "parameters": []
            }
            for tool in tools
        }
    }

# Run the FastAPI application with uvicorn when executed directly
if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    # Run server
    logger.info(f"Starting FastAPI server on port {settings.PORT}")
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)