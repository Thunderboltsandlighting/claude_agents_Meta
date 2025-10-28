# Content Creation Project

A complete content creation system powered by the Claude-Agents Framework with 4 specialized AI agents.

## Quick Start

```bash
# Test the workflow
python example_workflow.py

# Use the quick-start script
python ../Claude-Agents/run.py --project .
```

## Your Agents

This project includes 4 specialized agents:

### 1. Content Strategist
- **Role**: Content planning and strategy
- **Temperature**: 0.4 (balanced creativity)
- **Commands**: `/brainstorm`, `/calendar`, `/seo-audit`, `/audience-research`
- **Best for**: Strategy, planning, audience analysis

### 2. Content Writer
- **Role**: Creating high-quality content
- **Temperature**: 0.7 (creative writing)
- **Commands**: `/write`, `/edit`, `/proofread`, `/rewrite`, `/optimize`
- **Best for**: Blog posts, articles, social media, technical writing

### 3. Content Editor
- **Role**: Quality assurance and editing
- **Temperature**: 0.2 (precise corrections)
- **Commands**: `/review`, `/edit`, `/fact-check`, `/style-check`, `/readability`
- **Best for**: Editing, proofreading, fact-checking

### 4. SEO Specialist
- **Role**: SEO optimization and analysis
- **Temperature**: 0.3 (data-driven)
- **Commands**: `/keyword-research`, `/seo-audit`, `/competitor-analysis`, `/optimize`
- **Best for**: Keyword research, SEO strategy, content optimization

## Project Structure

```
my-content-project/
├── README.md                           # This file
├── CONTENT_CREATION_GUIDE.md          # Comprehensive guide
├── example_workflow.py                # Working example
└── agents/
    ├── content-creation-content-strategist/
    │   ├── config.yaml                # Agent configuration
    │   └── prompt.md                  # Agent prompt (Four Core Keys)
    ├── content-creation-content-writer/
    │   ├── config.yaml
    │   └── prompt.md
    ├── content-creation-content-editor/
    │   ├── config.yaml
    │   └── prompt.md
    └── content-creation-seo-specialist/
        ├── config.yaml
        └── prompt.md
```

## Usage Examples

### Example 1: Generate Content Strategy Prompt

```python
import sys
from pathlib import Path
import importlib.util

# Load framework modules
FRAMEWORK_DIR = Path("../Claude-Agents")

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine

# Initialize
manager = AgentManager(agents_dir="agents")
engine = PromptEngine()

# Load strategist
strategist = manager.load_agent("content-creation-content-strategist")

# Generate prompt
prompt = engine.generate_prompt(
    context=strategist.context,
    model=strategist.model,
    tools=strategist.tools,
    task="Create a 30-day content calendar for a tech startup blog"
)

print(prompt)
```

### Example 2: Complete Workflow

See [example_workflow.py](./example_workflow.py) for a complete 4-step workflow:
1. Strategy & Planning
2. SEO Research
3. Content Writing
4. Content Editing

### Example 3: Quick Content Brief

```python
# Load writer agent
writer = manager.load_agent("content-creation-content-writer")

# Generate writing prompt
prompt = engine.generate_prompt(
    context=writer.context,
    model=writer.model,
    tools=writer.tools,
    task="""
    Write a 1500-word blog post about "Building RESTful APIs with Python".

    Target audience: Junior to mid-level developers
    Tone: Professional but approachable
    Include: Code examples, best practices, common pitfalls
    """
)

# Use with Claude API
import anthropic
client = anthropic.Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8000,
    temperature=0.7,
    messages=[{"role": "user", "content": prompt}]
)

content = response.content[0].text
print(content)
```

## Recommended Workflow

```
Strategy → SEO Research → Writing → Editing → Publishing
   ↓           ↓            ↓          ↓
Content    Keywords    First      Final
Planning   Research    Draft    Polished
                                Content
```

1. **Strategy**: Use Content Strategist to plan topics, structure, audience
2. **SEO**: Use SEO Specialist to research keywords and competitors
3. **Writing**: Use Content Writer to create initial draft with SEO keywords
4. **Editing**: Use Content Editor to review, edit, and polish
5. **Publish**: Deploy final content!

## Integration Options

### Option 1: Use Framework Directly (Current Setup)

```python
# Import from framework location
sys.path.insert(0, "../Claude-Agents/core")
from agent_manager import AgentManager
from prompt_engine import PromptEngine
```

