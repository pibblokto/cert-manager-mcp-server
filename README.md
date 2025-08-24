# cert-manager-mcp-server
This local MCP server lets you troubleshoot and interact with certificate and other resources managed by [cert-manager](https://github.com/cert-manager/cert-manager). 



Claude Desktop config:
```json
{
  "mcpServers": {
    "cert-manager-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "~/.kube:/home/app/.kube:ro",
        "piblokto/cert-manager-mcp-server:latest"
      ]
    }
  }
}
```

Claude Desktop config for GKE clusters:
```json
{
  "mcpServers": {
    "cert-manager-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "~/.kube:/home/app/.kube:ro",
        "-v",
        "~/.config/gcloud:/home/app/.config/gcloud",
        "-e",
        "CLOUDSDK_CORE_PROJECT=<YOUR_GCP_PROJECT>",
        "-e",
        "CLOUDSDK_COMPUTE_REGION=<DEFAULT_GCP_REGION>",
        "piblokto/cert-manager-mcp-server:latest"
      ]
    }
  }
}
```
