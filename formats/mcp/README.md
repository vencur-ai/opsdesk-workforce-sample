# MCP

`python -m opsdesk.workforce.mcp --server http://127.0.0.1:8080` serves every workspace tool over MCP (stdio).
Calls go to the same `/api/step` as the GUI, so GUI and MCP agents change the same state. Image: `opsdesk-workforce-sample:3.2.0`.
