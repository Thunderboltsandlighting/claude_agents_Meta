# Template Review and Corrections

**Date**: 2025-10-27
**Reviewed By**: Claude Agent Framework Team
**Status**: Issues Identified - Corrections Needed

---

## 📋 Issues Identified

### 1. **Filename Typos and Inconsistencies**

| Current Filename | Issue | Correct Filename |
|-----------------|-------|------------------|
| `base_agent templete.txt` | Space in name + typo | `base_agent_template.txt` |
| `business_analyst_templete.txt` | Typo | `business_analyst_template.txt` |
| `data_scientist_templete.txt` | Typo | `data_scientist_template.txt` |
| `thereapist_assistant_template.txt` | Typo | `therapist_assistant_template.txt` |

### 2. **Template Structure Issues**

#### Base Agent Template
**Issues**:
- ❌ Missing variable: `{task_description}` (line 22) - should be `{task}`
- ⚠️ Uses different variable naming than prompt-engine.py expects
- ⚠️ Doesn't fully align with Four Core Keys structure

**Required Variables** (from prompt_engine_example.py):
- `task` (not `task_description`)
- `agent_role`
- `agent_expertise`
- `current_task`
- `user_background`
- `available_tools`
- `constraints`
- `max_tokens`
- `temperature`
- `response_format`
- `methodology_steps`
- `output_format`
- `skills_list`
- `slash_commands`
- `mcp_servers`
- `external_apis`

#### Business Analyst Template
**Issues**:
- ✅ Good: Has hardcoded values for financial analysis
- ⚠️ Uses `{task}` variable but other templates use different naming
- ⚠️ Doesn't match Four Core Keys structure exactly
- ⚠️ Missing integration with prompt-engine.py variable system

### 3. **Misalignment with Framework.md**

The templates need to strictly follow the **Four Core Keys** structure:

```
KEY 1: CONTEXT
- Role
- Expertise
- Scope
- Constraints

KEY 2: MODEL
- Model name
- Max tokens
- Temperature
- Response format

KEY 3: PROMPT
- Task
- Methodology
- Output requirements

KEY 4: TOOLS
- Skills
- Slash commands
- MCP servers
- External APIs
```

Current templates use section headers but don't explicitly label them as "KEY 1", "KEY 2", etc.

### 4. **Integration Issues**

#### prompt_engine_example.py vs Core prompt-engine.py
- **Two different implementations exist**:
  1. `prompts/templates/prompt_engine_example.py` (uses `Template.substitute()`)
  2. `core/prompt-engine.py` (uses `Template.safe_substitute()`)

**Recommendation**: Use `core/prompt-engine.py` as the canonical version.

---

## 🔧 Corrections Required

### Priority 1: Fix Filenames
```bash
cd Claude-Agents/prompts/templates/

# Rename files
mv "base_agent templete.txt" "base_agent_template.txt"
mv "business_analyst_templete.txt" "business_analyst_template.txt"
mv "data_scientist_templete.txt" "data_scientist_template.txt"
mv "thereapist_assistant_template.txt" "therapist_assistant_template.txt"
```

### Priority 2: Standardize Variable Names

All templates should use the same variable names as defined in the framework:

**Standard Variables**:
```python
{
    # Context variables
    "role": "",
    "expertise": "",
    "scope": "",
    "constraints": "",

    # Model variables
    "model_name": "claude-sonnet-4-20250514",
    "max_tokens": "",
    "temperature": "",
    "response_format": "",

    # Prompt variables
    "task": "",
    "methodology_steps": "",
    "output_format": "",

    # Tools variables
    "skills": "",
    "slash_commands": "",
    "mcp_servers": "",
    "external_apis": ""
}
```

### Priority 3: Update Base Template

Create a corrected `base_agent_template.txt`:

