#!/usr/bin/env python3

from mcp_server import server

if __name__ == "__main__":
    server.run(transport="sse")
