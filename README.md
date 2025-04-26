# DirectAdmin MCP Server

[![version](https://img.shields.io/badge/version-0.1.1-blue.svg)](https://github.com/omryatia/directadmin-mcp)

A Model Context Protocol (MCP) server for DirectAdmin integration, allowing AI assistants to interact with DirectAdmin through natural language.

## Features

- **MCP Integration**: Connect AI assistants to DirectAdmin using the Model Context Protocol
- **RESTful API**: Comprehensive API for DirectAdmin management
- **Server-Sent Events (SSE)**: Real-time communication with clients
- **Tool-based Architecture**: Modular design with tool-based commands
- **Command-line Client**: Included client for testing and scripting
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Architecture

This project implements a server that acts as a bridge between AI assistants and DirectAdmin:

```
┌──────────┐     ┌─────────────────┐     ┌────────────┐
│   AI     │     │  DirectAdmin    │     │ DirectAdmin│
│ Assistant├────►│  MCP Server     ├────►│   API      │
└──────────┘     └─────────────────┘     └────────────┘
      MCP                SSE                 HTTP
```

The server exposes DirectAdmin functionality through a tool-based interface, making it easy for AI assistants to understand and interact with DirectAdmin operations.

## Prerequisites

- Python 3.12+
- DirectAdmin server with API access
- DirectAdmin login key (preferred) or username/password

## Installation

### Option 1: Standard Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/omryatia/directadmin-mcp.git
   cd directadmin-mcp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create configuration:
   ```bash
   cp .gitignore.sample .gitignore
   cp .env.sample .env
   # Edit .env with your DirectAdmin settings
   ```

### Option 2: Docker Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/omryatia/directadmin-mcp.git
   cd directadmin-mcp
   ```

2. Create configuration:
   ```bash
   cp .env.sample .env
   # Edit .env with your DirectAdmin settings
   ```

3. Build and start with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Configuration

Edit the `.env` file with your DirectAdmin credentials:

```ini
# DirectAdmin Settings
DA_URL=https://your-directadmin-server:2222
DA_USERNAME=admin
DA_LOGIN_KEY=your_directadmin_login_key_here/password

# Server Settings
PORT=8888
LOG_LEVEL=INFO
DEBUG=false

# SSL Settings
SSL_VERIFY=true
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `DA_URL` | DirectAdmin server URL with port | (Required) |
| `DA_USERNAME` | DirectAdmin username | (Required) |
| `DA_LOGIN_KEY` | DirectAdmin login key | (Required) |
| `PORT` | Port to run the MCP server on | 8888 |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `DEBUG` | Enable debug mode for development | false |
| `SSL_VERIFY` | Verify SSL certificates for DirectAdmin API calls | true |

## Usage

### Starting the Server

You can start the server in two ways:

1. Using FastAPI with SSE support (recommended):
   ```bash
   python main.py
   ```

2. Using the simple MCP server:
   ```bash
   python server.py
   ```

The server will start on port 8888 by default (configurable in .env).

### Using the Command-line Client

The included command-line client allows you to interact with the MCP server:

```bash
# Get server info
python client.py --info

# Check server health
python client.py --health

# Send a specific message
python client.py "Show me the version of DirectAdmin"

# Interactive mode
python client.py
```

#### Client Options

| Option | Description |
|--------|-------------|
| `--server`, `-s` | MCP server URL |
| `--key`, `-k` | API key for authentication |
| `--no-verify` | Disable SSL verification |
| `--timeout`, `-t` | Request timeout in seconds |
| `--info`, `-i` | Get server info |
| `--health` | Check server health |

### Connecting AI Assistants

Configure your AI assistant to use the MCP endpoint:

```
http://your-server:8888/sse
```

This allows the AI assistant to:
1. Query DirectAdmin information
2. Execute DirectAdmin commands
3. Receive real-time updates

## Available Tools

The server exposes the following DirectAdmin operations as tools:

### System Management
- `api_restart`: Restart DirectAdmin
- `api_ping`: Check if DirectAdmin is running

### Version Control
- `api_get_version`: Get DirectAdmin version information
- `api_version_update`: Update DirectAdmin to the latest version
- `api_change_update_channel`: Change update channel

### System Updates
- `api_system_packages_updates`: Get available system package updates
- `api_system_packages_update_test`: Test system package update
- `api_system_packages_update_run`: Run system package update

### Security
- `api_security_txt_status`: Check security.txt status
- `api_security_txt_get`: Get security.txt content
- `api_security_txt_update`: Update security.txt content

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root page with HTML welcome message |
| `/about` | GET | Server information |
| `/health` | GET | Health check endpoint |
| `/sse` | GET | MCP SSE connection endpoint |
| `/messages` | POST | Internal endpoint for posting SSE messages |

## Development

### Project Structure

```
directadmin-mcp/
├── README.md               # Project documentation
├── .env.sample             # Environment variables template
├── config.py               # Configuration module
├── main.py                 # FastAPI application with SSE support
├── server.py               # Simple MCP server
├── client.py               # Command-line client
├── da.py                   # DirectAdmin API client
├── mcp_instance.py         # MCP instance configuration
├── tools/                  # Tool modules directory
│   ├── __init__.py         # Tool loading mechanism
│   ├── common.py           # Common tool utilities
│   ├── misc.py             # Misc DirectAdmin operations
│   ├── security_txt.py     # Security.txt related tools
│   ├── system_update.py    # System update tools
│   └── versioning.py       # Versioning and update tools
│   └── and alot more ......
└── requirements.txt        # Project dependencies
```

### Adding New Tools

1. Create or edit a file in the `tools` directory
2. Add a new function with the `@mcp.tool()` decorator:

```python
import logging
from mcp_instance import mcp
from da import call_da_api
from tools.common import log_tool_call, format_response

@mcp.tool()
@log_tool_call
async def my_new_tool(param1, param2):
    """
    Tool documentation.
    
    Args:
        param1: First parameter description
        param2: Second parameter description
        
    Returns:
        Description of the return value
    """
    # Implementation
    response = await call_da_api("/api/endpoint", method="GET")
    return format_response(response)
```

The tool will be automatically discovered and registered when the server starts.

### Logging

The server uses a comprehensive logging system:

- Console logs: Shown in the terminal
- File logs: Written to the `logs` directory
- Error logs: Separate file for error tracking

Log levels can be configured in the `.env` file with the `LOG_LEVEL` variable.

## Docker Deployment

The project includes Docker support for easy deployment:

```bash
# Build the image
docker build -t directadmin-mcp .

# Run the container
docker run -d \
  -p 8888:8888 \
  --env-file .env \
  --name directadmin-mcp \
  directadmin-mcp
```

Or more simply with Docker Compose:

```bash
docker-compose up -d
```

## Security Considerations

- Use HTTPS with a valid SSL certificate in production
- Set up proper firewall rules to restrict access
- Use a reverse proxy (like Nginx) with proper security headers
- Keep your DirectAdmin login key secure and rotate it regularly
- Consider adding authentication to the MCP server for production use

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Verify that your DirectAdmin server is accessible
2. Check that your DirectAdmin API credentials are correct
3. Ensure the DirectAdmin API is enabled
4. Check your SSL settings if using HTTPS

### Common Error Messages

- "Authentication failed": Check your DirectAdmin credentials
- "SSL verification failed": Set `SSL_VERIFY=false` in .env or fix your certificates
- "Tool not found": Ensure the tool module is correctly loaded
- "Connection refused": Check that DirectAdmin is running and accessible

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [DirectAdmin](https://www.directadmin.com/)
- [DirectAdmin Api Swagger](https://demo.directadmin.com:2222/evo/api-docs)
- [DirectAdmin Api Swagger Json](https://demo.directadmin.com:2222/docs/swagger.json)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SSE Client](https://github.com/btubbs/sseclient)