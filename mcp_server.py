#!/usr/bin/env python3

import os
import asyncio
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# Initialize server
server = FastMCP("log-server")
LOGS_DIR = Path(__file__).parent / "logs"

@server.tool()
async def list_files():
    """List all .log files in ./logs directory with metadata"""
    log_files = []
    
    for file_path in LOGS_DIR.glob("*.log"):
        if file_path.is_file():
            stat = file_path.stat()
            size_kb = round(stat.st_size / 1024, 2)
            log_files.append(f"{file_path.name} ({size_kb} KB)")
    
    if not log_files:
        return [TextContent(type="text", text="No .log files found")]
    
    return [TextContent(type="text", text="📁 Log Files:\n" + "\n".join(log_files))]

@server.tool()
async def read_file(filename: str, lines: int = 10):
    """Read last N lines from a log file with formatted output"""
    file_path = LOGS_DIR / filename
    
    if not file_path.exists():
        return [TextContent(type="text", text=f"❌ File '{filename}' not found")]
    
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    if not all_lines:
        return [TextContent(type="text", text=f"📄 {filename} is empty")]
    
    last_lines = all_lines[-lines:]
    total_lines = len(all_lines)
    
    result = f"📄 {filename} (showing last {len(last_lines)} of {total_lines} lines)\n"
    result += "─" * 50 + "\n"
    
    for i, line in enumerate(last_lines, 1):
        line_num = total_lines - len(last_lines) + i
        result += f"{line_num:4d} | {line.rstrip()}\n"
    
    return [TextContent(type="text", text=result)]

if __name__ == "__main__":
    print("Starting enhanced MCP log server...")
    print("Tools available: list_files, read_file")
    print("Waiting for connections...")
    asyncio.run(server.run())