import argparse
from kubernetes import client, config
import subprocess
import os

class MCPConfig:
    def __init__(self, cm_version: str, context: str = None, kubeconfig_path: str = None):
        self.cm_version = "_".join(cm_version.split("."))
        self.kubeconfig_path = kubeconfig_path
        if context is None:
            _, current_context = config.list_kube_config_contexts(config_file=kubeconfig_path)
            self.context = current_context["name"]
        else:
            self.context = context
        self.api = None
        self.core = None
        self.refresh_config()

    def _refresh_token(self):
        cmd = ["kubectl"]
        if self.kubeconfig_path:
            cmd += ["--kubeconfig", self.kubeconfig_path]
        if self.context:
            cmd += ["--context", self.context]
        cmd += ["get", "ns", "default", "--request-timeout=10s", "--quiet"]

        subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def refresh_config(self):
        api_client = config.new_client_from_config(
            config_file=self.kubeconfig_path,
            context=self.context,
            persist_config=False,
        )
        self.api = client.CustomObjectsApi(api_client)
        self.core = client.CoreV1Api(api_client)
        self._refresh_token()

    def set_context(self, ctx: str):
        kubeconfig_path = self.kubeconfig_path or os.path.expanduser("~/.kube/config")
        contexts, _ = config.list_kube_config_contexts(config_file=kubeconfig_path)
        if ctx not in [ctx["name"] for ctx in contexts]:
            raise ValueError("Context doesn't exist")
        self.context = ctx

_config : MCPConfig | None = None

def init_config():
    global _config
    parser = argparse.ArgumentParser(
        prog='cert-manager-mcp-server',
        description='MCP server for cert-manager')
    
    parser.add_argument("--cm-release", type=str, default="v1.18", dest="cm_version")
    args = parser.parse_args()

    _config = MCPConfig(cm_version=args.cm_version)

def get_config() -> MCPConfig:
    if _config is None:
        raise RuntimeError("_config: MCPConfig is empty")
    return _config
