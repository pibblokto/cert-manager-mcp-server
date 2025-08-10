from utils.config import init_config
init_config()

from tools.server import mcp
from tools.certificate_tools import list_certificates, get_certificate
from tools.core_tools import list_namespaces
import logging

if __name__ == "__main__":
    logging.info("Starting cert-manager MCP server...")
    mcp.run()
