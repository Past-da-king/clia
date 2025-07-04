from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "CliSweAiTools",
    description="A toolset for an AI to perform software engineering tasks on the command line.",
)

# Import all tool modules to register them with the FastMCP instance
from swe_tools import cli_commander
from swe_tools import codebase_restorer
from swe_tools import codebase_snapshot_generator
from swe_tools import directory_tree_viewer
from swe_tools import file_deleter
from swe_tools import file_fetcher
from swe_tools import line_editor
from swe_tools import utils
