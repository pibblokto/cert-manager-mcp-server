from .config import get_config
from kubernetes.client import ApiException
from kubernetes.client.models import V1NamespaceList

_mcp_config = get_config()

def list_namespaces() -> list[str]:
    result = []
    try:
        namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
    except ApiException as e:
        raise
    else:
        for ns in namespaces.items:
            result.append(ns.metadata.name)
        return result
