from tools.server import mcp
from utils import certificates
from typing import Any

@mcp.tool(
        description="List certificates within provided namespace_name namespace or within all namespaces if all_namespaces=True (defaults to False, if True ns_name is ignored). " \
        "If include_domains is True, each certificate will be listen along with domains for which it was supposed to be issued (defaults to False). If list_expired is True " \
        "only expired certificates will be listed. Argumet cursor represents offset and is used along with page_size (number of certs per fetch) if there are too many certificates in namespace" \
        "(defaults to -1 in which case everything will be fetched. If you want to use pagination start with 0)",
        annotations={
            "title": "List Certificates",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def list_certificates(
    namespace_name: str="", 
    all_namespaces: bool=False, 
    include_domains: bool=False, 
    list_expired: bool=False,
    cursor: int=-1,
    page_size: int=25
    ) -> dict[str, str | dict[str, None | str | int | list[dict[str, Any]]]]:
    certs_response = certificates.list_certificates(
        namespace_name, 
        all_namespaces, 
        include_domains, 
        list_expired,
        cursor,
        page_size
    )
    total_count = 0
    for ns_data in certs_response.values():
        if isinstance(ns_data, dict):
            total_count += ns_data.get("certs_count", 0)
    
    if cursor == -1 and total_count > 200:
        return {"WARNING": f"There are {total_count} certificates in response. " \
        "It's suggested to use pagination and load handful of certs per prompt while listing certs within single namespace"
        }
    return certs_response

@mcp.tool(
        description="Gets detailed information about certificate. Both namespace_name and resource_name (name of certificate) are required",
        annotations={
            "title": "Get Certificate",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
)
def get_certificate(namespace_name: str = "", resource_name: str = "") -> dict[str, Any]:
    return certificates.get_certificate(namespace_name, resource_name)
