import asyncio
import sys
from pathlib import Path
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from client_workflow import run_weather_client

async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("server.py"))],
    )

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        await run_weather_client(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
