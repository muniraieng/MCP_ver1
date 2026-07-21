# MCP Weather Server Learning Project

##	Contribute by
A learning project for building an MCP server by munir.ai.eng@gmail.com

A hands-on introduction to the **Model Context Protocol (MCP)**. This repository contains a weather MCP server, example clients, and a Docker-based SSE deployment.

It was built while learning how an MCP host, client, server, tools, resources, and prompts work together.

## What is MCP?

MCP is a standard way for AI applications to discover and use external capabilities. Instead of building a separate integration for every AI app, an MCP server exposes a consistent interface that compatible hosts can connect to.

```text
MCP Host (Cursor / Claude Desktop / custom app)
        |
        v
MCP Client
        |
        v
MCP Server
        |
        v
Weather.gov API
```

- **Host**: the AI application, such as Cursor or Claude Desktop.
- **Client**: the connection layer that manages the MCP session and invokes server capabilities.
- **Server**: the program that provides tools, resources, and prompts.
- **Tools**: actions the AI can call. This project provides weather alerts and forecasts.
- **Resources**: data exposed through a URI, such as configuration or an echo example.
- **Prompts**: reusable prompt templates, such as the included code-review prompt.

## Repository layout

```text
mcp_v1/
|-- server/
|   |-- weather.py          # Local FastMCP weather server (stdio)
|   `-- example.py          # Small example server
|-- client/
|   |-- weather.json        # MCP client configuration
|   `-- weather.py          # Interactive MCP + LLM client
`-- mcp_docker/
    |-- server.py           # SSE weather server
    |-- client-sse.py       # Connects to the SSE server
    |-- client-stdio.py     # Connects over stdio
    `-- Dockerfile          # Container image definition
```

## Features

- `get_alerts(state)` retrieves active weather alerts for a two-letter US state code.
- `get_forecast(latitude, longitude)` retrieves a short forecast for a US location (Docker/SSE server).
- Uses `httpx.AsyncClient` to call the [National Weather Service API](https://www.weather.gov/documentation/services-web-api).
- Demonstrates both **stdio** and **SSE** transports.
- Includes example MCP resources and a reusable prompt.

## Prerequisites

- Python 3.11+ (the local project currently declares Python 3.14+)
- [uv](https://docs.astral.sh/uv/)
- Docker Desktop (only for the Docker example)
- Optional: Cursor or Claude Desktop to use the server from an AI host
- Optional: a Groq API key for `client/weather.py`

## Run the local MCP server

From the project directory:

```powershell
cd mcp_v1
uv sync
uv run mcp run server/weather.py
```

The server uses **stdio** transport, which is intended to be launched and managed by an MCP host rather than opened in a browser.

## Connect it to an MCP host

The example configuration is in [`mcp_v1/client/weather.json`](mcp_v1/client/weather.json). Update the two Windows paths so they match your clone and virtual environment:

```json
{
  "mcpServers": {
    "weather": {
      "command": "C:\\path\\to\\mcp_v1\\.venv\\Scripts\\mcp.exe",
      "args": [
        "run",
        "C:\\path\\to\\mcp_v1\\server\\weather.py"
      ]
    }
  }
}
```

Add the equivalent server entry in your host application's MCP configuration, then restart the host. The host can discover the `get_alerts` tool and call it with values such as `CA` or `NY`.

## Run the Docker / SSE example

```powershell
cd mcp_v1/mcp_docker
docker build -t mcp-weather-server .
docker run --rm -p 8000:8000 mcp-weather-server
```

In a second terminal, install the dependencies for the client and run:

```powershell
cd mcp_v1/mcp_docker
uv run client-sse.py
```

The client connects to `http://localhost:8000/sse`, lists available tools, then requests alerts for California.

To test the same server program through stdio without Docker:

```powershell
cd mcp_v1/mcp_docker
uv run client-stdio.py
```

## Optional LLM client

`mcp_v1/client/weather.py` is an interactive chat client using `mcp-use` and Groq. Create a `.env` file inside `mcp_v1/client`:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Then run:

```powershell
cd mcp_v1
uv run client/weather.py
```

## Notes

- The weather API covers US National Weather Service data, so use US state codes and coordinates.
- API requests include a user-agent header and basic error handling.
- Never commit `.env` files or API keys.

## Learning outcomes

This project demonstrates:

- MCP host, client, and server responsibilities
- Tool, resource, and prompt registration with FastMCP
- Calling an external HTTP API asynchronously with `httpx`
- Using stdio for local host integrations
- Running an MCP server over SSE in Docker
- Connecting an AI/LLM client to MCP tools

## License

This is a personal learning project. Add a license file before distributing or reusing it publicly.

