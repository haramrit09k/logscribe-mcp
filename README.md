# LogScribe MCP

A Model Context Protocol (MCP) server for log file management and analysis with enhanced formatting and error handling.

## ✨ Features

- 📁 **List Log Files** - View all .log files with size and modification metadata
- 📖 **Read Log Files** - Read the last N lines with line numbers and formatting
- 🔍 **Search Individual Files** - Search for patterns within specific log files
- 🌐 **Cross-File Search** - Search patterns across all log files simultaneously
- 🏷️ **Filter by Log Level** - Filter entries by ERROR, WARN, INFO, DEBUG, CRITICAL
- 📊 **Generate Analytics** - Comprehensive log file summaries and statistics
- ✅ **Error Handling** - Graceful handling of missing files and edge cases
- 🎨 **Rich Output** - Formatted output with emojis and visual separators
- 🔧 **Hot Reload** - Auto-restart on file changes during development

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create logs directory (optional):**
   ```bash
   mkdir logs
   # Add some .log files to test
   echo "2024-01-01 INFO Application started" > logs/app.log
   ```
   (You could also use sample logs in the logs folder to get started.)

3. **Run the server (SSE via uvicorn):**
   ```bash
   # Use default ./logs directory
   python mcp_server.py

   # The server uses uvicorn and exposes an SSE endpoint at
   # http://localhost:8000/log-server
   
   # Use custom logs directory (command line)
   python mcp_server.py /path/to/your/logs
   
   # Use custom logs directory (environment variable)
   LOGS_DIR="/path/to/your/logs" python mcp_server.py
   
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

### `search_all_logs(pattern: str, max_results: int = 50)`
Searches for a pattern across ALL log files simultaneously.

**Parameters:**
- `pattern`: Search pattern (supports regex)
- `max_results`: Maximum number of matching lines to return (default: 50)

### `log_summary(filename: str)`
Generates comprehensive analytics and statistics for a log file.

**Parameters:**
- `filename`: Name of the log file to analyze

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

**Option 1: Default logs directory**
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

**Option 2: Custom logs directory (command line)**
```json
{
  "mcpServers": {
    "log-server": {
      "command": "/full/path/to/your/venv/bin/python",
      "args": ["/full/path/to/your/mcp_server.py", "/path/to/your/logs"],
      "cwd": "/full/path/to/your/project"
    }
  }
}
```

**Option 3: Custom logs directory (environment variable)**
```json
{
  "mcpServers": {
    "log-server": {
      "command": "/full/path/to/your/venv/bin/python",
      "args": ["/full/path/to/your/mcp_server.py"],
      "cwd": "/full/path/to/your/project",
      "env": {
        "LOGS_DIR": "/path/to/your/logs"
      }
    }
  }
}
```

## Configuration

### Logs Directory

The server supports three ways to specify where your log files are located:

1. **Default**: Uses `./logs` directory in the project folder
2. **Command Line**: Pass directory path as first argument
   ```bash
   python mcp_server.py /var/log/myapp
   ```
3. **Environment Variable**: Set `LOGS_DIR` environment variable
   ```bash
   export LOGS_DIR="/var/log/myapp"
   python mcp_server.py
   ```

Priority order: Command Line > Environment Variable > Default

## Example Usage

Ask Claude:
- "List all my log files"
- "Show me the last 20 lines from app.log"
- "Read the last 5 lines from error.log"
- "Search for 'ERROR' in app.log"
- "Show me all ERROR entries in app.log"
- "Search for 'PaymentService' across all my logs"
- "Generate a summary of app.log"

## Error Handling

The server gracefully handles:
- Missing log files (returns helpful error message)
- Empty log files (indicates file is empty)
- Invalid file paths

## Requirements

- Python 3.8+
- mcp>=1.9.3
- watchdog>=3.0.0 (for development hot reload)
- pytest>=8.4.0 (for running tests)

## Testing

Run the included tests to verify everything works:

```bash
# Simple test runner
python tests/test_basic.py

# Or using pytest (install first: pip install pytest)
pytest tests/ -v
```

Tests cover:
- Server initialization and configuration
- Log directory selection logic (env vars, command line args)
- Basic functionality verification

## Development

For development with automatic restart on file changes:
```bash
python dev_server.py
```

The development server will automatically restart when you modify any `.py` files, making it easier to test changes without manually restarting.