from swe_tools.__init__ import mcp

# This file is primarily for local development/testing of the MCP server
# It is not used when the MCP server is mounted within the FastAPI app.

if __name__ == "__main__":
    # This will run the FastMCP server as a standalone application
    # It will listen on stdio by default.
    mcp.run()