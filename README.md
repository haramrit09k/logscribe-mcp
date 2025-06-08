# LogScribe MCP

A Model Context Protocol (MCP) server for log file management and analysis.

## Features

- 📁 **List Log Files** - View all .log files in your logs directory
- 📖 **Read Log Files** - Read the last N lines from any log file

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install mcp>=1.9.3
   ```

2. **Create logs directory:**
   ```bash
   mkdir logs
   ```

3. **Run the server:**
   ```bash
   python mcp_server.py
   ```

## Available Tools

### `list_files()`
Lists all .log files in the `./logs` directory.

### `read_file(filename: str, lines: int = 10)`
Reads the last N lines from a specified log file.

**Parameters:**
- `filename`: Name of the log file (e.g., "app.log")
- `lines`: Number of lines to read from the end (default: 10)

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "logscribe": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"]
    }
  }
}
```

## Example Usage

Ask Claude:
- "List all my log files"
- "Show me the last 20 lines from app.log"

## Requirements

- Python 3.8+
- mcp>=1.9.3