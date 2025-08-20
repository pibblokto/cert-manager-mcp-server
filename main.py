from utils.config import init_config
init_config()

from tools.server import mcp
from tools.certificates import list_certificates, get_certificate, renew_certificate
from tools.core import list_namespaces, list_contexts, get_current_context, switch_context
from tools.issuers import list_issuers
import logging

if __name__ == "__main__":
    logging.info("Starting cert-manager MCP server...")
    mcp.run()
