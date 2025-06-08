# LogScribe MCP

A Model Context Protocol (MCP) server for log file management and analysis with enhanced formatting and error handling.

## ✨ Features

- 📁 **List Log Files** - View all .log files with size metadata
- 📖 **Read Log Files** - Read the last N lines with line numbers and formatting
- 🔍 **Search Logs** - Search for patterns within log files using regex
- ✅ **Error Handling** - Graceful handling of missing files and edge cases
- 🎨 **Rich Output** - Formatted output with emojis and visual separators
- 🔧 **Hot Reload** - Auto-restart on file changes during development

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install mcp>=1.9.3 watchdog>=3.0.0
   ```

2. **Create logs directory:**
   ```bash
   mkdir logs
   # Add some .log files to test
   echo "2024-01-01 INFO Application started" > logs/app.log
   ```

3. **Run the server:**
   ```bash
   # Production
   python mcp_server.py
   
   # Development (with hot reload)
   python dev_server.py
   ```

## Available Tools

### `list_files()`
Lists all .log files in the `./logs` directory with file size information.

**Example output:**
```
📁 Log Files:
app.log (2.5 KB)
error.log (1.2 KB)
```

### `read_file(filename: str, lines: int = 10)`
Reads the last N lines from a specified log file with enhanced formatting.

**Parameters:**
- `filename`: Name of the log file (e.g., "app.log")
- `lines`: Number of lines to read from the end (default: 10)

**Example output:**
```
📄 app.log (showing last 3 of 100 lines)
──────────────────────────────────────────────────
  98 | 2024-01-01 10:00:00 INFO Application started
  99 | 2024-01-01 10:01:00 DEBUG Loading configuration
 100 | 2024-01-01 10:02:00 INFO Ready to serve requests
```

### `search_logs(filename: str, pattern: str, lines: int = 20)`
Searches for a pattern within a specific log file using case-insensitive regex.

**Parameters:**
- `filename`: Name of the log file to search
- `pattern`: Search pattern (supports regex)
- `lines`: Maximum number of matching lines to return (default: 20)

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "log-server": {
      "command": "/full/path/to/your/venv/bin/python",
      "args": ["/full/path/to/your/mcp_server.py"],
      "cwd": "/full/path/to/your/project"
    }
  }
}
```

**Example (replace with your actual paths):**
```json
{
  "mcpServers": {
    "log-server": {
      "command": "/Users/username/projects/logscribe-mcp/venv/bin/python",
      "args": ["/Users/username/projects/logscribe-mcp/mcp_server.py"],
      "cwd": "/Users/username/projects/logscribe-mcp"
    }
  }
}
```

## Example Usage

Ask Claude:
- "List all my log files"
- "Show me the last 20 lines from app.log"
- "Read the last 5 lines from error.log"
- "Search for 'ERROR' in app.log"

## Error Handling

The server gracefully handles:
- Missing log files (returns helpful error message)
- Empty log files (indicates file is empty)
- Invalid file paths

## Requirements

- Python 3.8+
- mcp>=1.9.3
- watchdog>=3.0.0 (for development hot reload)

## Development

For development with automatic restart on file changes:
```bash
python dev_server.py
```

The development server will automatically restart when you modify any `.py` files, making it easier to test changes without manually restarting.