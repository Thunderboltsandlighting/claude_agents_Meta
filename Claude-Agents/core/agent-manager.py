"""
Agent Manager Module
Handles agent lifecycle, configuration loading, and orchestration
Part of Claude-Agents Framework
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class AgentManager:
    """
    Manages Claude agents including loading configurations,
    initializing agents, and coordinating agent interactions.
    """

    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self.loaded_agents: Dict[str, 'Agent'] = {}
        self.agent_configs: Dict[str, Dict] = {}

    def load_agent(self, agent_name: str) -> Optional['Agent']:
        """
        Load an agent from its configuration directory.

        Args:
            agent_name: Name of the agent to load

        Returns:
            Agent instance or None if not found
        """
        agent_path = self.agents_dir / agent_name
        config_file = agent_path / "config.yaml"

        if not config_file.exists():
            raise FileNotFoundError(f"Agent config not found: {config_file}")

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        self.agent_configs[agent_name] = config
        agent = Agent(agent_name, config, agent_path)
        self.loaded_agents[agent_name] = agent

        return agent

    def list_agents(self) -> List[str]:
        """List all available agents in the agents directory."""
        if not self.agents_dir.exists():
            return []

        agents = []
        for item in self.agents_dir.iterdir():
            if item.is_dir() and (item / "config.yaml").exists():
                agents.append(item.name)

        return agents

    def get_agent(self, agent_name: str) -> Optional['Agent']:
        """
        Get a loaded agent or load it if not already loaded.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent instance or None
        """
        if agent_name in self.loaded_agents:
            return self.loaded_agents[agent_name]

        return self.load_agent(agent_name)

    def reload_agent(self, agent_name: str) -> Optional['Agent']:
        """
        Reload an agent's configuration.

        Args:
            agent_name: Name of the agent to reload

        Returns:
            Reloaded Agent instance
        """
        if agent_name in self.loaded_agents:
            del self.loaded_agents[agent_name]

        return self.load_agent(agent_name)

    def validate_agent_config(self, config: Dict) -> tuple[bool, List[str]]:
        """
        Validate agent configuration against framework requirements.

        Args:
            config: Agent configuration dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        required_fields = ['agent_name', 'context', 'model', 'tools']

        # Check required top-level fields
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        # Validate context structure
        if 'context' in config:
            context_fields = ['role', 'expertise', 'scope', 'constraints']
            for field in context_fields:
                if field not in config['context']:
                    errors.append(f"Missing context field: {field}")

        # Validate model structure
        if 'model' in config:
            model_fields = ['name', 'max_tokens', 'temperature']
            for field in model_fields:
                if field not in config['model']:
                    errors.append(f"Missing model field: {field}")

        # Validate tools structure
        if 'tools' in config:
            tools_fields = ['skills', 'slash_commands', 'mcp_servers']
            for field in tools_fields:
                if field not in config['tools']:
                    errors.append(f"Missing tools field: {field}")

        return (len(errors) == 0, errors)


class Agent:
    """
    Represents a Claude agent instance with its configuration,
    prompt template, and tools.
    """

    def __init__(self, name: str, config: Dict, agent_path: Path):
        self.name = name
        self.config = config
        self.agent_path = agent_path

        # Extract configuration components
        self.context = config.get('context', {})
        self.model = config.get('model', {})
        self.tools = config.get('tools', {})
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> Optional[str]:
        """Load the agent's prompt template if it exists."""
        prompt_file = self.agent_path / "prompt.md"
        if prompt_file.exists():
            with open(prompt_file, 'r') as f:
                return f.read()
        return None

    def get_context(self) -> Dict:
        """Get agent context configuration."""
        return self.context

    def get_model_config(self) -> Dict:
        """Get agent model configuration."""
        return self.model

    def get_tools(self) -> Dict:
        """Get agent tools configuration."""
        return self.tools

    def get_skills(self) -> List[str]:
        """Get list of agent skills."""
        return self.tools.get('skills', [])

    def get_slash_commands(self) -> List[str]:
        """Get list of agent slash commands."""
        return self.tools.get('slash_commands', [])

    def get_mcp_servers(self) -> List[str]:
        """Get list of agent MCP servers."""
        return self.tools.get('mcp_servers', [])

    def generate_system_prompt(self) -> str:
        """
        Generate the complete system prompt for the agent
        using the Four Core Keys structure.
        """
        if self.prompt_template:
            return self.prompt_template

        # Fallback: generate basic prompt from config
        return self._generate_basic_prompt()

    def _generate_basic_prompt(self) -> str:
        """Generate a basic prompt from configuration."""
        prompt = f"""# {self.name.replace('-', ' ').title()}

## CONTEXT
Role: {self.context.get('role', '')}
Expertise: {', '.join(self.context.get('expertise', []))}
Scope: {self.context.get('scope', '')}

## MODEL
{yaml.dump(self.model, default_flow_style=False)}

## TOOLS
Skills: {', '.join(self.get_skills())}
Slash Commands: {', '.join(self.get_slash_commands())}
MCP Servers: {', '.join(self.get_mcp_servers())}

## CONSTRAINTS
{chr(10).join('- ' + c for c in self.context.get('constraints', []))}
"""
        return prompt

    def __repr__(self) -> str:
        return f"Agent(name='{self.name}', role='{self.context.get('role', 'unknown')}')"


# Example usage
if __name__ == "__main__":
    manager = AgentManager()

    # List all available agents
    print("Available agents:", manager.list_agents())

    # Load an agent
    try:
        agent = manager.load_agent("business-analyst")
        print(f"Loaded: {agent}")
        print(f"Skills: {agent.get_skills()}")
        print(f"Slash Commands: {agent.get_slash_commands()}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
