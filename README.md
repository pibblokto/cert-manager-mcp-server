# cert-manager-mcp-server
MCP server for management and troubleshooting of certificates and other resources managed by [cert-manager](https://github.com/cert-manager/cert-manager). 


Claude Desktop config:
```json
{
  "mcpServers": {
    "cert-manager-mcp-server": {
      "command": "sh",
      "args": [
        "-c",
        "docker run -i --rm -v ~/.kube:/home/app/.kube:ro -v ~/.config/gcloud:/home/app/.config/gcloud piblokto/cert-manager-mcp-server:v0.0.5"
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
      "command": "sh",
      "args": [
        "-c",
        "docker run -i --rm -v ~/.kube:/home/app/.kube:ro -v ~/.config/gcloud:/home/app/.config/gcloud -e CLOUDSDK_CORE_PROJECT=<DEFAULT_PROJECT_ID> -e CLOUDSDK_COMPUTE_REGION=<DEFAULT_COMPUTE_REGION> piblokto/cert-manager-mcp-server:v0.0.5"
      ]
    }
  }
}
```

# Tools

This MCP server provides the following tools for interacting with cert-manager and Kubernetes resources:

## Certificate Management
- **list_certificates** - List certificates within a namespace or across all namespaces, with options for filtering expired certificates and pagination. You can also include domains for listed certificates with include_domains argument (defaults to False to make responses more compact)
- **get_certificate** - Get detailed information about a specific certificate
- **renew_certificate** - Force renewal of a certificate

## Issuer Management
- **list_issuers** - List issuers or cluster issuers with their statuses and configuration. Unlike **list_certificates** there are no pagination or filtering except for cluster/namespaced issuers and namespaces for Issuers.

## Kubernetes Context Management
- **list_namespaces** - List all namespaces in the cluster
- **list_contexts** - List all available kubeconfig contexts
- **get_current_context** - Get the currently active kubeconfig context
- **switch_context** - Switch to a different kubeconfig context. Updates in-memory config

## Available Tools

| Tool Name | Description | Read-Only | Parameters |
|-----------|-------------|-----------|------------|
| `list_certificates` | List certificates within a namespace or all namespaces, with filtering and pagination options | ✅ | `namespace_name`, `all_namespaces`, `include_domains`, `list_expired`, `cursor`, `page_size` |
| `get_certificate` | Get detailed information about a specific certificate | ✅ | `namespace_name`, `certificate_name` |
| `renew_certificate` | Force renewal of a certificate in a given namespace | ❌ | `namespace_name`, `certificate_name` |
| `list_issuers` | List issuers or cluster issuers with their statuses and configuration | ✅ | `list_cluster_issuers`, `all_namespaces`, `namespace_name` |
| `list_namespaces` | List all namespaces in the cluster | ✅ | None |
| `list_contexts` | List all available kubeconfig contexts | ✅ | None |
| `get_current_context` | Get the currently active kubeconfig context | ✅ | None |
| `switch_context` | Switch to a different kubeconfig context | ✅ | `ctx` |

## Hosted deployment

A hosted deployment is available on [Fronteir AI](https://fronteir.ai/mcp/pibblokto-cert-manager-mcp-server).

