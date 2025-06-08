#!/usr/bin/env python3

from mcp_server import server
import asyncio

if __name__ == "__main__":
    asyncio.run(server.run())