```markdown
# Agent System Prompt

## KEY 1: CONTEXT

**Role:** $role

**Expertise:**
$expertise

**Scope:** $scope

**Constraints:**
$constraints

---

## KEY 2: MODEL

**Model Configuration:**
- Model: $model_name
- Max Tokens: $max_tokens
- Temperature: $temperature
- Response Format: $response_format

**Behavior:**
- Maintain accuracy and precision in all outputs
- Follow structured response formats
- Escalate when complexity exceeds thresholds
- Provide clear documentation and reasoning

---

## KEY 3: PROMPT

**Task:** $task

**Methodology:**
$methodology_steps

**Output Requirements:**
$output_format

---

## KEY 4: TOOLS

**Available Skills:**
$skills

**Slash Commands:**
$slash_commands

**MCP Servers:**
$mcp_servers

**External APIs:**
$external_apis

---

## Execution Protocol

1. Receive and parse user task
2. Identify required tools and capabilities
3. Execute using Four Core Keys structure
4. Validate outputs against constraints
5. Deliver results with documentation

**Remember:** You are a specialized agent operating within the Claude-Agents framework. Always maintain the highest standards of accuracy, professionalism, and clarity.
```

### Priority 4: Update Business Analyst Template

Align with agent configuration in `agents/business-analyst/`:

```markdown
# Business Finance Analyst Agent

## KEY 1: CONTEXT

**Role:** Business Finance Analyst

**Expertise:**
- Budget analysis and variance reporting
- Financial forecasting and projections
- KPI reporting and dashboard creation
- Financial statement analysis
- Cost analysis and optimization
- Scenario modeling and what-if analysis

**Scope:** Comprehensive business finance analysis for budget management, forecasting, KPI tracking, and financial decision support

**Constraints:**
- Must maintain 99.9% calculation accuracy
- Handle sensitive financial data with strict security protocols
- Comply with GAAP, IFRS, and SOX standards
- Escalate tasks exceeding complexity score 8 or 20-minute duration
- Never log account numbers, balances, or PII
- Provide audit trails for all calculations

---

## KEY 2: MODEL

**Model Configuration:**
- Model: claude-sonnet-4-20250514
- Max Tokens: 5000
- Temperature: 0.1
- Response Format: structured

---

## KEY 3: PROMPT

**Task:** $task

**Methodology:**
1. **Data Validation & Loading**: Validate data sources, check integrity, load financial data
2. **Core Analysis**: Perform calculations (variance, forecast, KPIs) with 99.9% accuracy
3. **Visualization & Reporting**: Create professional charts, Excel reports, executive summaries
4. **Quality Assurance**: Verify calculations, validate assumptions, ensure compliance

**Output Requirements:**
- Excel Workbooks with professional formatting
- Publication-ready visualizations (PNG/PDF at 300 DPI)
- Executive summaries (3-5 key insights)
- Complete documentation (methodology, assumptions, audit trails)

---

## KEY 4: TOOLS

**Available Skills:**
- xlsx (Excel manipulation and formatting)
- pdf (PDF report generation)
- financial-modeling (Advanced financial calculations)
- reporting (Professional report formatting)

**Slash Commands:**
- /financial - Comprehensive financial analysis
- /kpi - Generate KPI dashboard
- /forecast - Create financial forecasts
- /variance - Budget variance analysis
- /report - Generate formatted reports

**MCP Servers:**
- google-sheets (Collaborative spreadsheet access)
- quickbooks (Accounting data integration)
- salesforce (Sales and revenue data)
- financial-apis (Market data and benchmarks)
- postgresql (Database queries)
- sqlite (Local database access)

**Python Libraries:**
- pandas, numpy (Data manipulation)
- openpyxl, xlsxwriter (Excel export)
- matplotlib, seaborn (Visualization)
- statsmodels, scipy (Statistical analysis)

---

## Execution Protocol

[Same as base template...]
```

---

## 🔄 Integration with prompt-engine.py

