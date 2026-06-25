"""
mcp_python_client.py -- call Scavio's remote MCP server from Python.

Scavio runs a hosted Model Context Protocol server at https://mcp.scavio.dev/mcp
that exposes all 33 Scavio endpoints as MCP tools (search_google,
search_amazon, get_instagram_profile, search_reddit, ...). Any MCP client can
use them -- Claude Desktop, Cursor, or your own code. This script connects over
streamable HTTP, lists the tools, and calls two of them.

Auth: pass your Scavio API key in the `x-api-key` header.

Prerequisites:
  pip install mcp
  export SCAVIO_API_KEY="sk_..."   # https://dashboard.scavio.dev

Usage:
  python mcp_python_client.py
"""

import asyncio
import json
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_URL = "https://mcp.scavio.dev/mcp"


async def main():
    api_key = os.environ["SCAVIO_API_KEY"]
    headers = {"x-api-key": api_key}

    async with streamablehttp_client(MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            print(f"Scavio MCP exposes {len(names)} tools, e.g.: {', '.join(names[:8])} ...\n")

            # 1) Google search.
            google = await session.call_tool("search_google", {"query": "best ai search api 2026"})
            print("search_google ->")
            print(_first_text(google)[:400], "\n")

            # 2) Instagram profile.
            ig = await session.call_tool("get_instagram_profile", {"username": "nike"})
            print("get_instagram_profile(nike) ->")
            print(_first_text(ig)[:400])


def _first_text(result) -> str:
    """Pull the first text block out of an MCP tool result."""
    for block in result.content:
        text = getattr(block, "text", None)
        if text:
            try:
                return json.dumps(json.loads(text), indent=2)
            except (ValueError, TypeError):
                return text
    return str(result.content)


if __name__ == "__main__":
    asyncio.run(main())
