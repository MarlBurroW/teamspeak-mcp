#!/usr/bin/env python3
"""
Test script for TeamSpeak MCP server.
Used to test functionality without Claude Desktop.
"""

import asyncio
import json
import os
import sys
from teamspeak_mcp.server import TeamSpeakMCPServer, ts_connection

async def test_connection():
    """Test TeamSpeak server connection."""
    print("🔍 Testing TeamSpeak server connection...")
    
    # Check environment variables
    required_vars = ["TEAMSPEAK_HOST", "TEAMSPEAK_USER", "TEAMSPEAK_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Create a .env file based on config.example.env")
        return False
    
    success = await ts_connection.connect()
    if success:
        print("✅ Connection successful!")
        await ts_connection.disconnect()
        return True
    else:
        print("❌ Connection failed")
        return False

async def test_tools():
    """Test MCP tools."""
    server = TeamSpeakMCPServer()
    
    print("\n🔧 Testing MCP tools...")
    
    # Test tools list
    from mcp.types import ListToolsRequest
    
    tools_request = ListToolsRequest(method="tools/list")
    tools_result = await server.handle_list_tools(tools_request)
    
    print(f"📋 {len(tools_result.tools)} tools available:")
    for tool in tools_result.tools:
        print(f"  • {tool.name}: {tool.description}")
    
    return True

async def main():
    """Main test function."""
    print("🚀 TeamSpeak MCP Tests\n")
    
    # Load environment variables from .env or .env.test if present
    env_files = [".env.test", ".env"]
    loaded_env = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"📄 Loading configuration from {env_file}")
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
            loaded_env = True
            break
    
    if not loaded_env:
        print("⚠️  .env file not found, using system environment variables")
    
    # Run tests
    connection_ok = await test_connection()
    tools_ok = await test_tools()
    
    if connection_ok and tools_ok:
        print("\n✅ All tests passed! TeamSpeak MCP is ready to use.")
        print("\n🎯 Next steps:")
        print("1. Add configuration to Claude Desktop (see README.md)")
        print("2. Restart Claude Desktop")
        print("3. Test with commands like 'Connect to TeamSpeak server'")
    else:
        print("\n❌ Some tests failed. Check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 