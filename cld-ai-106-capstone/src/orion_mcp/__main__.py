"""Console entry point for the orion-mcp server."""
from .server import mcp

def main():
    mcp.run()  # stdio transport

if __name__ == "__main__":
    main()
