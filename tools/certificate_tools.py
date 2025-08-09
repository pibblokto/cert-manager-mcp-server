from tools.server import mcp
from utils import certificates
from typing import Any

@mcp.tool(
        description="List certificates within provided namespace_name namespace or within all namespaces if all_namespaces=True (defaults to False, if True ns_name is ignored). " \
        "If include_domains is True, each certificate will be listen along with domains for which it was supposed to be issued (defaults to False). If list_expired is True " \
        "only expired certificates will be listed",
        annotations={
            "title": "List Certificates",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def list_certificates(namespace_name="", all_namespaces=False, include_domains=False, list_expired=False) -> dict[str, list[dict[str, Any]]]:
    return certificates.list_certificates(namespace_name, all_namespaces, include_domains, list_expired)
