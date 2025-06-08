#!/usr/bin/env python3

import os
import re
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
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            log_files.append(f"{file_path.name} ({size_kb} KB, modified: {mod_time})")
    
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

@server.tool()
async def search_logs(filename: str, pattern: str, lines: int = 20):
    """Search for pattern in log file and return matching lines"""
    file_path = LOGS_DIR / filename
    
    if not file_path.exists():
        return [TextContent(type="text", text=f"❌ File '{filename}' not found")]
    
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    matches = []
    for i, line in enumerate(all_lines, 1):
        if re.search(pattern, line, re.IGNORECASE):
            matches.append((i, line.rstrip()))
    
    if not matches:
        return [TextContent(type="text", text=f"🔍 No matches found for '{pattern}' in {filename}")]
    
    # Limit results
    if len(matches) > lines:
        matches = matches[-lines:]
    
    result = f"🔍 Search results for '{pattern}' in {filename}:\n"
    result += "─" * 50 + "\n"
    
    for line_num, content in matches:
        result += f"{line_num:4d} | {content}\n"
    
    return [TextContent(type="text", text=result)]

@server.tool()
async def filter_by_level(filename: str, level: str = "ERROR"):
    """Filter log entries by level (ERROR, WARN, INFO, DEBUG, CRITICAL)"""
    file_path = LOGS_DIR / filename
    
    if not file_path.exists():
        return [TextContent(type="text", text=f"❌ File '{filename}' not found")]
    
    level = level.upper()
    valid_levels = ["ERROR", "WARN", "INFO", "DEBUG", "CRITICAL"]
    
    if level not in valid_levels:
        return [TextContent(type="text", text=f"❌ Invalid level. Use: {', '.join(valid_levels)}")]
    
    with open(file_path, 'r') as f:
        all_lines = f.readlines()
    
    matches = []
    for i, line in enumerate(all_lines, 1):
        if f'[{level}]' in line:
            matches.append((i, line.rstrip()))
    
    if not matches:
        return [TextContent(type="text", text=f"📊 No {level} entries found in {filename}")]
    
    result = f"📊 {level} entries in {filename} ({len(matches)} found):\n"
    result += "─" * 50 + "\n"
    
    for line_num, content in matches:
        result += f"{line_num:4d} | {content}\n"
    
    return [TextContent(type="text", text=result)]

@server.tool()
async def search_all_logs(pattern: str, max_results: int = 50):
    """Search for pattern across all log files"""
    log_files = list(LOGS_DIR.glob("*.log"))
    
    if not log_files:
        return [TextContent(type="text", text="No .log files found")]
    
    all_matches = []
    
    for file_path in log_files:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                all_matches.append((file_path.name, i, line.rstrip()))
    
    if not all_matches:
        return [TextContent(type="text", text=f"🔍 No matches found for '{pattern}' across all log files")]
    
    # Limit results
    if len(all_matches) > max_results:
        all_matches = all_matches[-max_results:]
    
    result = f"🔍 Search results for '{pattern}' across all logs:\n"
    result += "─" * 50 + "\n"
    
    current_file = ""
    for filename, line_num, content in all_matches:
        if filename != current_file:
            result += f"\n📄 {filename}:\n"
            current_file = filename
        
        result += f"{line_num:4d} | {content}\n"
    
    return [TextContent(type="text", text=result)]

@server.tool()
async def log_summary(filename: str):
    """Generate a summary of log file contents by level and services"""
    file_path = LOGS_DIR / filename
    
    if not file_path.exists():
        return [TextContent(type="text", text=f"❌ File '{filename}' not found")]
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return [TextContent(type="text", text=f"📄 {filename} is empty")]
    
    # Count by level
    levels = {"ERROR": 0, "WARN": 0, "INFO": 0, "DEBUG": 0, "CRITICAL": 0}
    services = {}
    
    for line in lines:
        # Count log levels
        for level in levels:
            if f'[{level}]' in line:
                levels[level] += 1
                break
        
        # Extract service names (text in parentheses)
        service_match = re.search(r'\(([^)]+)\)', line)
        if service_match:
            service = service_match.group(1)
            services[service] = services.get(service, 0) + 1
    
    # Build summary
    result = f"📊 Summary for {filename} ({len(lines)} total lines):\n"
    result += "─" * 50 + "\n"
    
    # Log levels
    result += "📈 Log Levels:\n"
    for level, count in levels.items():
        if count > 0:
            result += f"  {level}: {count}\n"
    
    # Top services
    if services:
        result += "\n🔧 Top Services:\n"
        sorted_services = sorted(services.items(), key=lambda x: x[1], reverse=True)[:5]
        for service, count in sorted_services:
            result += f"  {service}: {count} entries\n"
    
    return [TextContent(type="text", text=result)]

if __name__ == "__main__":
    print("Starting enhanced MCP log server...")
    print("Tools available: list_files, read_file, search_logs, filter_by_level, search_all_logs, log_summary")
    print("Waiting for connections...")
    asyncio.run(server.run())