# MCP recipes

Scavio runs a hosted [Model Context Protocol](https://modelcontextprotocol.io)
server at `https://mcp.scavio.dev/mcp` that exposes all 33 Scavio endpoints as
MCP tools (`search_google`, `search_amazon`, `get_instagram_profile`,
`search_reddit`, ...). Any MCP client can call them.

## Use it from an MCP client (Claude Desktop, Cursor, ...)

Copy `mcp-config.example.json` into your client's MCP config (e.g.
`.mcp.json` or Claude Desktop's config) and set your API key:

```json
{
  "mcpServers": {
    "scavio": {
      "type": "http",
      "url": "https://mcp.scavio.dev/mcp",
      "headers": { "x-api-key": "sk_your_scavio_api_key" }
    }
  }
}
```

Your agent can now search Google, Amazon, YouTube, Walmart, Reddit, TikTok, and
Instagram in real time -- no extra code.

## Use it from Python

```bash
pip install -r requirements.txt
export SCAVIO_API_KEY="sk_..."   # free key: https://dashboard.scavio.dev
python mcp_python_client.py
```

`mcp_python_client.py` connects over streamable HTTP, lists the tools, and calls
`search_google` and `get_instagram_profile`. Auth is the `x-api-key` header.

## Files

- **`mcp_python_client.py`** -- connect, list tools, call two of them. Talks to
  the [Scavio MCP server](https://scavio.dev) -- [get a free key](https://dashboard.scavio.dev).
- **`mcp-config.example.json`** -- drop-in MCP config for Claude Desktop / Cursor.
  Point it at the [Scavio search API](https://scavio.dev) -- [start free](https://dashboard.scavio.dev).

---

Give any MCP client real-time search with **[Scavio](https://scavio.dev)** -- [MCP docs](https://scavio.dev/docs).
