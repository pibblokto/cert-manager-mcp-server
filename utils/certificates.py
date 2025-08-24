from .config import get_config
from datetime import datetime, timezone
from time import time
from kubernetes.client.models import V1NamespaceList
from kubernetes.client import ApiException
from collections import defaultdict
from typing import Any
from copy import deepcopy
import models.v1_18 as models

_mcp_config = get_config()

_CERT_CACHE: dict[str, dict[str, Any]] = {}
_CACHE_TTL = 300

def clear_cert_cache(namespace_name: str | None = None) -> None:
    if namespace_name is None:
        _CERT_CACHE.clear()
    else:
        _CERT_CACHE.pop(namespace_name, None)

def list_certificates(
        namespace_name: str = "",
        all_namespaces: bool = False,
        include_domains: bool = False,
        list_expired: bool = False,
        cursor: int = -1,
        page_size: int = 100,
        sort_by_domain: str = ""
    ) -> dict[str, str | dict[str, None | str | int | list[dict[str, Any]]]]:
    _mcp_config.refresh_config()
    result: dict[str, str | dict[str, None | str | int | list[dict[str, Any]]]] = defaultdict(dict)

    def list_domains(crt: models.Certificate) -> list[str]:
        domains = crt.spec.dnsNames if crt.spec.dnsNames else []
        if crt.spec.commonName not in domains:
            domains.append(crt.spec.commonName)
        return domains

    def is_expired(crt: models.Certificate) -> bool:
        return bool(crt.status.notAfter and crt.status.notAfter < datetime.now(timezone.utc))

    def is_for_domain(crt: models.Certificate, domain_name: str) -> bool:
        domains = list_domains(crt)
        if domain_name in domains:
            return True
        return False

    def fetch_all_for_namespace(ns: str) -> list[dict[str, Any]]:
        certs_out = []
        try:
            resp = _mcp_config.api.list_namespaced_custom_object(
                group="cert-manager.io",
                version="v1",
                namespace=ns,
                plural="certificates"
            )
        except ApiException as e:
            if e.status == 404:
                result[ns] = None
                return []
            raise
        else:
            for item in resp["items"]:
                cert = models.Certificate.model_validate(item)
                if sort_by_domain != "" and not is_for_domain(crt=cert, domain_name=sort_by_domain):
                    continue
                if list_expired and not is_expired(cert):
                    continue
                entry = {"name": cert.metadata["name"]}
                if include_domains or cursor >= 0:
                    entry["domains"] = list_domains(cert)
                certs_out.append(entry)
            return certs_out

    if all_namespaces:
        namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
        for ns in namespaces.items:
            name = ns.metadata.name
            certs = fetch_all_for_namespace(name)
            result[name]["certs"] = certs
            result[name]["certs_count"] = len(certs)
        return result

    if not namespace_name:
        raise ValueError("Namespace name is required when all_namespaces=False")

    if cursor == -1:
        certs = fetch_all_for_namespace(namespace_name)
        result[namespace_name]["certs"] = certs
        result[namespace_name]["certs_count"] = len(certs)
        result[namespace_name]["next_cursor"] = None
        return result

    now = time()
    cache_entry = _CERT_CACHE.get(namespace_name)
    if not cache_entry or (now - cache_entry["ts"]) > _CACHE_TTL:
        _CERT_CACHE[namespace_name] = {
            "ts": now,
            "items": fetch_all_for_namespace(namespace_name)
        }

    items = _CERT_CACHE[namespace_name]["items"]
    start = cursor
    end = cursor + page_size
    page_items = None
    if include_domains:
        page_items = items[start:end]
    else:
        page_items = [{"name": item["name"]} for item in items[start:end]]
    next_cursor = end if end < len(items) else None

    result[namespace_name]["certs"] = page_items
    result[namespace_name]["certs_count"] = len(items)
    result[namespace_name]["next_cursor"] = next_cursor

    if next_cursor is None:
        _CERT_CACHE.pop(namespace_name, None)

    return result

def get_certificate(namespace_name: str = "", certificate_name: str = "") -> dict[str, Any]:
    _mcp_config.refresh_config()
    result: dict[str, Any] = defaultdict(dict)
    try:
        if namespace_name == "" or certificate_name == "":
            raise ValueError("Both namespace_name and certificate_name are required")
        resp = _mcp_config.api.get_namespaced_custom_object(
            group="cert-manager.io",
            version="v1",
            namespace=namespace_name,
            plural="certificates",
            name=certificate_name
        )
    except ApiException as e:
        if e.status == 404:
            result = {}
            return result
    else:
        cert = models.Certificate.model_validate(resp)
        result["validNotAfter"] = cert.status.notAfter
        result["dateNow"] = datetime.now(timezone.utc)
        result["issuer"] = {
            "kind": cert.spec.issuerRef.kind,
            "name": cert.spec.issuerRef.name
        }
        domains = cert.spec.dnsNames
        if cert.spec.commonName not in domains:
            domains.append(cert.spec.commonName)
        result["domains"] = domains
        result["kubernetesSecret"] = cert.spec.secretName
        return result

def renew_certificate(namespace_name: str, certificate_name: str):
    _mcp_config.refresh_config()
    try:
        resp = _mcp_config.api.get_namespaced_custom_object(
            group="cert-manager.io",
            version="v1",
            namespace=namespace_name,
            plural="certificates",
            name=certificate_name
        )
    except ApiException as e:
        if e.status == 404:
            result = {}
            return result
    else:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        observed_generation = resp["metadata"]["generation"]

        new_condition = {
            "type": "Issuing",
            "status": "True",
            "reason": "ManuallyTriggered",
            "message": "Certificate re-issuance manually triggered",
            "observedGeneration": observed_generation,
            "lastTransitionTime": now,
        }

        status = deepcopy(resp.get("status", {}))
        conditions = list(status.get("conditions") or [])
        idx = next((i for i, c in enumerate(conditions) if c.get("type") == "Issuing"), None)

        if idx is not None:
            old = conditions[idx]
            if str(old.get("status")) == "True" and old.get("lastTransitionTime"):
                new_condition["lastTransitionTime"] = old["lastTransitionTime"]
            conditions[idx] = new_condition
        else:
            conditions.append(new_condition)

        status["conditions"] = conditions
        try:
            _mcp_config.api.patch_namespaced_custom_object_status(
                group="cert-manager.io",
                version="v1",
                namespace=namespace_name,
                plural="certificates",
                name=certificate_name,
                body={"status": status},
            )
        except ApiException as e:
            raise
