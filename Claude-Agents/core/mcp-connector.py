"""
MCP Connector Module
Handles Model Context Protocol (MCP) server connections and integrations
Part of Claude-Agents Framework
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class MCPServer:
    """Represents an MCP server configuration."""
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    description: Optional[str] = None
    category: Optional[str] = None


class MCPConnector:
    """
    Manages MCP server configurations and connections.
    Handles loading, validation, and organization of MCP servers.
    """

    def __init__(self, mcp_dir: str = "mcp-servers"):
        self.mcp_dir = Path(mcp_dir)
        self.servers: Dict[str, MCPServer] = {}
        self.categories: Dict[str, List[str]] = {}

    def load_server_config(self, config_file: str) -> Dict[str, MCPServer]:
        """
        Load MCP server configurations from a JSON file.

        Args:
            config_file: Path to MCP configuration file

        Returns:
            Dictionary of server name to MCPServer objects
        """
        config_path = self.mcp_dir / config_file

        if not config_path.exists():
            raise FileNotFoundError(f"MCP config not found: {config_path}")

        with open(config_path, 'r') as f:
            config = json.load(f)

        servers = {}
        if 'mcpServers' in config:
            for name, server_config in config['mcpServers'].items():
                server = MCPServer(
                    name=name,
                    command=server_config.get('command', ''),
                    args=server_config.get('args', []),
                    env=server_config.get('env'),
                    description=server_config.get('description'),
                    category=server_config.get('category')
                )
                servers[name] = server
                self.servers[name] = server

                # Organize by category
                category = server.category or 'uncategorized'
                if category not in self.categories:
                    self.categories[category] = []
                self.categories[category].append(name)

        return servers

    def get_server(self, server_name: str) -> Optional[MCPServer]:
        """
        Get an MCP server configuration by name.

        Args:
            server_name: Name of the MCP server

        Returns:
            MCPServer object or None if not found
        """
        return self.servers.get(server_name)

    def get_servers_by_category(self, category: str) -> List[MCPServer]:
        """
        Get all MCP servers in a specific category.

        Args:
            category: Category name (e.g., 'finance', 'data', 'development')

        Returns:
            List of MCPServer objects in that category
        """
        server_names = self.categories.get(category, [])
        return [self.servers[name] for name in server_names if name in self.servers]

    def list_servers(self) -> List[str]:
        """List all loaded MCP server names."""
        return list(self.servers.keys())

    def list_categories(self) -> List[str]:
        """List all MCP server categories."""
        return list(self.categories.keys())

    def generate_claude_config(
        self,
        server_names: List[str],
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Generate Claude desktop app configuration for specified MCP servers.

        Args:
            server_names: List of MCP server names to include
            output_file: Optional path to save configuration

        Returns:
            Configuration dictionary in Claude desktop format
        """
        config = {
            "mcpServers": {}
        }

        for name in server_names:
            if name in self.servers:
                server = self.servers[name]
                config["mcpServers"][name] = {
                    "command": server.command,
                    "args": server.args
                }
                if server.env:
                    config["mcpServers"][name]["env"] = server.env

        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2)

        return config

    def create_server_config(
        self,
        name: str,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        category: Optional[str] = None
    ) -> MCPServer:
        """
        Create a new MCP server configuration.

        Args:
            name: Server name
            command: Command to execute
            args: Command arguments
            env: Environment variables (optional)
            description: Server description (optional)
            category: Server category (optional)

        Returns:
            Created MCPServer object
        """
        server = MCPServer(
            name=name,
            command=command,
            args=args,
            env=env,
            description=description,
            category=category
        )

        self.servers[name] = server

        # Update categories
        cat = category or 'uncategorized'
        if cat not in self.categories:
            self.categories[cat] = []
        self.categories[cat].append(name)

        return server

    def save_server_configs(self, output_file: str) -> Path:
        """
        Save all MCP server configurations to a file.

        Args:
            output_file: Path to save configurations

        Returns:
            Path to saved file
        """
        output_path = self.mcp_dir / output_file

        config = {
            "mcpServers": {}
        }

        for name, server in self.servers.items():
            config["mcpServers"][name] = {
                "command": server.command,
                "args": server.args
            }
            if server.env:
                config["mcpServers"][name]["env"] = server.env
            if server.description:
                config["mcpServers"][name]["description"] = server.description
            if server.category:
                config["mcpServers"][name]["category"] = server.category

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)

        return output_path

    def validate_server_config(self, server: MCPServer) -> tuple[bool, List[str]]:
        """
        Validate an MCP server configuration.

        Args:
            server: MCPServer to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not server.name:
            errors.append("Server name is required")

        if not server.command:
            errors.append("Server command is required")

        if not isinstance(server.args, list):
            errors.append("Server args must be a list")

        if server.env and not isinstance(server.env, dict):
            errors.append("Server env must be a dictionary")

        return (len(errors) == 0, errors)

    def get_recommended_servers_for_domain(self, domain: str) -> List[str]:
        """
        Get recommended MCP servers for a specific domain.

        Args:
            domain: Domain name (e.g., 'business_finance', 'data_science')

        Returns:
            List of recommended server names
        """
        # Predefined recommendations based on framework
        recommendations = {
            'business_finance': [
                'google-sheets',
                'quickbooks',
                'salesforce',
                'financial-apis'
            ],
            'data_science': [
                'postgresql',
                'sqlite',
                'jupyter',
                'pandas-server'
            ],
            'development': [
                'github',
                'gitlab',
                'docker',
                'aws-cli'
            ],
            'research_content': [
                'arxiv',
                'pubmed',
                'notion',
                'knowledge-base'
            ],
            'automation': [
                'slack',
                'email',
                'calendar',
                'monitoring-tools'
            ]
        }

        return recommendations.get(domain, [])


# Predefined MCP Server Templates
MCP_SERVER_TEMPLATES = {
    'google-sheets': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-google-sheets'],
        'description': 'Access and manipulate Google Sheets',
        'category': 'productivity'
    },
    'quickbooks': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-quickbooks'],
        'description': 'Integrate with QuickBooks accounting software',
        'category': 'finance'
    },
    'salesforce': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-salesforce'],
        'description': 'Connect to Salesforce CRM',
        'category': 'crm'
    },
    'postgresql': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-postgres'],
        'description': 'Query PostgreSQL databases',
        'category': 'database'
    },
    'sqlite': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-sqlite'],
        'description': 'Query SQLite databases',
        'category': 'database'
    },
    'github': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-github'],
        'description': 'Interact with GitHub repositories',
        'category': 'development'
    },
    'slack': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-slack'],
        'description': 'Send messages and interact with Slack',
        'category': 'communication'
    }
}


# Example usage
if __name__ == "__main__":
    connector = MCPConnector()

    # Create example servers from templates
    for name, template in MCP_SERVER_TEMPLATES.items():
        server = connector.create_server_config(
            name=name,
            command=template['command'],
            args=template['args'],
            description=template['description'],
            category=template['category']
        )
        print(f"Created server: {server.name} ({server.category})")

    print(f"\nTotal servers: {len(connector.list_servers())}")
    print(f"Categories: {connector.list_categories()}")

    # Get recommended servers for business finance
    finance_servers = connector.get_recommended_servers_for_domain('business_finance')
    print(f"\nRecommended for business_finance: {finance_servers}")

    # Generate Claude config
    config = connector.generate_claude_config(finance_servers)
    print(f"\nGenerated Claude config with {len(config['mcpServers'])} servers")

    # Save configurations
    output_path = connector.save_server_configs("mcp-config.json")
    print(f"Saved configurations to: {output_path}")
