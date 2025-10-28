"""
Claude-Agents Framework
A modular framework for creating specialized Claude AI agents
"""

__version__ = "1.0.0"

# Import core modules for easy access
from pathlib import Path
import sys

# Add core directory to path
FRAMEWORK_DIR = Path(__file__).parent
sys.path.insert(0, str(FRAMEWORK_DIR / "core"))

# Core functionality (optional - for advanced usage)
# from core.agent_manager import AgentManager
# from core.prompt_engine import PromptEngine
# from core.mcp_connector import MCPConnector

__all__ = [
    "AgentManager",
    "PromptEngine",
    "MCPConnector",
    "AgentFactory",
]
