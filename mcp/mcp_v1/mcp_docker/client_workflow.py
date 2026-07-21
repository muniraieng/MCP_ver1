"""Shared MCP client workflow, independent of the transport used."""

from mcp import ClientSession


async def run_weather_client(read_stream, write_stream, state: str = "CA") -> None:
    """Initialize an MCP session, show its tools, and request weather alerts."""
    async with ClientSession(read_stream, write_stream) as session:
        await session.initialize()

        tools_result = await session.list_tools()
        print("Available tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")

        result = await session.call_tool("get_alerts", arguments={"state": state})
        print(f"The weather alerts are = {result.content[0].text}")
