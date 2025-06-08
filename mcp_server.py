#!/usr/bin/env python3

import os
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Initialize server
server = FastMCP("log-server")
LOGS_DIR = Path(__file__).parent / "logs"

@server.tool()
async def list_files():
    """List all .log files in ./logs directory"""
    log_files = list(LOGS_DIR.glob("*.log"))
    files = [f.name for f in log_files if f.is_file()]
    
    if not files:
        return [TextContent(type="text", text="No .log files found")]
    
    return [TextContent(type="text", text="\n".join(files))]

@server.tool()
async def read_file(filename: str, lines: int = 10):
    """Read last N lines from a log file"""
    file_path = LOGS_DIR / filename
    
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    last_lines = all_lines[-lines:]
    content = "".join(last_lines)
    
    return [TextContent(type="text", text=content)]

if __name__ == "__main__":
    print("Starting MCP log server...")
    print("Tools available: list_files, read_file")
    print("Waiting for connections...")
    asyncio.run(server.run())