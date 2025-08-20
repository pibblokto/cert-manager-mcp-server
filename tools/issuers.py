from tools.server import mcp
from utils import issuers
from typing import Any

@mcp.tool(
        description="Lists issuers (or cluster issuers) along with their statuses and configuration. If list_cluster_issuers is true, then all_namespaces and namespace_name" \
        "are ignored. If all_namespaces is true, then namespace_name is ignored",
        annotations={
            "title": "List issuers",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def list_issuers(
    list_cluster_issuers: bool=False,
    all_namespaces: bool=False,
    namespace_name: str=""
    ) -> dict[str, Any]:
    return issuers.list_issuers(list_cluster_issuers, all_namespaces, namespace_name)
