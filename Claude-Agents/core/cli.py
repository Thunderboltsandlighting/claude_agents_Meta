#!/usr/bin/env python3
"""
Claude-Agents Framework CLI
Main entry point for the framework
"""

import argparse
import sys
from pathlib import Path
import importlib.util

# Load modules dynamically (handles hyphenated filenames)
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get framework directory
FRAMEWORK_DIR = Path(__file__).parent.parent

# Load core modules
agent_factory_mod = load_module("agent_factory", FRAMEWORK_DIR / "core" / "agent-factory.py")
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentFactory = agent_factory_mod.AgentFactory
AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine


class ClaudeAgentsCLI:
    """CLI interface for Claude-Agents framework"""

    def __init__(self):
        self.framework_dir = FRAMEWORK_DIR
        self.factory = AgentFactory(framework_dir=str(self.framework_dir))

    def init_project(self, args):
        """Initialize a new project with agents"""
        print(f"\n{'='*60}")
        print("🚀 CLAUDE-AGENTS FRAMEWORK")
        print(f"{'='*60}")
        print(f"\nInitializing project: {args.name}")
        print(f"Project type: {args.type}")
        print(f"Output directory: {args.output}")

        # Create project directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Auto-create agents based on project type
        print(f"\nCreating agents...")
        agents = self.factory.auto_create_agents_for_project(
            project_type=args.type,
            project_name=args.name,
            output_dir=output_dir / "agents"
        )

        print(f"\n{'='*60}")
        print("✅ PROJECT INITIALIZED")
        print(f"{'='*60}")

        print(f"\nCreated {len(agents)} agent(s):")
        for agent_path in agents:
            print(f"  ✓ {agent_path.name}")

        print(f"\nProject structure:")
        print(f"  {output_dir}/")
        print(f"  └── agents/")
        for agent_path in agents:
            print(f"      ├── {agent_path.name}/")
            print(f"      │   ├── config.yaml")
            print(f"      │   └── prompt.md")

        print(f"\n{'='*60}")
        print("NEXT STEPS:")
        print(f"{'='*60}")
        print(f"\n1. Review your agents:")
        print(f"   cd {output_dir}/agents")
        print(f"   ls -la")

        print(f"\n2. Use agents in your code:")
        print(f"""
   from core.agent_manager import AgentManager
   from core.prompt_engine import PromptEngine

   manager = AgentManager(agents_dir="{output_dir}/agents")
   engine = PromptEngine()

   agent = manager.load_agent("{agents[0].name}")
   prompt = engine.generate_prompt(
       context=agent.context,
       model=agent.model,
       tools=agent.tools,
       task="Your analysis task"
   )
""")

        print(f"\n3. Or use the quick-start script:")
        print(f"   python run.py --project {output_dir}")

        return agents

    def create_agent(self, args):
        """Create a custom agent"""
        print(f"\n{'='*60}")
        print("🤖 CREATING CUSTOM AGENT")
        print(f"{'='*60}")
        print(f"\nAgent name: {args.name}")
        print(f"Template: {args.template}")

        output_dir = Path(args.output) if args.output else Path("agents")

        if args.template:
            # Use template
            agent_path = self.factory.create_agent_from_template(
                agent_name=args.name,
                template_name=args.template,
                output_dir=output_dir
            )
        else:
            print("\n❌ Error: --template is required for custom agents")
            print("Available templates:")
            for template in self.factory.list_available_templates():
                print(f"  - {template}")
            return

        print(f"\n✅ Agent created at: {agent_path}")
        print(f"\nFiles created:")
        print(f"  - {agent_path}/config.yaml")
        print(f"  - {agent_path}/prompt.md")

        return agent_path

    def list_templates(self, args):
        """List available agent templates"""
        print(f"\n{'='*60}")
        print("📋 AVAILABLE AGENT TEMPLATES")
        print(f"{'='*60}\n")

        templates = self.factory.list_available_templates()

        template_descriptions = {
            'base_agent': 'Generic foundation for custom agents (all variables)',
            'business_analyst': 'Financial analysis, KPIs, forecasting, budgeting',
            'data_scientist': 'Statistical analysis, ML, data visualization',
            'therapist_assistant': 'Educational support (psychology, NOT clinical)'
        }

        for template in templates:
            desc = template_descriptions.get(template, 'Specialized agent template')
            print(f"  {template}")
            print(f"    └─ {desc}\n")

        print(f"{'='*60}")
        print(f"Total: {len(templates)} templates available")
        print(f"{'='*60}\n")

        print("Usage:")
        print(f"  claude-agents init --name my-project --type sql_database_analysis")
        print(f"  claude-agents create --name my-agent --template business_analyst\n")

    def list_project_types(self, args):
        """List available project types"""
        print(f"\n{'='*60}")
        print("📦 AVAILABLE PROJECT TYPES")
        print(f"{'='*60}\n")

        project_types = {
            'sql_database_analysis': [
                'SQL Database Analyst (data scientist, customized)',
                'Business Reporter (business analyst)'
            ],
            'financial_analysis': [
                'Finance Analyst (business analyst)'
            ],
            'data_science': [
                'Data Analyst (data scientist)'
            ],
            'customer_analysis': [
                'Customer Analyst (data scientist, customized)',
                'Business Strategist (business analyst)'
            ],
            'web_analytics': [
                'Web Analyst (data scientist, customized)'
            ],
            'content_creation': [
                'Content Strategist (planning and strategy)',
                'Content Writer (writing and creation)',
                'Content Editor (editing and QA)',
                'SEO Specialist (optimization and analysis)'
            ],
            'therapy_practice_management': [
                'Business Analyst (practice financials and KPIs)',
                'Content Strategist (HIPAA-compliant marketing)',
                'Content Creator (mental health content)',
                'Social Media Manager (community engagement)',
                'Marketing Analytics (ROI and performance)',
                'Market Research (local demand analysis)',
                'Practice Operations (scheduling and efficiency)'
            ],
            'full_stack': [
                'Data Scientist',
                'Business Analyst'
            ]
        }

        for ptype, agents in project_types.items():
            print(f"  {ptype}")
            print(f"    Creates:")
            for agent in agents:
                print(f"      • {agent}")
            print()

        print(f"{'='*60}")
        print(f"Total: {len(project_types)} project types")
        print(f"{'='*60}\n")

        print("Usage:")
        print(f"  claude-agents init --name my-project --type sql_database_analysis\n")

    def test_framework(self, args):
        """Run framework tests"""
        print(f"\n{'='*60}")
        print("🧪 TESTING FRAMEWORK")
        print(f"{'='*60}\n")

        test_script = self.framework_dir / "test_framework.py"

        if not test_script.exists():
            print(f"❌ Test script not found: {test_script}")
            return

        print(f"Running: python {test_script}\n")

        import subprocess
        result = subprocess.run(
            [sys.executable, str(test_script)],
            cwd=str(self.framework_dir),
            capture_output=False
        )

        if result.returncode == 0:
            print(f"\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with code {result.returncode}")

        return result.returncode


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description='Claude-Agents Framework - Create and manage AI agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize a new SQL analysis project
  claude-agents init --name sales-db --type sql_database_analysis

  # Create a custom business analyst agent
  claude-agents create --name finance-analyst --template business_analyst

  # List available templates
  claude-agents list-templates

  # List available project types
  claude-agents list-types

  # Run framework tests
  claude-agents test

For more information, see: README.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new project with agents')
    init_parser.add_argument('--name', '-n', required=True, help='Project name')
    init_parser.add_argument('--type', '-t', required=True, help='Project type (sql_database_analysis, financial_analysis, etc.)')
    init_parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a custom agent')
    create_parser.add_argument('--name', '-n', required=True, help='Agent name')
    create_parser.add_argument('--template', '-t', help='Template to use (base_agent, business_analyst, data_scientist)')
    create_parser.add_argument('--output', '-o', help='Output directory (default: ./agents)')

    # List templates command
    subparsers.add_parser('list-templates', help='List available agent templates')

    # List project types command
    subparsers.add_parser('list-types', help='List available project types')

    # Test command
    subparsers.add_parser('test', help='Run framework tests')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Initialize CLI
    cli = ClaudeAgentsCLI()

    # Execute command
    if args.command == 'init':
        cli.init_project(args)
    elif args.command == 'create':
        cli.create_agent(args)
    elif args.command == 'list-templates':
        cli.list_templates(args)
    elif args.command == 'list-types':
        cli.list_project_types(args)
    elif args.command == 'test':
        return cli.test_framework(args)
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())
