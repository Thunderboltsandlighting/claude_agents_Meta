# Prompt Templates Documentation

**Claude-Agents Framework - Template System**
**Version**: 1.0.0
**Last Updated**: 2025-10-27

---

## Overview

This directory contains prompt templates for creating specialized Claude agents following the **Four Core Keys** structure defined in the Claude-Agents framework. Templates provide reusable, structured formats for agent system prompts that ensure consistency and compliance with framework standards.

---

## The Four Core Keys Structure

Every template in this directory follows the Four Core Keys format:

```
## KEY 1: CONTEXT
- Role: Agent's primary function
- Expertise: Areas of specialization
- Scope: Boundaries and focus areas
- Constraints: Limitations and requirements

## KEY 2: MODEL
- Model: Claude model version
- Max Tokens: Response length limit
- Temperature: Creativity vs. consistency
- Response Format: Output structure
- Behavior: Expected conduct and standards

## KEY 3: PROMPT
- Task: Specific user request (dynamic)
- Methodology: Step-by-step approach
- Output Requirements: Expected deliverables
- Analysis Framework: Detailed workflows

## KEY 4: TOOLS
- Available Skills: Specialized capabilities
- Slash Commands: Quick workflows
- MCP Servers: External integrations
- Python Libraries: Technical dependencies
```

---

## Available Templates

### 1. Base Agent Template
**File**: `base_agent_template.txt`
**Purpose**: Generic foundation for any agent type
**Use Case**: Starting point for custom agents

**Variables**:
- `$role` - Agent role
- `$expertise` - Expertise areas (formatted list)
- `$scope` - Agent scope
- `$constraints` - Constraints (formatted list)
- `$model_name` - Claude model
- `$max_tokens` - Token limit
- `$temperature` - Temperature setting
- `$response_format` - Response format
- `$task` - User task (dynamic)
- `$methodology_steps` - Methodology
- `$output_format` - Output requirements
- `$skills` - Skills (formatted list)
- `$slash_commands` - Commands (formatted list)
- `$mcp_servers` - MCP servers (formatted list)
- `$external_apis` - External APIs (formatted list)

**Example Usage**:
```python
from core.prompt_engine import PromptEngine

engine = PromptEngine()
prompt = engine.generate_prompt(
    context={'role': 'Data Analyst', ...},
    model={'name': 'claude-sonnet-4-20250514', ...},
    tools={'skills': ['python', 'sql'], ...},
    task='Analyze customer data',
    template_name='base_agent_template'
)
```

---

### 2. Business Finance Analyst Template
**File**: `business_analyst_template.txt`
**Purpose**: Financial analysis, budgeting, forecasting, KPI reporting
**Use Case**: Budget variance, financial modeling, business intelligence

**Key Features**:
- Budget analysis and variance reporting
- Financial forecasting (ARIMA, exponential smoothing)
- KPI dashboard generation
- Excel report formatting
- GAAP/IFRS/SOX compliance
- 99.9% calculation accuracy standard

**Variables**:
- `$task` - Specific financial analysis task (only dynamic variable)
- All other content is hardcoded for financial analysis

**Slash Commands**:
- `/financial` - Comprehensive financial analysis
- `/kpi` - KPI dashboard generation
- `/forecast` - Financial forecasting
- `/variance` - Budget variance analysis
- `/report` - Report generation

**Example Usage**:
```python
# Load business analyst agent
from core.agent_manager import AgentManager

manager = AgentManager()
agent = manager.load_agent("business-analyst")

# Generate prompt with specific task
engine = PromptEngine()
prompt = engine.generate_prompt(
    context=agent.context,
    model=agent.model,
    tools=agent.tools,
    task="Analyze Q1 2025 budget variance and forecast Q2",
    template_name="business_analyst_template"
)
```

---

### 3. Data Scientist Template
**File**: `data_scientist_template.txt`
**Purpose**: Statistical analysis, machine learning, data visualization
**Use Case**: Exploratory analysis, predictive modeling, hypothesis testing

