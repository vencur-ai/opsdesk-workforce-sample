# MCP

`opsdesk_mcp_bridge.py` serves every workspace tool over MCP (stdio). It needs Python 3.9 or newer and nothing else –
no package of this set and no Docker access – and talks to the app container over HTTP (plain HTTP, step 1):

```
python3 opsdesk_mcp_bridge.py --server http://127.0.0.1:8080
```

Calls go to the same `/api/step` as the GUI, so GUI and MCP agents change the same state. Each tool's `inputSchema` is
`{"args": <the tool's schema>}`; arguments outside `args` are refused, and a call the app refuses comes back with
`isError: true`. Image of the app: `opsdesk-workforce:3.12.4-sample-312en`.
