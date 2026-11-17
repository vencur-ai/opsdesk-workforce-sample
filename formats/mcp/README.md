# MCP

`python -m opsdesk.workforce.mcp --server http://127.0.0.1:8080` serves every workspace tool over MCP (stdio).
Calls go to the same `/api/step` as the GUI, so GUI and MCP agents change the same state. Image: `opsdesk-workforce:3.9.3-reviewer-sample`.

Without Python on the host, run it inside the running app container (plain HTTP, step 1): `docker exec -i opsdesk python -m opsdesk.workforce.mcp --server http://127.0.0.1:8080`.
