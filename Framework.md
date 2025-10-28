# Claude-Agents Project Instructions

## Project Overview

**Claude-Agents** is a modular system for creating specialized AI sub-agents that leverage skills, custom slash commands, structured prompts, and MCP (Model Context Protocol) servers to handle specific tasks efficiently.

## Core Architecture

### 1. Agent Framework Structure

```
Claude-Agents/
├── agents/
│   ├── data-scientist/
│   ├── business-analyst/
│   ├── therapist-assistant/
│   └── code-reviewer/
├── skills/
│   ├── shared/
│   └── agent-specific/
├── slash-commands/
├── mcp-servers/
├── prompts/
│   └── templates/
└── core/
    ├── agent-manager.py
    ├── prompt-engine.py
    └── mcp-connector.py
```

## 2. The Four Core Keys Framework

Every agent prompt must incorporate these elements:

### **Context**
- Agent's role and expertise
- Current task scope
- Available tools and limitations
- User background/preferences (when relevant)

### **Model** 
- Specific Claude model to use
- Response format requirements
- Token limits and constraints
- Temperature/creativity settings

### **Prompt**
- Clear task instructions
- Step-by-step methodology
- Expected output format
- Error handling procedures

### **Tools**
- Required skills and capabilities
- MCP server connections
- External API integrations
- Slash command availability

## 3. Agent Creation Template

```python
class AgentTemplate:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.context = self._define_context()
        self.model_config = self._configure_model()
        self.prompt_template = self._create_prompt_template()
        self.tools = self._initialize_tools()
        
    def _define_context(self):
        return {
            "role": "",
            "expertise": [],
            "scope": "",
            "constraints": []
        }
    
    def _configure_model(self):
        return {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "temperature": 0.3,
            "response_format": "structured"
        }
    
    def _create_prompt_template(self):
        return """
        CONTEXT: {context}
        
        ROLE: You are a specialized {role} agent with expertise in {expertise}.
        
        TASK: {task}
        
        METHODOLOGY:
        1. {step_1}
        2. {step_2}
        3. {step_3}
        
        TOOLS AVAILABLE: {tools}
        
        OUTPUT FORMAT: {format}
        
        CONSTRAINTS: {constraints}
        """
        
    def _initialize_tools(self):
        return {
            "skills": [],
            "slash_commands": [],
            "mcp_servers": [],
            "external_apis": []
        }
```

## 4. Slash Command System

### Core Slash Commands
- `/agent create <name> <type>` - Create new agent
- `/agent list` - Show all available agents
- `/agent switch <name>` - Switch to specific agent
- `/skill load <skill_name>` - Load additional skill
- `/mcp connect <server_name>` - Connect MCP server
- `/context update <key> <value>` - Update context variables

### Custom Slash Commands per Agent
```python
# Data Science Agent
/analyze dataset <file>
/visualize <data> <chart_type>
/model train <algorithm> <parameters>
/stats summary <data>

# Business Analyst Agent
/financial analyze <statements>
/kpi calculate <metrics>
/forecast <data> <periods>
/report generate <template>

# Therapist Assistant Agent
/assessment create <type>
/intervention suggest <issue>
/resources find <topic>
/progress track <client_id>

# Code Reviewer Agent
/review analyze <code>
/security scan <files>
/performance check <function>
/documentation generate <module>
```

## 5. MCP Server Integration

### When to Incorporate MCP Servers

**Required for:**
- External database connections
- API integrations with third-party services
- Real-time data fetching
- File system operations beyond basic read/write
- Complex workflow orchestration

**Implementation Pattern:**
```python
class MCPConnector:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.active_servers = {}
        
    def register_server(self, server_name, config):
        """Register MCP server for agent use"""
        if self._is_required_for_agent(server_name):
            self.active_servers[server_name] = config
            
    def _is_required_for_agent(self, server_name):
        """Determine if MCP server is needed for agent tasks"""
        requirements = {
            "data-scientist": ["database", "analytics-api"],
            "business-analyst": ["financial-api", "reporting"],
            "therapist-assistant": ["secure-storage", "assessment-tools"],
            "code-reviewer": ["git-integration", "security-scanner"]
        }
        return server_name in requirements.get(self.agent_name, [])
```

