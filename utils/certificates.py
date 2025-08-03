from .config import get_config
from importlib import import_module
from kubernetes.client.models import V1NamespaceList
from collections import defaultdict
# import models.v1_18 as models
_mcp_config = get_config()

models = import_module(f"models.{_mcp_config.cm_version}")

def list_all_certificates() -> dict[str, list[str]]:
    result: dict[str|list[str]] = defaultdict(list)
    namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
    for ns in namespaces.items:
        ns_name = ns.metadata.name
        crt_list_response = _mcp_config.api.list_namespaced_custom_object(
            group="cert-manager.io",
            version="v1",
            namespace=ns_name,
            plural="certificates"
        )
        certs = [models.Certificate.model_validate(item) for item in crt_list_response["items"]]
        for cert in certs:
            result[ns_name].append(cert.metadata["name"])
    return result
