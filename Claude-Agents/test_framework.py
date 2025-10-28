#!/usr/bin/env python3
"""
Test Suite for Claude-Agents Framework
Validates all core components and agent configurations
"""

import sys
from pathlib import Path

# Add core directory to path
core_dir = Path(__file__).parent / "core"
sys.path.insert(0, str(core_dir))

# Import with explicit path handling
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

agent_manager = load_module("agent_manager", core_dir / "agent-manager.py")
prompt_engine = load_module("prompt_engine", core_dir / "prompt-engine.py")
mcp_connector = load_module("mcp_connector", core_dir / "mcp-connector.py")

AgentManager = agent_manager.AgentManager
PromptEngine = prompt_engine.PromptEngine
MCPConnector = mcp_connector.MCPConnector


def test_agent_manager():
    """Test agent manager functionality"""
    print("\n" + "="*80)
    print("TEST 1: Agent Manager")
    print("="*80)

    manager = AgentManager(agents_dir="agents")

    # Test listing agents
    agents = manager.list_agents()
    print(f"✓ Found {len(agents)} agent(s): {agents}")
    assert len(agents) > 0, "No agents found"

    # Test loading agent
    print("\nLoading business-analyst agent...")
    agent = manager.load_agent("business-analyst")
    print(f"✓ Loaded agent: {agent}")

    # Validate configuration
    is_valid, errors = manager.validate_agent_config(agent.config)
    if is_valid:
        print("✓ Agent configuration is valid")
    else:
        print(f"✗ Validation errors: {errors}")
        return False

    # Test agent properties
    print(f"\nAgent Properties:")
    print(f"  Role: {agent.context['role']}")
    print(f"  Skills: {agent.get_skills()}")
    print(f"  Slash Commands: {agent.get_slash_commands()}")
    print(f"  MCP Servers: {agent.get_mcp_servers()}")

    # Test prompt generation
    print("\nGenerating system prompt...")
    prompt = agent.generate_system_prompt()
    assert len(prompt) > 0, "Empty prompt generated"
    print(f"✓ Generated prompt ({len(prompt)} characters)")

    return True


