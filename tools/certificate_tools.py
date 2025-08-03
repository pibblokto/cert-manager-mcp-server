from tools.server import mcp
from utils.certificates import list_all_certificates

@mcp.tool()
def list_certificates() -> dict[str, list[str]]:
    return list_all_certificates()
