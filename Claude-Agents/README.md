# Claude-Agents Framework

A comprehensive framework for building specialized Claude AI agents following Anthropic's best practices and the Four Core Keys structure.

## Framework Structure

```
Claude-Agents/
├── agents/                 # Agent configurations
│   └── business-analyst/   # Business finance analyst agent
│       ├── config.yaml    # Agent configuration
│       └── prompt.md      # Agent prompt template
├── core/                  # Core Python modules
│   ├── agent-manager.py   # Agent lifecycle management
│   ├── prompt-engine.py   # Dynamic prompt generation
│   └── mcp-connector.py   # MCP server integration
├── skills/                # Reusable skills
│   └── xlsx.md           # Excel manipulation skill
├── slash-commands/        # Specialized commands
│   ├── financial.md      # Comprehensive financial analysis
│   ├── kpi.md           # KPI dashboard generation
│   ├── forecast.md      # Financial forecasting
│   ├── variance.md      # Budget variance analysis
│   └── report.md        # Financial report generation
├── mcp-servers/          # MCP server configurations
│   └── business-finance-servers.json
└── prompts/              # Prompt templates
    └── templates/
```

## The Four Core Keys

Every agent in this framework follows the **Four Core Keys** structure:

### 1. CONTEXT
- **Role**: Agent's primary function
- **Expertise**: Areas of specialization
- **Scope**: Boundaries and focus areas
- **Constraints**: Limitations and requirements

### 2. MODEL
- **Name**: Claude model version
- **Max Tokens**: Response length limit
- **Temperature**: Creativity vs. consistency
- **Response Format**: Output structure

### 3. PROMPT
- **Task**: Specific user request
- **Methodology**: Step-by-step approach
- **Output Requirements**: Expected deliverables

### 4. TOOLS
- **Skills**: Specialized capabilities
- **Slash Commands**: Quick workflows
- **MCP Servers**: External integrations
- **Python Libraries**: Technical dependencies

## Quick Start

### 1. Installation

```bash
# Clone or navigate to the framework
cd Claude-Agents

# Install Python dependencies
pip install pandas numpy openpyxl xlsxwriter matplotlib seaborn statsmodels scipy pyyaml

# Install Node.js (for MCP servers)
# macOS: brew install node
# Windows: Download from nodejs.org
```

### 2. Load an Agent

```python
from core.agent_manager import AgentManager

# Initialize manager
manager = AgentManager(agents_dir="agents")

# Load business analyst agent
agent = manager.load_agent("business-analyst")

# Get agent configuration
print(f"Agent: {agent.name}")
print(f"Role: {agent.context['role']}")
print(f"Skills: {agent.get_skills()}")
print(f"Commands: {agent.get_slash_commands()}")

# Generate system prompt
prompt = agent.generate_system_prompt()
print(prompt)
```

### 3. Generate a Prompt

```python
from core.prompt_engine import PromptEngine

engine = PromptEngine(prompts_dir="prompts")

# Generate prompt using Four Core Keys
prompt = engine.generate_prompt(
    context=agent.get_context(),
    model=agent.get_model_config(),
    tools=agent.get_tools(),
    task="Analyze Q1 2025 budget variance"
)

print(prompt)
```

### 4. Configure MCP Servers

```python
from core.mcp_connector import MCPConnector

connector = MCPConnector(mcp_dir="mcp-servers")

# Load MCP server configurations
connector.load_server_config("business-finance-servers.json")

# Get recommended servers for domain
finance_servers = connector.get_recommended_servers_for_domain('business_finance')
print(f"Recommended MCP servers: {finance_servers}")

# Generate Claude desktop configuration
config = connector.generate_claude_config(
    finance_servers,
    output_file="claude_desktop_config.json"
)
```

## Available Agents

### Business Finance Analyst
**Location**: `agents/business-analyst/`

**Specialization**: Business finance analysis, budgeting, forecasting, KPI reporting

