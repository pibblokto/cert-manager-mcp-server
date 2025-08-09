from utils.config import init_config
init_config()

from tools.server import mcp
from tools.certificate_tools import list_all_certificates
import logging
from utils.certificates import list_all_certificates

if __name__ == "__main__":
    logging.info("Starting cert-manager MCP server...")
    print(list_all_certificates())
    mcp.run()