### Current State
- `core/prompt-engine.py` uses `safe_substitute()` method
- `prompts/templates/prompt_engine_example.py` uses `substitute()` method
- Templates use curly braces `{variable}` but should use dollar signs `$variable`

### Recommended Changes

**Option 1: Update Templates (Preferred)**
- Change all `{variable}` to `$variable` in templates
- This works with Python's `string.Template` class
- Matches `core/prompt-engine.py` implementation

**Option 2: Update prompt-engine.py**
- Use `str.format()` instead of `Template.safe_substitute()`
- Keep templates with `{variable}` syntax
- Less flexible for partial substitution

**Recommendation**: Go with **Option 1** - update templates to use `$variable` syntax.

---

## 📊 Template Variable Mapping

Map template variables to agent config structure:

| Template Variable | Config Path | Example Value |
|------------------|-------------|---------------|
| `$role` | `context.role` | "Business Finance Analyst" |
| `$expertise` | `context.expertise` (list → formatted) | "- Budget analysis\n- Forecasting\n- KPI reporting" |
| `$scope` | `context.scope` | "Comprehensive business finance analysis..." |
| `$constraints` | `context.constraints` (list → formatted) | "- 99.9% accuracy\n- GAAP compliance" |
| `$model_name` | `model.name` | "claude-sonnet-4-20250514" |
| `$max_tokens` | `model.max_tokens` | "5000" |
| `$temperature` | `model.temperature` | "0.1" |
| `$response_format` | `model.response_format` | "structured" |
| `$task` | User input | "Analyze Q1 budget variance" |
| `$skills` | `tools.skills` (list → formatted) | "- xlsx\n- pdf\n- financial-modeling" |
| `$slash_commands` | `tools.slash_commands` (list → formatted) | "- /financial\n- /kpi\n- /forecast" |
| `$mcp_servers` | `tools.mcp_servers` (list → formatted) | "- google-sheets\n- quickbooks" |

---

## ✅ Action Items

### Immediate (Do Now)
- [ ] Rename all template files (fix typos)
- [ ] Update base_agent_template.txt with correct variable syntax
- [ ] Update business_analyst_template.txt to match agent config
- [ ] Test with prompt-engine.py

### Short Term (This Week)
- [ ] Create updated data_scientist_template.txt
- [ ] Remove or update therapist_assistant_template.txt
- [ ] Update prompt_engine_example.py to use core/prompt-engine.py
- [ ] Add validation for template variables

### Medium Term (This Month)
- [ ] Create templates for additional agent types
- [ ] Add template validation to agent-manager.py
- [ ] Document template creation guidelines
- [ ] Create template generator tool

---

## 🧪 Testing

Test templates with this command:
```python
from core.prompt_engine import PromptEngine
from core.agent_manager import AgentManager

# Load agent
manager = AgentManager(agents_dir="agents")
agent = manager.load_agent("business-analyst")

# Generate prompt from template
engine = PromptEngine(prompts_dir="prompts")
prompt = engine.generate_prompt(
    context=agent.context,
    model=agent.model,
    tools=agent.tools,
    task="Analyze Q1 2025 budget variance",
    template_name="business_analyst_template"
)

print(prompt)
```

---

## 📚 Documentation Updates Needed

Update these files:
1. **README.md**: Add template usage section
2. **agents/business-analyst/README.md**: Create agent-specific docs
3. **prompts/templates/README.md**: Create template documentation

---

## 🎯 Expected Outcome

After corrections:
- ✅ All templates use consistent variable naming
- ✅ Templates align with Four Core Keys structure
- ✅ Integration with core/prompt-engine.py works seamlessly
- ✅ Business analyst template matches agent configuration exactly
- ✅ All filenames follow naming conventions
- ✅ Templates are testable and validated

---

**Priority**: HIGH
**Estimated Time**: 2-3 hours
**Dependencies**: None
**Blocker**: No

Would you like me to implement these corrections now?
