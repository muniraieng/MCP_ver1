import asyncio
from mcp.client.sse import sse_client
from client_workflow import run_weather_client

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

To run the server:
uv run server.py
"""


async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        await run_weather_client(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
