from utils.config import init_config
init_config()

from tools.server import mcp
from tools.certificate import list_certificates, get_certificate, renew_certificate
from tools.core import list_namespaces, list_contexts, get_current_context, switch_context
import logging

if __name__ == "__main__":
    logging.info("Starting cert-manager MCP server...")
    mcp.run()
