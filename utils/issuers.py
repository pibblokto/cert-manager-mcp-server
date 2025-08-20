from .config import get_config
from kubernetes.client import ApiException
from collections import defaultdict
from typing import Any
from kubernetes.client.models import V1NamespaceList

_mcp_config = get_config()

def list_issuers(
        list_cluster_issuers: bool=False,
        all_namespaces: bool=False,
        namespace_name: str=""
) -> dict[str, Any]:
    _mcp_config.refresh_config()
    result: dict[str, Any] = defaultdict(dict)
    
    if list_cluster_issuers:
        try:
            result["cluster_issuers"] = {}
            resp = _mcp_config.api.list_cluster_custom_object(
                group="cert-manager.io",
                version="v1",
                plural="clusterissuers"
            )
        except ApiException as e:
            if e.status == 404:
                return {}
            raise
        else:
            for item in resp["items"]:
                cluster_issuer_name = item["metadata"]["name"]
                item.pop('metadata', None)
                result["cluster_issuers"][cluster_issuer_name] = item
            return result
    
    if all_namespaces:
        namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
        for ns in namespaces.items:
            ns_name = ns.metadata.name
            result[ns_name] = {}
            try:
                resp = _mcp_config.api.list_namespaced_custom_object(
                    group="cert-manager.io",
                    version="v1",
                    namespace=ns_name,
                    plural="issuers"
                )
            except ApiException as e:
                if e.status == 404:
                    return {}
                raise
            else:
                for item in resp["items"]:
                    issuer_name = item["metadata"]["name"]
                    item.pop('metadata', None)
                    result[ns_name][issuer_name] = item
        return result
    
    try:
        if namespace_name == "":
            raise ValueError("Namespace name has to be set")
        resp = _mcp_config.api.list_namespaced_custom_object(
                    group="cert-manager.io",
                    version="v1",
                    namespace=namespace_name,
                    plural="issuers"
                )
    except ApiException as e:
        if e.status == 404:
            return {}
        raise
    else:
        result[namespace_name] = {}
        for item in resp["items"]:
            issuer_name = item["metadata"]["name"]
            item.pop('metadata', None)
            result[namespace_name][issuer_name] = item
