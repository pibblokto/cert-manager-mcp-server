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
