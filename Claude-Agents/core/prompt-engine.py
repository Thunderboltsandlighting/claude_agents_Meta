"""
Prompt Engine Module
Handles dynamic prompt generation using the Four Core Keys structure
Part of Claude-Agents Framework
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from string import Template


class PromptEngine:
    """
    Generates and manages prompts using the Four Core Keys structure:
    1. Context
    2. Model
    3. Prompt
    4. Tools
    """

    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.templates_dir = self.prompts_dir / "templates"
        self.loaded_templates: Dict[str, str] = {}

    def load_template(self, template_name: str) -> str:
        """
        Load a prompt template from the templates directory.

        Args:
            template_name: Name of the template file (without .md extension)

        Returns:
            Template content as string
        """
        template_path = self.templates_dir / f"{template_name}.md"

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r') as f:
            content = f.read()

        self.loaded_templates[template_name] = content
        return content

    def generate_prompt(
        self,
        context: Dict,
        model: Dict,
        tools: Dict,
        task: str = "",
        template_name: Optional[str] = None
    ) -> str:
        """
        Generate a complete prompt using the Four Core Keys structure.

        Args:
            context: Context configuration (role, expertise, scope, constraints)
            model: Model configuration
            tools: Tools configuration (skills, slash_commands, mcp_servers)
            task: Specific task for the agent (optional)
            template_name: Name of template to use (optional)

        Returns:
            Complete formatted prompt string
        """
        if template_name:
            template_content = self.load_template(template_name)
            return self._apply_template(template_content, context, model, tools, task)

        # Generate default Four Core Keys prompt
        return self._generate_four_keys_prompt(context, model, tools, task)

    def _generate_four_keys_prompt(
        self,
        context: Dict,
        model: Dict,
        tools: Dict,
        task: str = ""
    ) -> str:
        """
        Generate prompt following Four Core Keys structure.

        The Four Core Keys:
        1. CONTEXT - Role, expertise, scope, constraints
        2. MODEL - Configuration and behavior settings
        3. PROMPT - Task description and methodology
        4. TOOLS - Available skills, commands, and integrations
        """

        prompt = f"""# Agent System Prompt

## KEY 1: CONTEXT

**Role:** {context.get('role', 'Specialized Agent')}

**Expertise:**
{self._format_list(context.get('expertise', []))}

**Scope:** {context.get('scope', '')}

**Constraints:**
{self._format_list(context.get('constraints', []))}

---

## KEY 2: MODEL

**Model Configuration:**
- Model: {model.get('name', 'claude-sonnet-4-20250514')}
- Max Tokens: {model.get('max_tokens', 4000)}
- Temperature: {model.get('temperature', 0.3)}
- Response Format: {model.get('response_format', 'structured')}

**Behavior:**
- Maintain accuracy and precision in all outputs
- Follow structured response formats
- Escalate when complexity exceeds thresholds
- Provide clear documentation and reasoning

---

## KEY 3: PROMPT

**Task:** {task if task else '{Task will be provided by user}'}

**Methodology:**
1. **Analysis Phase**: Understand requirements, validate inputs, identify constraints
2. **Execution Phase**: Apply domain expertise, use appropriate tools, generate outputs
3. **Validation Phase**: Verify accuracy, check quality, ensure completeness
4. **Delivery Phase**: Format results professionally, provide documentation, summarize insights

**Output Requirements:**
- Clear, actionable results
- Professional formatting
- Comprehensive documentation
- Quality assurance validation

---

## KEY 4: TOOLS

**Available Skills:**
{self._format_list(tools.get('skills', []))}

**Slash Commands:**
{self._format_list(tools.get('slash_commands', []))}

**MCP Servers:**
{self._format_list(tools.get('mcp_servers', []))}

**Tool Usage Guidelines:**
- Use appropriate tools for each task
- Combine tools when necessary
- Validate tool outputs
- Document tool usage in responses

---

## Execution Protocol

1. Receive and parse user task
2. Identify required tools and capabilities
3. Execute using Four Core Keys structure
4. Validate outputs against constraints
5. Deliver results with documentation