## 6. Agent Implementations

### Data Science Agent
```python
data_scientist_agent = {
    "context": {
        "role": "Senior Data Scientist",
        "expertise": ["statistical_analysis", "machine_learning", "data_visualization"],
        "scope": "Data analysis, modeling, and insights generation",
        "constraints": ["privacy_compliant", "reproducible_results"]
    },
    "model_config": {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 6000,
        "temperature": 0.2
    },
    "tools": {
        "skills": ["xlsx", "pdf", "statistical-analysis"],
        "slash_commands": ["/analyze", "/visualize", "/model", "/stats"],
        "mcp_servers": ["database-connector", "analytics-api"],
        "external_apis": ["pandas", "scikit-learn", "matplotlib"]
    }
}
```

### Business Analyst Agent
```python
business_analyst_agent = {
    "context": {
        "role": "Business Financial Analyst",
        "expertise": ["financial_modeling", "kpi_analysis", "forecasting"],
        "scope": "Business performance analysis and strategic insights",
        "constraints": ["confidential_data", "regulatory_compliance"]
    },
    "model_config": {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 5000,
        "temperature": 0.1
    },
    "tools": {
        "skills": ["xlsx", "financial-modeling", "reporting"],
        "slash_commands": ["/financial", "/kpi", "/forecast", "/report"],
        "mcp_servers": ["financial-data-api", "reporting-engine"],
        "external_apis": ["quickbooks", "stripe", "financial-databases"]
    }
}
```

## 7. Implementation Steps

### Phase 1: Core Framework
1. Create agent manager system
2. Implement prompt engine with 4-key structure
3. Build slash command parser
4. Establish MCP connector foundation

### Phase 2: Agent Development
1. Implement data scientist agent
2. Create business analyst agent
3. Build therapist assistant agent
4. Develop code reviewer agent

### Phase 3: Integration & Testing
1. Connect MCP servers for each agent
2. Test slash command functionality
3. Validate skill integration
4. Performance optimization

### Phase 4: Advanced Features
1. Agent collaboration workflows
2. Cross-agent skill sharing
3. Dynamic MCP server discovery
4. Custom skill creation tools

## 8. Configuration Files

### Agent Config Template
```yaml
agent_name: "data-scientist"
version: "1.0"
context:
  role: "Senior Data Scientist"
  expertise: 
    - "statistical_analysis"
    - "machine_learning"
    - "data_visualization"
  scope: "Data analysis, modeling, and insights generation"
  constraints:
    - "privacy_compliant"
    - "reproducible_results"

model:
  name: "claude-sonnet-4-20250514"
  max_tokens: 6000
  temperature: 0.2
  response_format: "structured"

tools:
  skills:
    - "xlsx"
    - "pdf" 
    - "statistical-analysis"
  slash_commands:
    - "/analyze"
    - "/visualize"
    - "/model"
    - "/stats"
  mcp_servers:
    - name: "database-connector"
      required: true
      config: "config/database.json"
    - name: "analytics-api"
      required: false
      config: "config/analytics.json"
```

## 9. Usage Examples

### Creating and Using an Agent
```bash
# Create new data science agent
/agent create ds-analyst data-scientist

# Load additional skills
/skill load advanced-statistics
/skill load ml-algorithms

# Connect required MCP servers
/mcp connect database-connector
/mcp connect analytics-api

# Execute agent-specific commands
/analyze dataset sales_data.csv
/visualize sales_data line_chart
/model train random_forest {"n_estimators": 100}
```

### Agent Collaboration
```bash
# Business analyst requests data from data scientist
/agent data-scientist /analyze dataset financial_data.xlsx
/agent switch business-analyst
/financial analyze /previous_analysis
/report generate quarterly_summary
```

This framework provides a robust foundation for creating specialized Claude sub-agents that can handle complex, domain-specific tasks while maintaining consistency and leveraging appropriate tools and integrations.