### Option 2: Install Framework as Package

```bash
cd ../Claude-Agents
pip install -e .

# Now import from anywhere
from claude_agents import AgentManager, PromptEngine
```

### Option 3: Copy to Your Project

```bash
# Copy agents to your project
cp -r agents /path/to/your/project/

# Copy core modules
cp -r ../Claude-Agents/core /path/to/your/project/
```

## Customization

### Add New Slash Commands

Create a new file in `../Claude-Agents/slash-commands/`:

```markdown
# /your-command.md

Your slash command description and instructions here.
```

Update agent config.yaml:

```yaml
tools:
  slash_commands:
    - /brainstorm
    - /your-command  # Add your new command
```

### Modify Agent Behavior

Edit agent `config.yaml`:

```yaml
model:
  temperature: 0.7  # Adjust creativity (0.0 = precise, 1.0 = creative)
  max_tokens: 8000  # Adjust output length
```

Edit agent `prompt.md`:

```markdown
## KEY 1: CONTEXT

**Role:** Your Custom Role
**Expertise:**
- Your custom expertise
```

### Create Custom Agents

```bash
# Use CLI to create new agent
cd ../Claude-Agents
python core/cli.py create --name my-custom-agent --template base_agent --output ../my-content-project/agents
```

## CLI Commands

```bash
# List available project types
python ../Claude-Agents/core/cli.py list-types

# List available templates
python ../Claude-Agents/core/cli.py list-templates

# Create new agent
python ../Claude-Agents/core/cli.py create --name my-agent --template data_scientist

# Run framework tests
python ../Claude-Agents/core/cli.py test
```

## MCP Server Integration

Configure MCP servers in your Claude desktop config (`~/.config/claude/config.json`):

```json
{
  "mcpServers": {
    "google-analytics": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-google-analytics"]
    },
    "grammarly": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-grammarly"]
    },
    "semrush": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-semrush"]
    }
  }
}
```

## Documentation

- [CONTENT_CREATION_GUIDE.md](./CONTENT_CREATION_GUIDE.md) - Comprehensive guide with examples
- [../Claude-Agents/FRAMEWORK_AS_PACKAGE_GUIDE.md](../Claude-Agents/FRAMEWORK_AS_PACKAGE_GUIDE.md) - Framework integration guide
- [../Claude-Agents/README.md](../Claude-Agents/README.md) - Main framework documentation

## Best Practices

1. **Use Agents in Sequence**: Strategy → SEO → Writing → Editing
2. **Respect Temperature Settings**: Each agent is optimized for its task
3. **Provide Context**: Always include target audience, tone, and requirements
4. **Review Output**: Always use Editor agent for final review
5. **Iterate**: Don't expect perfection on first draft - iterate with agents

## Example Output Structure

When using all 4 agents in sequence, you'll get:

```
1. Strategy Output:
   - Content structure
   - Key themes
   - Audience insights
   - Promotion strategy

2. SEO Output:
   - Target keywords
   - Search intent
   - Competitor gaps
   - Linking strategy

3. Writing Output:
   - Complete draft
   - Markdown formatted
   - SEO optimized
   - Code examples (if applicable)

4. Editing Output:
   - Polished content
   - Error-free
   - Fact-checked
   - Publication-ready
```

## Troubleshooting

### Import Errors

```python
# Use dynamic module loading for hyphenated filenames
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

### Agent Not Found

```bash
# Check agents directory
ls -la agents/

# Verify agent name matches directory
python -c "from pathlib import Path; print(list(Path('agents').iterdir()))"
```

### Prompt Too Long

```python
# Reduce prompt size by loading specific template
prompt = engine.load_template("base_agent_template.txt")
# Then manually insert your task
```

## Next Steps

1. ✅ Run the example: `python example_workflow.py`
2. ✅ Review agent configurations: `cat agents/*/config.yaml`
3. ✅ Read the comprehensive guide: [CONTENT_CREATION_GUIDE.md](./CONTENT_CREATION_GUIDE.md)
4. 📝 Set up your Claude API key
5. 🚀 Start creating content!

## Support

- Framework issues: Check `../Claude-Agents/README.md`
- Agent customization: See agent `prompt.md` files
- Integration help: [CONTENT_CREATION_GUIDE.md](./CONTENT_CREATION_GUIDE.md)

---

**Created with**: Claude-Agents Framework v1.0.0
**Agents**: 4 specialized content creation agents
**Status**: Ready for production use 🚀