**Key Features**:
- Statistical analysis and hypothesis testing
- Machine learning (classification, regression, clustering)
- Data visualization (matplotlib, seaborn)
- Feature engineering and selection
- Model validation and performance optimization
- Reproducible code with Python

**Variables**:
- `$task` - Specific data science task (only dynamic variable)
- All other content hardcoded for data science

**Slash Commands**:
- `/analyze` - Comprehensive data analysis
- `/visualize` - Create visualizations
- `/model` - Train ML models
- `/stats` - Statistical summaries
- `/feature-eng` - Feature engineering

**Python Libraries**:
- pandas, numpy, scikit-learn
- statsmodels, scipy
- matplotlib, seaborn, plotly
- jupyter

**Example Usage**:
```python
prompt = engine.generate_prompt(
    context=data_scientist_context,
    model=model_config,
    tools=data_science_tools,
    task="Analyze customer churn patterns and build predictive model",
    template_name="data_scientist_template"
)
```

---

### 4. Therapist Assistant Template
**File**: `therapist_assistant_template.txt`
**Purpose**: Educational/administrative support (NOT clinical therapy)
**Use Case**: Psychology education, resource compilation, documentation support

**⚠️ CRITICAL**: This template is for **educational and administrative support ONLY**. It does NOT provide clinical diagnosis, therapy, or treatment.

**Key Features**:
- Psychology principles education
- Evidence-based framework descriptions
- Professional development resources
- Documentation and administrative templates
- Professional referral guidance
- Strict ethical boundaries

**Variables**:
- `$task` - Educational/administrative task (only dynamic variable)

**Slash Commands**:
- `/resources` - Find educational resources
- `/framework` - Explain therapeutic frameworks
- `/documentation` - Administrative templates
- `/referral` - Professional referral guidance
- `/ethics` - Ethical guidelines

**Ethical Boundaries**:
- ✓ Educational information from literature
- ✓ Resource compilation
- ✓ Administrative support
- ✗ NO clinical diagnosis
- ✗ NO therapy or treatment
- ✗ NO clinical advice

**Example Usage**:
```python
prompt = engine.generate_prompt(
    context=therapist_assistant_context,
    model=model_config,
    tools=educational_tools,
    task="Provide educational resources on CBT principles for psychology student",
    template_name="therapist_assistant_template"
)
```

---

## Template Variable Syntax

### Using Python's string.Template

Templates use `$variable` syntax (NOT `{variable}`):

**Correct**:
```
Role: $role
Task: $task
```

**Incorrect**:
```
Role: {role}
Task: {task}
```

### Variable Substitution

The prompt engine uses `safe_substitute()` which allows partial substitution:

```python
from string import Template

template_str = """
Role: $role
Task: $task
Skills: $skills
"""

template = Template(template_str)
result = template.safe_substitute(
    role="Data Analyst",
    task="Analyze sales data"
    # skills missing - will remain as $skills
)
```

---

## Creating Custom Templates

### Step 1: Copy Base Template

```bash
cp prompts/templates/base_agent_template.txt prompts/templates/my_agent_template.txt
```

### Step 2: Update Four Core Keys

Edit the template following the Four Core Keys structure:

```markdown
# My Custom Agent

## KEY 1: CONTEXT
**Role:** [Agent role]
**Expertise:**
- [Area 1]
- [Area 2]
**Scope:** [Agent scope]
**Constraints:**
- [Constraint 1]

## KEY 2: MODEL
**Model Configuration:**
- Model: claude-sonnet-4-20250514
- Max Tokens: [number]
- Temperature: [0.0-1.0]
- Response Format: [structured|conversational|code]

## KEY 3: PROMPT
**Task:** $task

**Methodology:**
1. [Step 1]
2. [Step 2]

**Output Requirements:**
- [Requirement 1]
- [Requirement 2]

## KEY 4: TOOLS
**Available Skills:**
- [skill-1]
- [skill-2]

**Slash Commands:**
- /command1 - Description
- /command2 - Description

**MCP Servers:**
- server-1
- server-2
```