**Capabilities**:
- Budget analysis and variance reporting
- Financial forecasting and projections
- KPI reporting and dashboard creation
- Financial statement analysis
- Cost analysis and optimization
- Scenario modeling and what-if analysis

**Slash Commands**:
- `/financial` - Comprehensive financial analysis
- `/kpi` - Generate KPI dashboard
- `/forecast` - Create financial forecasts
- `/variance` - Budget variance analysis
- `/report` - Generate formatted reports

**Configuration**:
```yaml
agent_name: "business-analyst"
model:
  name: "claude-sonnet-4-20250514"
  max_tokens: 5000
  temperature: 0.1
tools:
  skills: ["xlsx", "pdf", "financial-modeling", "reporting"]
  slash_commands: ["/financial", "/kpi", "/forecast", "/report", "/variance"]
  mcp_servers: ["google-sheets", "quickbooks", "salesforce", "financial-apis"]
```

## Creating New Agents

### Step 1: Create Agent Directory

```bash
mkdir -p agents/my-new-agent
```

### Step 2: Create config.yaml

```yaml
agent_name: "my-new-agent"

context:
  role: "Agent Role"
  expertise:
    - "Expertise area 1"
    - "Expertise area 2"
  scope: "Agent scope description"
  constraints:
    - "Constraint 1"
    - "Constraint 2"

model:
  name: "claude-sonnet-4-20250514"
  max_tokens: 4000
  temperature: 0.3
  response_format: "structured"

tools:
  skills: []
  slash_commands: []
  mcp_servers: []
```

### Step 3: Create prompt.md

Follow the Four Core Keys structure:

```markdown
# My New Agent

## KEY 1: CONTEXT
[Define role, expertise, scope, constraints]

## KEY 2: MODEL
[Specify model configuration and behavior]

## KEY 3: PROMPT
[Define task methodology and output requirements]

## KEY 4: TOOLS
[List available skills, commands, servers, libraries]
```

### Step 4: Load and Test

```python
manager = AgentManager()
agent = manager.load_agent("my-new-agent")

# Validate configuration
is_valid, errors = manager.validate_agent_config(agent.config)
if not is_valid:
    print("Validation errors:", errors)
```

## Core Modules

### agent-manager.py
Manages agent lifecycle: loading, validation, orchestration.

**Key Classes**:
- `AgentManager`: Load and manage multiple agents
- `Agent`: Represents a single agent instance

**Usage**:
```python
manager = AgentManager(agents_dir="agents")
agent = manager.load_agent("business-analyst")
```

### prompt-engine.py
Generates dynamic prompts using the Four Core Keys structure.

**Key Features**:
- Generate prompts from configuration
- Apply templates with variable substitution
- Validate prompt structure
- Support custom templates

**Usage**:
```python
engine = PromptEngine()
prompt = engine.generate_prompt(context, model, tools, task)
```

### mcp-connector.py
Manages Model Context Protocol server connections.

**Key Features**:
- Load MCP server configurations
- Generate Claude desktop configs
- Recommend servers by domain
- Validate server configurations

**Usage**:
```python
connector = MCPConnector()
connector.load_server_config("servers.json")
```

## Slash Commands

Slash commands provide quick access to specialized workflows.

### /financial
Comprehensive financial analysis including budget variance, forecasting, and KPI reporting.
```
/financial <data_source> [analysis_type] [output_format]
```

### /kpi
Generate KPI dashboard with financial and operational metrics.
```
/kpi <financial_statements> [kpi_list] [period]
```

### /forecast
Create financial forecasts using multiple statistical methods.
```
/forecast <historical_data> <periods> [method] [scenarios]
```

### /variance
Perform budget variance analysis comparing actual vs. budget.
```
/variance <budget_file> <actuals_file> [threshold] [dimension]
```

### /report
Generate professionally formatted financial reports.
```
/report <data_source> [report_type] [format] [audience]
```

## Skills

Skills are reusable capabilities that agents can utilize.

### xlsx (Excel Manipulation)
- Read/write Excel files
- Apply professional formatting
- Create charts and visualizations
- Generate multi-sheet workbooks