**Remember:** You are a specialized agent operating within the Claude-Agents framework. Always maintain the highest standards of accuracy, professionalism, and clarity.
"""
        return prompt

    def _apply_template(
        self,
        template: str,
        context: Dict,
        model: Dict,
        tools: Dict,
        task: str
    ) -> str:
        """
        Apply context, model, and tools values to a template.

        Args:
            template: Template string with placeholders
            context: Context configuration
            model: Model configuration
            tools: Tools configuration
            task: Task description

        Returns:
            Formatted prompt with values filled in
        """
        # Prepare template variables
        variables = {
            # Context variables
            'role': context.get('role', ''),
            'expertise': self._format_list(context.get('expertise', [])),
            'scope': context.get('scope', ''),
            'constraints': self._format_list(context.get('constraints', [])),

            # Model variables
            'model_name': model.get('name', 'claude-sonnet-4-20250514'),
            'max_tokens': model.get('max_tokens', 4000),
            'temperature': model.get('temperature', 0.3),
            'response_format': model.get('response_format', 'structured'),

            # Tools variables
            'skills': self._format_list(tools.get('skills', [])),
            'slash_commands': self._format_list(tools.get('slash_commands', [])),
            'mcp_servers': self._format_list(tools.get('mcp_servers', [])),

            # Task variable
            'task': task if task else '{Task will be provided by user}'
        }

        # Use safe_substitute to avoid errors on missing variables
        template_obj = Template(template)
        return template_obj.safe_substitute(variables)

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as bullet points."""
        if not items:
            return "- None"
        return '\n'.join(f"- {item}" for item in items)

    def create_template(self, template_name: str, content: str) -> Path:
        """
        Create a new prompt template.

        Args:
            template_name: Name for the template
            content: Template content

        Returns:
            Path to created template file
        """
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        template_path = self.templates_dir / f"{template_name}.md"

        with open(template_path, 'w') as f:
            f.write(content)

        self.loaded_templates[template_name] = content
        return template_path

    def list_templates(self) -> List[str]:
        """List all available prompt templates."""
        if not self.templates_dir.exists():
            return []

        templates = []
        for file in self.templates_dir.glob("*.md"):
            templates.append(file.stem)

        return templates

    def validate_prompt_structure(self, prompt: str) -> tuple[bool, List[str]]:
        """
        Validate that a prompt follows the Four Core Keys structure.

        Args:
            prompt: Prompt string to validate

        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        required_sections = [
            "KEY 1: CONTEXT",
            "KEY 2: MODEL",
            "KEY 3: PROMPT",
            "KEY 4: TOOLS"
        ]

        for section in required_sections:
            if section not in prompt:
                warnings.append(f"Missing required section: {section}")

        # Check for key context elements
        context_elements = ["Role:", "Expertise:", "Scope:", "Constraints:"]
        for element in context_elements:
            if element not in prompt:
                warnings.append(f"Missing context element: {element}")

        # Check for key model elements
        model_elements = ["Model:", "Max Tokens:", "Temperature:"]
        for element in model_elements:
            if element not in prompt:
                warnings.append(f"Missing model element: {element}")

        # Check for tools sections
        tools_sections = ["Available Skills:", "Slash Commands:", "MCP Servers:"]
        for section in tools_sections:
            if section not in prompt:
                warnings.append(f"Missing tools section: {section}")

        return (len(warnings) == 0, warnings)


# Example usage
if __name__ == "__main__":
    engine = PromptEngine()

    # Example configuration
    context = {
        "role": "Business Finance Analyst",
        "expertise": [
            "Budget analysis and variance reporting",
            "Financial forecasting and projections",
            "KPI reporting and dashboard creation"
        ],
        "scope": "Comprehensive business finance analysis",
        "constraints": [
            "Maintain 99.9% calculation accuracy",
            "Handle sensitive financial data securely",
            "Comply with GAAP and IFRS standards"
        ]
    }

    model = {
        "name": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "temperature": 0.3,
        "response_format": "structured"
    }

    tools = {
        "skills": ["xlsx", "pdf", "financial-modeling"],
        "slash_commands": ["/analyze-budget", "/forecast", "/kpi-dashboard"],
        "mcp_servers": ["google-sheets", "quickbooks"]
    }

    # Generate prompt
    prompt = engine.generate_prompt(
        context=context,
        model=model,
        tools=tools,
        task="Analyze Q1 2025 budget variance"
    )

    print(prompt)
    print("\n" + "="*80 + "\n")

    # Validate prompt
    is_valid, warnings = engine.validate_prompt_structure(prompt)
    print(f"Prompt valid: {is_valid}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
