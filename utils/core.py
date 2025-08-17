from .config import get_config, MCPConfig
from kubernetes.client import ApiException
from kubernetes.client.models import V1NamespaceList
from kubernetes import config
from typing import Any
import os

_mcp_config = get_config()

def list_namespaces() -> list[str]:
    _mcp_config.refresh_config()
    result = []
    try:
        namespaces: V1NamespaceList = _mcp_config.core.list_namespace()
    except ApiException as e:
        raise
    else:
        for ns in namespaces.items:
            result.append(ns.metadata.name)
        return result

def list_contexts(kubeconfig_path: str = None) -> list[str]:
    kubeconfig_path = kubeconfig_path or os.path.expanduser("~/.kube/config")
    contexts, _ = config.list_kube_config_contexts(config_file=kubeconfig_path)
    return [ctx["name"] for ctx in contexts]

def get_current_context() -> str:
    return _mcp_config.context

def switch_context(ctx: str):
    _mcp_config.set_context(ctx)
    _mcp_config.refresh_config()
