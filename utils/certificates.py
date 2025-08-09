from .config import get_config
from importlib import import_module
from datetime import datetime, timezone
from kubernetes.client.models import V1NamespaceList
from kubernetes.client import ApiException
from collections import defaultdict
from typing import Any
_mcp_config = get_config()

models = import_module(f"models.{_mcp_config.cm_version}")

def list_certificates(
        namespace_name="", 
        all_namespaces=False, 
        include_domains=False,
        list_expired=False
    ) -> dict[str, list[dict[str, Any]]]:
    
    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    
    def list_domains(crt) -> list[str]:
        domains = crt.spec.dnsNames
        if crt.spec.commonName not in domains:
            domains.append(crt.spec.commonName)
        return domains

    def is_expired(crt) -> bool:
        if crt.status.notAfter and crt.status.notAfter < datetime.now(timezone.utc):
            return True
        return False

    def fetch_for_namespace(ns: str):
        try:
            crt_list_response = _mcp_config.api.list_namespaced_custom_object(
                group="cert-manager.io",
                version="v1",
                namespace=ns,
                plural="certificates"
                )
        except ApiException as e:
            if e.status == 404:
                result[ns] = None
                return
            raise
        else:
            certs = []
            for item in crt_list_response["items"]:
                cert = models.Certificate.model_validate(item)
                if list_expired:
                    if is_expired(cert):
                        certs.append(cert)
                        continue
                else:
                    certs.append(cert)

            for cert in certs:
                result_insertion = {"name": cert.metadata["name"]}
                if include_domains:
                    result_insertion["domains"] = list_domains(cert)
                result[ns].append(result_insertion)

    if all_namespaces:
        namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
        for ns in namespaces.items:
            fetch_for_namespace(ns.metadata.name)
        return result
    
    fetch_for_namespace(namespace_name)
    if not namespace_name:
        raise ValueError("Namespace name is required when all_namespaces=False")
    return result
