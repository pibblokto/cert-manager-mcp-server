import argparse
from kubernetes import client, config

class MCPConfig():
    def __init__(self, cm_version: str):
        config.load_kube_config()
        self.cm_version = "_".join(cm_version.split("."))
        self.api = client.CustomObjectsApi()
        self.core = client.CoreV1Api()

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
