# LogScribe MCP

A Model Context Protocol (MCP) server for log file management and analysis with enhanced formatting and error handling.

## ✨ Features

- 📁 **List Log Files** - View all .log files with size metadata
- 📖 **Read Log Files** - Read the last N lines with line numbers and formatting
- ✅ **Error Handling** - Graceful handling of missing files and edge cases
- 🎨 **Rich Output** - Formatted output with emojis and visual separators

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install mcp>=1.9.3
   ```

2. **Create logs directory:**
   ```bash
   mkdir logs
   # Add some .log files to test
   echo "2024-01-01 INFO Application started" > logs/app.log
   ```

3. **Run the server:**
   ```bash
   python mcp_server.py
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

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "logscribe": {
      "command": "python",
      "args": ["/full/path/to/your/mcp_server.py"]
    }
  }
}
```

## Example Usage

Ask Claude:
- "List all my log files"
- "Show me the last 20 lines from app.log"
- "Read the last 5 lines from error.log"

## Error Handling

The server gracefully handles:
- Missing log files (returns helpful error message)
- Empty log files (indicates file is empty)
- Invalid file paths

## Requirements

- Python 3.8+
- mcp>=1.9.3
