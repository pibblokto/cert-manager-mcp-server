# cert-manager-mcp-server
MCP Server for cert-manager


Add the following config to Claude Desktop:
```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "~/.kube:/home/appuser/.kube:ro",
        "-v",
        "~/.config/gcloud:/home/appuser/.config/gcloud:ro",
        "-e",
        "CLOUDSDK_CORE_PROJECT=<YOUR_GCP_PROJECT>",
        "-e",
        "CLOUDSDK_COMPUTE_REGION=<DEFAULT_GCP_REGION",
        "piblokto/cert-manager-mcp-server:latest"
      ]
    }
  }
}
```