### Step 3: Choose Variable Strategy

**Option A: All Variables** (like base template)
- Use `$variable` for all configurable elements
- Maximum flexibility
- Requires complete variable mapping

**Option B: Hardcoded Content** (like business analyst template)
- Only `$task` is dynamic
- Rest is specialized content
- Best for domain-specific agents

### Step 4: Test Template

```python
from core.prompt_engine import PromptEngine

engine = PromptEngine()

# Test loading
template = engine.load_template('my_agent_template')
assert template is not None

# Test generation
prompt = engine.generate_prompt(
    context=test_context,
    model=test_model,
    tools=test_tools,
    task="Test task",
    template_name='my_agent_template'
)

# Validate structure
is_valid, warnings = engine.validate_prompt_structure(prompt)
print(f"Valid: {is_valid}")
if warnings:
    print("Warnings:", warnings)
```

---

## Template Best Practices

### 1. Follow Four Core Keys

**ALWAYS include all four keys**:
```
## KEY 1: CONTEXT
## KEY 2: MODEL
## KEY 3: PROMPT
## KEY 4: TOOLS
```

### 2. Use Consistent Variable Names

Match variable names in `core/prompt-engine.py`:
- `$role`, `$expertise`, `$scope`, `$constraints`
- `$model_name`, `$max_tokens`, `$temperature`
- `$task`, `$methodology_steps`, `$output_format`
- `$skills`, `$slash_commands`, `$mcp_servers`

### 3. Document Expectations

Include clear execution protocols:
- Phase-by-phase workflows
- Quality standards
- Escalation criteria
- Best practices

### 4. Provide Examples

Include code examples, workflow examples, output examples:

```markdown
### Example Workflow
\`\`\`python
# Example code showing expected approach
\`\`\`
```

### 5. Define Boundaries

Clearly state what the agent should/shouldn't do:

```markdown
**Always:**
- ✓ Action 1
- ✓ Action 2

**Never:**
- ✗ Action 3
- ✗ Action 4
```

### 6. Include Quality Standards

Define output quality requirements:

```markdown
## Output Quality Standards
Every deliverable must include:
- ✓ Requirement 1
- ✓ Requirement 2
- ✓ Requirement 3
```

---

## Integration with Agent Manager

### Loading Agent and Generating Prompt

```python
from core.agent_manager import AgentManager
from core.prompt_engine import PromptEngine

# 1. Load agent configuration
manager = AgentManager(agents_dir="agents")
agent = manager.load_agent("business-analyst")

# 2. Initialize prompt engine
engine = PromptEngine(prompts_dir="prompts")

# 3. Generate prompt from template
prompt = engine.generate_prompt(
    context=agent.context,
    model=agent.model,
    tools=agent.tools,
    task="Analyze Q1 budget variance",
    template_name="business_analyst_template"
)

# 4. Use prompt with Claude
# Send to Claude API with generated prompt
```

### Template Variable Mapping

How agent config maps to template variables:

| Agent Config Path | Template Variable | Format |
|-------------------|-------------------|--------|
| `context.role` | `$role` | String |
| `context.expertise` | `$expertise` | Formatted list |
| `context.scope` | `$scope` | String |
| `context.constraints` | `$constraints` | Formatted list |
| `model.name` | `$model_name` | String |
| `model.max_tokens` | `$max_tokens` | String |
| `model.temperature` | `$temperature` | String |
| `model.response_format` | `$response_format` | String |
| User input | `$task` | String |
| `tools.skills` | `$skills` | Formatted list |
| `tools.slash_commands` | `$slash_commands` | Formatted list |
| `tools.mcp_servers` | `$mcp_servers` | Formatted list |

---

## Template Validation

### Automated Validation