def test_prompt_engine():
    """Test prompt engine functionality"""
    print("\n" + "="*80)
    print("TEST 2: Prompt Engine")
    print("="*80)

    engine = PromptEngine(prompts_dir="prompts")

    # Test Four Core Keys prompt generation
    print("\nGenerating Four Core Keys prompt...")
    context = {
        "role": "Test Agent",
        "expertise": ["Testing", "Validation"],
        "scope": "Test framework components",
        "constraints": ["Must complete in 5 minutes"]
    }

    model = {
        "name": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "temperature": 0.3,
        "response_format": "structured"
    }

    tools = {
        "skills": ["test-skill"],
        "slash_commands": ["/test"],
        "mcp_servers": ["test-server"]
    }

    prompt = engine.generate_prompt(
        context=context,
        model=model,
        tools=tools,
        task="Test the framework"
    )

    print(f"✓ Generated prompt ({len(prompt)} characters)")

    # Validate prompt structure
    print("\nValidating prompt structure...")
    is_valid, warnings = engine.validate_prompt_structure(prompt)

    if is_valid:
        print("✓ Prompt structure is valid")
    else:
        print(f"⚠ Validation warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    # Check for Four Core Keys
    assert "KEY 1: CONTEXT" in prompt, "Missing KEY 1: CONTEXT"
    assert "KEY 2: MODEL" in prompt, "Missing KEY 2: MODEL"
    assert "KEY 3: PROMPT" in prompt, "Missing KEY 3: PROMPT"
    assert "KEY 4: TOOLS" in prompt, "Missing KEY 4: TOOLS"
    print("✓ All Four Core Keys present")

    return True


def test_mcp_connector():
    """Test MCP connector functionality"""
    print("\n" + "="*80)
    print("TEST 3: MCP Connector")
    print("="*80)

    connector = MCPConnector(mcp_dir="mcp-servers")

    # Load server configurations
    print("\nLoading MCP server configurations...")
    try:
        servers = connector.load_server_config("business-finance-servers.json")
        print(f"✓ Loaded {len(servers)} MCP server(s)")

        for name, server in servers.items():
            print(f"  - {name}: {server.description}")

    except FileNotFoundError as e:
        print(f"⚠ MCP config file not found: {e}")
        print("  Creating test servers...")

        # Create test servers
        connector.create_server_config(
            name="test-server",
            command="npx",
            args=["-y", "test-package"],
            description="Test MCP server",
            category="test"
        )
        print("✓ Created test server")

    # Test server retrieval
    print("\nTesting server operations...")
    servers = connector.list_servers()
    print(f"✓ Total servers available: {len(servers)}")

    categories = connector.list_categories()
    print(f"✓ Server categories: {categories}")

    # Test domain recommendations
    print("\nTesting domain recommendations...")
    domains = ['business_finance', 'data_science', 'development']

    for domain in domains:
        recommended = connector.get_recommended_servers_for_domain(domain)
        print(f"  {domain}: {len(recommended)} server(s) - {recommended[:3]}")

    # Test Claude config generation
    print("\nGenerating Claude desktop configuration...")
    finance_servers = connector.get_recommended_servers_for_domain('business_finance')

    if finance_servers:
        config = connector.generate_claude_config(
            finance_servers,
            output_file="test_claude_config.json"
        )
        print(f"✓ Generated config with {len(config['mcpServers'])} servers")
        print(f"  Saved to: test_claude_config.json")

    return True


def test_integration():
    """Test integrated workflow"""
    print("\n" + "="*80)
    print("TEST 4: Integration Test")
    print("="*80)

    print("\nTesting complete agent workflow...")

    # 1. Load agent
    manager = AgentManager(agents_dir="agents")
    agent = manager.load_agent("business-analyst")
    print(f"✓ Step 1: Loaded agent '{agent.name}'")

    # 2. Generate prompt using agent config
    engine = PromptEngine()
    prompt = engine.generate_prompt(
        context=agent.context,
        model=agent.model,
        tools=agent.tools,
        task="Analyze Q1 budget variance"
    )
    print(f"✓ Step 2: Generated task-specific prompt")

    # 3. Validate prompt
    is_valid, warnings = engine.validate_prompt_structure(prompt)
    assert is_valid or len(warnings) == 0, f"Prompt validation issues: {warnings}"
    print(f"✓ Step 3: Validated prompt structure")

    # 4. Get MCP servers
    connector = MCPConnector(mcp_dir="mcp-servers")
    try:
        connector.load_server_config("business-finance-servers.json")
        mcp_servers = agent.get_mcp_servers()
        print(f"✓ Step 4: Loaded {len(mcp_servers)} MCP servers for agent")
    except FileNotFoundError:
        print("⚠ Step 4: MCP config not found (optional)")

    # 5. Display agent readiness
    print(f"\n✓ Agent is ready for deployment!")
    print(f"\nAgent Summary:")
    print(f"  Name: {agent.name}")
    print(f"  Role: {agent.context['role']}")
    print(f"  Model: {agent.model['name']}")
    print(f"  Skills: {len(agent.get_skills())}")
    print(f"  Commands: {len(agent.get_slash_commands())}")
    print(f"  Prompt Length: {len(prompt)} chars")

    return True


def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*80)
    print("CLAUDE-AGENTS FRAMEWORK TEST SUITE")
    print("="*80)

    tests = [
        ("Agent Manager", test_agent_manager),
        ("Prompt Engine", test_prompt_engine),
        ("MCP Connector", test_mcp_connector),
        ("Integration", test_integration)
    ]

    results = {}
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
        except Exception as e:
            print(f"\n✗ Test '{name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Framework is ready to use.")
        return 0
    else:
        print("\n⚠ Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
