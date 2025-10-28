#!/usr/bin/env python3
"""
Claude-Agents Framework Quick-Start Script
Convenient wrapper for common framework operations
"""

import argparse
import sys
from pathlib import Path

# Add core directory to path
FRAMEWORK_DIR = Path(__file__).parent
sys.path.insert(0, str(FRAMEWORK_DIR / "core"))

# Import CLI
from cli import ClaudeAgentsCLI


def quick_start_project(project_path: str):
    """
    Quick-start an existing project by loading and using agents.

    This demonstrates how to use the framework programmatically.
    """
    from agent_manager import AgentManager
    from prompt_engine import PromptEngine

    project_path = Path(project_path)
    agents_dir = project_path / "agents"

    if not agents_dir.exists():
        print(f"❌ Error: No agents directory found at {agents_dir}")
        print(f"\nTo initialize a project first, run:")
        print(f"  claude-agents init --name my-project --type sql_database_analysis")
        return 1

    print(f"\n{'='*60}")
    print("🚀 CLAUDE-AGENTS QUICK-START")
    print(f"{'='*60}")
    print(f"\nProject: {project_path}")

    # Initialize managers
    manager = AgentManager(agents_dir=str(agents_dir))
    engine = PromptEngine()

    # List available agents
    agents = manager.list_agents()

    if not agents:
        print(f"\n❌ No agents found in {agents_dir}")
        return 1

    print(f"\nFound {len(agents)} agent(s):")
    for agent_name in agents:
        agent = manager.load_agent(agent_name)
        if agent:
            print(f"  ✓ {agent_name}")
            print(f"    Role: {agent.context.get('role', 'N/A')}")
            print(f"    Tools: {len(agent.tools.get('skills', []))} skills, "
                  f"{len(agent.tools.get('slash_commands', []))} commands")

    print(f"\n{'='*60}")
    print("USAGE EXAMPLES")
    print(f"{'='*60}\n")

    # Show example usage with first agent
    first_agent_name = agents[0]
    first_agent = manager.load_agent(first_agent_name)

    print(f"1. Generate a prompt for '{first_agent_name}':")
    print(f"""
from core.agent_manager import AgentManager
from core.prompt_engine import PromptEngine

manager = AgentManager(agents_dir="{agents_dir}")
engine = PromptEngine()

agent = manager.load_agent("{first_agent_name}")
prompt = engine.generate_prompt(
    context=agent.context,
    model=agent.model,
    tools=agent.tools,
    task="Analyze Q4 sales data and identify trends"
)

# Use prompt with Claude API
""")

    print(f"\n2. Use slash commands:")
    slash_commands = first_agent.tools.get('slash_commands', [])
    if slash_commands:
        print(f"   Available commands: {', '.join(slash_commands)}")
    else:
        print(f"   No slash commands configured")

    print(f"\n3. Connect MCP servers:")
    mcp_servers = first_agent.tools.get('mcp_servers', [])
    if mcp_servers:
        print(f"   Configured servers: {', '.join(mcp_servers)}")
        print(f"   Run: claude-agents mcp-setup (coming soon)")
    else:
        print(f"   No MCP servers configured")

    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}\n")

    print("1. Review agent configurations:")
    print(f"   cd {agents_dir}")
    print(f"   cat {first_agent_name}/config.yaml")
    print(f"   cat {first_agent_name}/prompt.md")

    print(f"\n2. Create additional agents:")
    print(f"   claude-agents create --name custom-agent --template data_scientist")

    print(f"\n3. Integrate into your application:")
    print(f"   See FRAMEWORK_AS_PACKAGE_GUIDE.md for examples")

    print()
    return 0


def interactive_setup():
    """
    Interactive project setup wizard.
    """
    print(f"\n{'='*60}")
    print("🤖 CLAUDE-AGENTS INTERACTIVE SETUP")
    print(f"{'='*60}\n")

    # Get project name
    project_name = input("Project name: ").strip()
    if not project_name:
        print("❌ Project name required")
        return 1

    # Show project types
    print("\nAvailable project types:")
    project_types = {
        '1': ('sql_database_analysis', 'SQL Database Analysis (data scientist + business analyst)'),
        '2': ('financial_analysis', 'Financial Analysis (business analyst)'),
        '3': ('data_science', 'Data Science (data scientist)'),
        '4': ('customer_analysis', 'Customer Analysis (data scientist + business strategist)'),
        '5': ('web_analytics', 'Web Analytics (web analyst)'),
        '6': ('full_stack', 'Full Stack (data scientist + business analyst)')
    }

    for key, (ptype, desc) in project_types.items():
        print(f"  {key}. {desc}")

    choice = input("\nSelect project type (1-6): ").strip()

    if choice not in project_types:
        print("❌ Invalid choice")
        return 1

    project_type, _ = project_types[choice]

    # Get output directory
    output_dir = input(f"\nOutput directory (default: ./{project_name}): ").strip()
    if not output_dir:
        output_dir = f"./{project_name}"

    # Run CLI init command
    print(f"\n{'='*60}")
    print("CREATING PROJECT")
    print(f"{'='*60}\n")

    cli = ClaudeAgentsCLI()

    # Create args object
    class Args:
        def __init__(self):
            self.name = project_name
            self.type = project_type
            self.output = output_dir

    args = Args()
    cli.init_project(args)

    return 0


def main():
    """Main entry point for run.py"""

    parser = argparse.ArgumentParser(
        description='Claude-Agents Framework Quick-Start',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup wizard
  python run.py --interactive

  # Quick-start an existing project
  python run.py --project ./my-sales-project

  # Show project info
  python run.py --info ./my-sales-project

For full CLI functionality, use:
  claude-agents --help
        """
    )

    parser.add_argument('--project', '-p', help='Path to project directory (for quick-start)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive setup wizard')
    parser.add_argument('--info', help='Show information about a project')

    args = parser.parse_args()

    if args.interactive:
        return interactive_setup()
    elif args.project:
        return quick_start_project(args.project)
    elif args.info:
        return quick_start_project(args.info)
    else:
        # Show help if no arguments
        parser.print_help()
        print(f"\n{'='*60}")
        print("QUICK START")
        print(f"{'='*60}\n")
        print("To create your first project:")
        print("  python run.py --interactive")
        print("\nOr use the full CLI:")
        print("  claude-agents init --name my-project --type sql_database_analysis")
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