```python
def validate_template(template_path):
    """Validate template structure"""
    with open(template_path) as f:
        content = f.read()

    errors = []

    # Check Four Core Keys
    required_keys = [
        "KEY 1: CONTEXT",
        "KEY 2: MODEL",
        "KEY 3: PROMPT",
        "KEY 4: TOOLS"
    ]

    for key in required_keys:
        if key not in content:
            errors.append(f"Missing: {key}")

    # Check variable syntax
    if '{' in content and '}' in content:
        errors.append("Use $variable syntax, not {variable}")

    # Check required sections
    required_sections = [
        "Role:",
        "Expertise:",
        "Scope:",
        "Constraints:",
        "Task:",
        "Methodology:",
        "Output Requirements:",
        "Available Skills:"
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing section: {section}")

    return len(errors) == 0, errors

# Validate all templates
templates = [
    'base_agent_template.txt',
    'business_analyst_template.txt',
    'data_scientist_template.txt',
    'therapist_assistant_template.txt'
]

for template in templates:
    is_valid, errors = validate_template(f'prompts/templates/{template}')
    if is_valid:
        print(f"✓ {template} is valid")
    else:
        print(f"✗ {template} has errors:")
        for error in errors:
            print(f"  - {error}")
```

---

## Troubleshooting

### Issue: Template Not Found

**Error**: `Template {name} not found`

**Solution**:
```python
# Check template exists
import os
template_path = "prompts/templates/my_template.txt"
assert os.path.exists(template_path), f"Template not found: {template_path}"
```

### Issue: Variable Not Substituted

**Error**: `$variable` appears in output

**Solutions**:
1. Check variable is in substitution dict
2. Use `safe_substitute()` (allows partial substitution)
3. Verify variable name matches exactly

```python
# Debug variable substitution
template = Template("Role: $role, Task: $task")
result = template.safe_substitute(role="Analyst")  # task remains $task
print(result)  # "Role: Analyst, Task: $task"
```

### Issue: Syntax Error in Template

**Error**: `Invalid template syntax`

**Solution**:
- Check all `$` signs are for variables
- Escape literal `$` with `$$`
- Verify no stray braces `{}`

```markdown
Correct: $variable
Incorrect: {variable}
Literal dollar: This costs $$100
```

### Issue: Four Core Keys Missing

**Error**: Validation fails

**Solution**:
Ensure all keys are explicitly labeled:
```markdown
## KEY 1: CONTEXT
## KEY 2: MODEL
## KEY 3: PROMPT
## KEY 4: TOOLS
```

---

## File Organization

```
prompts/
└── templates/
    ├── README.md                        # This file
    ├── base_agent_template.txt          # Generic base template
    ├── business_analyst_template.txt    # Finance agent
    ├── data_scientist_template.txt      # Data science agent
    ├── therapist_assistant_template.txt # Educational support
    ├── implementation_guide.txt         # Implementation guide
    └── prompt_engine_example.py         # Usage examples
```

---

## Version History

### v1.0.0 (2025-10-27)
- Initial release
- Four templates: base, business analyst, data scientist, therapist assistant
- Four Core Keys structure standardized
- Variable syntax updated to `$variable` format
- Comprehensive documentation created

---

## Contributing

### Adding New Templates

1. Create template file following Four Core Keys structure
2. Use `$variable` syntax for substitution
3. Add documentation to this README
4. Add validation tests
5. Test with prompt engine
6. Submit for review

### Template Naming Convention

- Use descriptive names: `{agent_type}_template.txt`
- Examples: `marketing_analyst_template.txt`, `devops_engineer_template.txt`
- Keep names lowercase with underscores

---

## Additional Resources

- **Framework Documentation**: `../README.md`
- **Agent Manager**: `../core/agent-manager.py`
- **Prompt Engine**: `../core/prompt-engine.py`
- **Agent Configurations**: `../agents/`
- **Framework Specification**: `../../Framework.md`

---

## Support

For questions or issues:
1. Review this documentation
2. Check template examples
3. Validate with prompt engine
4. Test with agent manager
5. Review framework specifications

---

**Templates are the foundation of consistent, high-quality agent prompts. Follow the Four Core Keys, use proper variable syntax, and validate thoroughly.**

🎯 **Quality templates = Effective agents**