**Dependencies**: `pandas`, `openpyxl`, `xlsxwriter`

## MCP Servers

MCP servers provide external integrations for agents.

### Business Finance Servers
- **google-sheets**: Collaborative spreadsheet access
- **quickbooks**: Accounting data integration
- **salesforce**: Sales and revenue data
- **financial-apis**: Market data and benchmarks
- **postgresql**: Database queries
- **sqlite**: Local database access

## Best Practices

### Agent Design
1. **Clear Role Definition**: Define agent's primary function
2. **Expertise Boundaries**: Limit scope to areas of specialization
3. **Explicit Constraints**: Document limitations and requirements
4. **Escalation Protocols**: Define when to escalate to other agents

### Prompt Engineering
1. **Follow Four Core Keys**: Always use the structured format
2. **Specific Methodology**: Provide step-by-step approach
3. **Clear Output Format**: Define expected deliverables
4. **Tool Documentation**: List all available tools

### Configuration Management
1. **Version Control**: Track agent configuration changes
2. **Validation**: Always validate configs before deployment
3. **Documentation**: Document customizations and rationale
4. **Testing**: Test agents with sample tasks

### Security
1. **Sensitive Data**: Never log financial data or PII
2. **Access Control**: Validate permissions for data access
3. **Audit Trails**: Maintain logs of agent actions
4. **Compliance**: Follow GAAP, IFRS, SOX standards

## Testing

### Test Agent Loading
```python
from core.agent_manager import AgentManager

manager = AgentManager()

# List all agents
print("Available agents:", manager.list_agents())

# Load and validate
agent = manager.load_agent("business-analyst")
is_valid, errors = manager.validate_agent_config(agent.config)

assert is_valid, f"Validation errors: {errors}"
print(f"✓ Agent {agent.name} loaded successfully")
```

### Test Prompt Generation
```python
from core.prompt_engine import PromptEngine

engine = PromptEngine()

prompt = engine.generate_prompt(
    context={"role": "Test", "expertise": ["Testing"], "scope": "Test", "constraints": []},
    model={"name": "claude-sonnet-4-20250514", "max_tokens": 4000, "temperature": 0.3},
    tools={"skills": ["test"], "slash_commands": [], "mcp_servers": []},
    task="Test task"
)

# Validate structure
is_valid, warnings = engine.validate_prompt_structure(prompt)
assert is_valid, f"Prompt validation warnings: {warnings}"
print("✓ Prompt generated and validated")
```

### Test MCP Connectors
```python
from core.mcp_connector import MCPConnector

connector = MCPConnector()
connector.load_server_config("business-finance-servers.json")

# Verify servers loaded
assert len(connector.list_servers()) > 0, "No servers loaded"
print(f"✓ Loaded {len(connector.list_servers())} MCP servers")

# Test recommendations
finance_servers = connector.get_recommended_servers_for_domain('business_finance')
assert 'google-sheets' in finance_servers
assert 'quickbooks' in finance_servers
print("✓ Server recommendations working")
```

## Troubleshooting

### Agent Won't Load
- Check YAML syntax in `config.yaml`
- Verify all required fields are present
- Ensure `prompt.md` exists in agent directory

### Prompt Validation Fails
- Verify Four Core Keys sections are present
- Check for required context elements
- Ensure tools are properly listed

### MCP Server Connection Issues
- Verify Node.js is installed
- Check environment variables are set
- Validate server package names

## Contributing

To add new agents to the framework:

1. Create agent directory under `agents/`
2. Follow the Four Core Keys structure
3. Validate configuration
4. Test with sample tasks
5. Document capabilities and usage

## License

This framework follows Anthropic's Claude agent development best practices.

## Support

For issues or questions:
- Review framework documentation
- Check agent configuration files
- Validate against Four Core Keys structure
- Test with provided examples

---

**Framework Version**: 1.0.0
**Last Updated**: 2025-10-27
**Compatible with**: Claude Sonnet 4.5 (claude-sonnet-4-20250514)
