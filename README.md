# cert-manager-mcp-server
MCP Server for cert-manager


Add the following config to Claude Desktop:
```json
{
  "mcpServers": {
    "cert_manager_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/repo/cert-manager-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```
