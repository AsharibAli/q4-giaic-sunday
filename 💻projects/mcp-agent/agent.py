"""
agent.py  —  OpenAI Agent + FastMCP Server
============================================
This file has 3 main parts:

  1. FastMCP Server  (server.py) — contains our tools
  2. MCP Client      — connects to the server
  3. OpenAI Agent    — thinks and uses the tools

Flow:
  User → Agent → MCP Client → FastMCP Server → Tool → Answer

Setup:
  uv init mcp-agent
  cd mcp-agent
  uv add fastmcp openai-agents python-dotenv

  # Add your API key in .env file:
  # OPENAI_API_KEY=sk-xxxx
  # GITHUB_TOKEN=ghp-xxxx

  # Run:
  uv run agent.py
"""

import asyncio
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file


# ═══════════════════════════════════════════════════════════════
# API KEY CHECK
# ═══════════════════════════════════════════════════════════════

async def main():

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY is not set!")
        print("   Add this line in your .env file:")
        print('   OPENAI_API_KEY=sk-xxxxxxxxxxxx')
        return

    print("🚀 Starting MCP Agent...\n")

    # ═══════════════════════════════════════════════════════════
    # STEP 1: Connect to MCP Server
    # ═══════════════════════════════════════════════════════════
    #
    # MCPServerStdio = runs the server as a subprocess
    # "command": "npx"         → use npx to start the server
    # "args": ["run", "..."]   → which server to run
    #
    # "async with" automatically:
    #   ✅ starts the server
    #   ✅ connects to it
    #   ✅ shuts it down when done
    # ═══════════════════════════════════════════════════════════
    #Stdio = same computer, communicates through pipes. HTTP = over the network, via URL. WebSocket = permanent open connection, real-time.
    
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-github"
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")
            }
        }
    ) as mcp_server:
    

        print("✅ Connected to MCP Server!\n")

        # ═══════════════════════════════════════════════════════
        # STEP 2: Create the Agent
        # ═══════════════════════════════════════════════════════
        #
        # Agent has 3 main parts:
        #
        # name         → any name for your agent
        # instructions → tell the agent who it is and what to do
        # mcp_servers  → which MCP servers it can use
        #
        # The agent automatically gets the list of tools from
        # the MCP server, then decides which tool to use
        # based on the user's question.
        # ═══════════════════════════════════════════════════════

        agent = Agent(
            name="Personal AI Assistant",
            model="gpt-5.3-codex",

            instructions="""
            You are a personal AI assistant.
            You have access to GitHub tools via MCP server.
            Use the available tools whenever needed to complete tasks.
            """,
            mcp_servers=[mcp_server],
        )

        print("✅ Agent is ready!\n")
        print("=" * 50)

        # ═══════════════════════════════════════════════════════
        # STEP 3: Give the Agent a task
        # ═══════════════════════════════════════════════════════
        #
        # Runner.run(agent, input="...") does this internally:
        #   1. Sends the input to OpenAI
        #   2. OpenAI decides which tool to use
        #   3. Tool is called on the MCP Server
        #   4. Result is sent back to OpenAI
        #   5. OpenAI generates the final answer
        #   6. Final answer is in result.final_output
        # ═══════════════════════════════════════════════════════
        task = input("Enter your input prompt: ")
        result = await Runner.run(
            agent,
            input=task
        )
        print(f"🤖 Agent: {result.final_output}")


# ── Run the program ────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())


#JSON RPC = Remote Procedure Call (RPC) protocol encoded in JSON. Client sends a request to call a method with parameters, and the server responds with the result. In this case, the client is asking the MCP server to call the "get_weather" tool with the argument "city" set to "Karachi".

#Client to server request example:
# {
#   "jsonrpc": "2.0",
#   "id": 1,
#   "method": "tools/call",
#   "params": {
#     "name": "get_weather",
#     "arguments": {
#       "city": "Karachi"
#     }
#   }
# }

#Server to client response example:
# {
#   "jsonrpc": "2.0",
#   "id": 1,
#   "result": {
#     "content": "Karachi: 35C, Sunny"
#   }
# }

#Error response example:
# {
#   "jsonrpc": "2.0",
#   "id": 1,
#   "error": {
#     "code": -32600,
#     "message": "City not found"
#   }
# }


#async with MCPServerStdio(
#     params={"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"],
#             "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")}}
# ) as github_server, MCPServerStdio(
#     params={"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Tushiba\\Desktop"]}
# ) as filesystem_server:

#     agent = Agent(
#         name="Super Assistant",
#         instructions="you can access github and filesystem.",
#         mcp_servers=[github_server, filesystem_server],  # ← dono dے do
#     )
# ```