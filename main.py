from utils.config import init_config
init_config()

from tools.server import mcp
from tools.certificate_tools import list_certificates
from tools.core_tools import list_namespaces
import logging
#from utils import certificates

if __name__ == "__main__":
    logging.info("Starting cert-manager MCP server...")
    #certificates.list_certificates(namespace_name="traefik",list_expired=True)
    mcp.run()
