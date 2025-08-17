from tools.server import mcp
from utils import core

@mcp.tool(
        description="List all namespaces in cluster",
        annotations={
            "title": "List Namespaces",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def list_namespaces() -> list[str]:
    return core.list_namespaces()

@mcp.tool(
        description="List all kubeconfig contexts",
        annotations={
            "title": "List contexts",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def list_contexts() -> list[str]:
    return core.list_contexts()

@mcp.tool(
        description="Get current kubeconfig context",
        annotations={
            "title": "Get current context",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def get_current_context() -> str:
    return core.get_current_context()

@mcp.tool(
        description="Switch kubeconfig context",
        annotations={
            "title": "Switch current context",
            "readOnlyHint": False,
            "openWorldHint": True,
        }
)
def switch_context(ctx: str):
    core.switch_context(ctx)
