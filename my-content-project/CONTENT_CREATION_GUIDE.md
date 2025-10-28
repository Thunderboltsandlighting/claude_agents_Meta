# Content Creation Project - Integration Guide

## Overview

This project includes 4 specialized agents for content creation:

1. **Content Strategist** - Planning and strategy
2. **Content Writer** - Writing and creation
3. **Content Editor** - Editing and quality assurance
4. **SEO Specialist** - Optimization and analysis

## Quick Start

### Option 1: Using the Quick-Start Script

```bash
# From the Claude-Agents directory
python run.py --project /Users/Coding\ Projects/Claude_Agents_Meta/my-content-project
```

### Option 2: Using the CLI

```bash
# List available agents
cd my-content-project/agents
ls -la

# View agent configuration
cat content-creation-content-strategist/config.yaml
cat content-creation-content-strategist/prompt.md
```

### Option 3: Programmatic Integration

```python
import sys
from pathlib import Path

# Add framework to path
framework_dir = Path("/Users/Coding Projects/Claude_Agents_Meta/Claude-Agents")
sys.path.insert(0, str(framework_dir / "core"))

from agent_manager import AgentManager
from prompt_engine import PromptEngine

# Initialize managers
manager = AgentManager(agents_dir="my-content-project/agents")
engine = PromptEngine()

# Load Content Strategist
strategist = manager.load_agent("content-creation-content-strategist")

# Generate prompt for content planning
prompt = engine.generate_prompt(
    context=strategist.context,
    model=strategist.model,
    tools=strategist.tools,
    task="""
    Create a 30-day content calendar for a tech startup blog.
    Focus areas:
    - AI and machine learning trends
    - Developer tools and tutorials
    - Industry news and analysis
    Target audience: Software developers and tech enthusiasts
    """
)

print(prompt)
```

---

## Agent Details

### 1. Content Strategist

**Purpose**: Content planning, audience research, SEO strategy

**Key Capabilities**:
- Content planning and ideation
- Audience analysis and targeting
- Content calendar management
- SEO optimization strategy
- Brand voice and messaging
- Multi-platform content strategy

**Model Configuration**:
- Temperature: 0.4 (balanced creativity and consistency)
- Max Tokens: 6000

**Available Commands**:
- `/brainstorm` - Generate content ideas
- `/calendar` - Create content calendars
- `/seo-audit` - Audit SEO strategy
- `/audience-research` - Research target audiences

**MCP Servers**:
- google-analytics
- semrush
- ahrefs

**Example Usage**:
```python
strategist = manager.load_agent("content-creation-content-strategist")
prompt = engine.generate_prompt(
    context=strategist.context,
    model=strategist.model,
    tools=strategist.tools,
    task="Create a Q1 2025 content strategy for our SaaS product blog"
)
```

---

### 2. Content Writer

**Purpose**: Creating high-quality content across multiple formats

**Key Capabilities**:
- Long-form content writing
- Blog posts and articles
- Social media copywriting
- Technical writing
- Creative storytelling
- Grammar and style editing

**Model Configuration**:
- Temperature: 0.7 (higher creativity for writing)
- Max Tokens: 8000 (longer content)

**Available Commands**:
- `/write` - Write new content
- `/edit` - Edit existing content
- `/proofread` - Proofread for errors
- `/rewrite` - Rewrite content in different style
- `/optimize` - Optimize for clarity and engagement

**MCP Servers**:
- grammarly
- copyscape

**Example Usage**:
```python
writer = manager.load_agent("content-creation-content-writer")
prompt = engine.generate_prompt(
    context=writer.context,
    model=writer.model,
    tools=writer.tools,
    task="""
    Write a 1500-word blog post about "The Future of AI in Software Development"
    Target audience: Mid-level software developers
    Tone: Professional but conversational
    Include: Code examples, practical tips, industry trends
    """
)
```

---

### 3. Content Editor

**Purpose**: Quality assurance, editing, and content review

**Key Capabilities**:
- Content editing and proofreading
- Style guide enforcement
- Fact-checking and verification
- Content quality assessment
- Readability optimization
- Plagiarism detection

**Model Configuration**:
- Temperature: 0.2 (precise and consistent)
- Max Tokens: 6000

**Available Commands**:
- `/review` - Comprehensive content review
- `/edit` - Edit for clarity and accuracy
- `/fact-check` - Verify facts and claims
- `/style-check` - Check style guide compliance
- `/readability` - Assess and improve readability

**MCP Servers**:
- grammarly
- hemingway
- copyscape

**Example Usage**:
```python
editor = manager.load_agent("content-creation-content-editor")
prompt = engine.generate_prompt(
    context=editor.context,
    model=editor.model,
    tools=editor.tools,
    task="""
    Review this blog post draft for:
    1. Grammar and spelling errors
    2. Style guide compliance (AP style)
    3. Fact accuracy
    4. Readability (target: 8th grade level)
    5. Plagiarism concerns

    [CONTENT TO REVIEW HERE]
    """
)
```

---

### 4. SEO Specialist

**Purpose**: SEO optimization and content performance analysis

**Key Capabilities**:
- Keyword research and analysis
- On-page SEO optimization
- Content performance tracking
- Competitor analysis
- Search intent mapping
- Technical SEO auditing

**Model Configuration**:
- Temperature: 0.3 (data-driven)
- Max Tokens: 5000
- Based on: data_scientist template

**Available Commands**:
- `/keyword-research` - Research target keywords
- `/seo-audit` - Audit content for SEO
- `/competitor-analysis` - Analyze competitor content
- `/optimize` - Optimize content for search

**MCP Servers**:
- google-search-console
- semrush
- ahrefs
- google-analytics

**Example Usage**:
```python
seo = manager.load_agent("content-creation-seo-specialist")
prompt = engine.generate_prompt(
    context=seo.context,
    model=seo.model,
    tools=seo.tools,
    task="""
    Perform keyword research for a blog post about "Python async programming"
    Goals:
    - Find 10-15 high-value keywords
    - Analyze search intent
    - Identify content gaps vs competitors
    - Recommend content structure
    """
)
```

---

## Complete Content Creation Workflow

Here's a complete workflow using all 4 agents:

```python
import sys
from pathlib import Path

# Setup
framework_dir = Path("/Users/Coding Projects/Claude_Agents_Meta/Claude-Agents")
sys.path.insert(0, str(framework_dir / "core"))

from agent_manager import AgentManager
from prompt_engine import PromptEngine

manager = AgentManager(agents_dir="my-content-project/agents")
engine = PromptEngine()

# STEP 1: Strategy & Planning
print("STEP 1: Content Strategy")
strategist = manager.load_agent("content-creation-content-strategist")
strategy_prompt = engine.generate_prompt(
    context=strategist.context,
    model=strategist.model,
    tools=strategist.tools,
    task="Create a content calendar for Q1 2025 focused on AI development tools"
)
# Use strategy_prompt with Claude API to get content strategy
# strategy_result = anthropic_client.messages.create(...)

# STEP 2: SEO Research
print("\nSTEP 2: SEO Research")
seo = manager.load_agent("content-creation-seo-specialist")
seo_prompt = engine.generate_prompt(
    context=seo.context,
    model=seo.model,
    tools=seo.tools,
    task="Research keywords for 'AI-powered code completion tools' article"
)
# Use seo_prompt with Claude API to get keyword research
# seo_result = anthropic_client.messages.create(...)

# STEP 3: Content Writing
print("\nSTEP 3: Content Creation")
writer = manager.load_agent("content-creation-content-writer")
writing_prompt = engine.generate_prompt(
    context=writer.context,
    model=writer.model,
    tools=writer.tools,
    task=f"""
    Write a 2000-word article about AI-powered code completion tools.
    Keywords to include: {seo_result}
    Target audience: Software developers
    Tone: Professional but engaging
    """
)
# Use writing_prompt with Claude API to generate content
# content_draft = anthropic_client.messages.create(...)

# STEP 4: Content Review & Editing
print("\nSTEP 4: Content Review")
editor = manager.load_agent("content-creation-content-editor")
editing_prompt = engine.generate_prompt(
    context=editor.context,
    model=editor.model,
    tools=editor.tools,
    task=f"""
    Review and edit this content:

    {content_draft}

    Check for:
    1. Grammar and spelling
    2. Factual accuracy
    3. Readability (target: 9th grade)
    4. Brand voice consistency
    5. SEO keyword usage
    """
)
# Use editing_prompt with Claude API to review content
# final_content = anthropic_client.messages.create(...)

print("\n✅ Content creation workflow complete!")
```

---

## Integration with Your Existing Project

### Method 1: Install Framework as Package

```bash
# From the Claude-Agents directory
pip install -e .

# Now you can import from anywhere
from claude_agents import AgentManager, PromptEngine
```

### Method 2: Copy Agents to Your Project

```bash
# Copy agents to your project
cp -r my-content-project/agents /path/to/your/project/claude-agents/

# Copy core modules
cp -r Claude-Agents/core /path/to/your/project/claude-agents/
```

### Method 3: Use as External Service

Keep the framework in its own directory and reference it:

```python
import sys
sys.path.insert(0, "/Users/Coding Projects/Claude_Agents_Meta/Claude-Agents/core")

from agent_manager import AgentManager
from prompt_engine import PromptEngine
```

---

## Adding Custom Slash Commands

Create new slash commands in the `Claude-Agents/slash-commands/` directory:

**Example: `/content-brief.md`**

```markdown
# Content Brief Generator

Generate a comprehensive content brief for writers.

## Prompt Structure

You are the Content Strategy Specialist. Generate a detailed content brief.

### Required Information:
1. **Topic**: [Main topic/title]
2. **Target Audience**: [Demographics, interests, pain points]
3. **Keywords**: [Primary and secondary keywords]
4. **Content Type**: [Blog post, article, guide, tutorial, etc.]
5. **Word Count**: [Target word count]
6. **Tone**: [Professional, casual, technical, etc.]

### Brief Components:
1. **Overview**: What this content will cover
2. **Target Keywords**: SEO keywords to include naturally
3. **Key Points**: Main sections/topics to address
4. **Research Notes**: Important facts, statistics, sources
5. **Call-to-Action**: What action should readers take?
6. **Style Guidelines**: Tone, voice, formatting requirements
7. **Competitor Analysis**: What similar content exists?
8. **Success Metrics**: How will we measure success?

### Output Format:
Provide a structured content brief in markdown format ready for the content writer.
```

Then update your agent's config.yaml to include the new command:

```yaml
tools:
  slash_commands:
  - /brainstorm
  - /calendar
  - /seo-audit
  - /audience-research
  - /content-brief  # New command
```

---

## MCP Server Configuration

To use MCP servers with your agents, configure them in your Claude desktop config:

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
    }
  }
}
```

See the main [FRAMEWORK_AS_PACKAGE_GUIDE.md](../FRAMEWORK_AS_PACKAGE_GUIDE.md) for complete MCP setup instructions.

---

## Best Practices

### 1. Agent Collaboration

Use agents in sequence for best results:
- **Strategist** → Plan content strategy
- **SEO Specialist** → Research keywords
- **Writer** → Create content
- **Editor** → Review and refine

### 2. Temperature Settings

Each agent has optimized temperature:
- **Strategist**: 0.4 (balanced)
- **Writer**: 0.7 (creative)
- **Editor**: 0.2 (precise)
- **SEO**: 0.3 (analytical)

### 3. Prompt Engineering

Always provide:
- Clear task description
- Target audience
- Desired output format
- Any constraints or requirements

### 4. Content Quality

- Always use the Editor agent for final review
- Fact-check important claims
- Run plagiarism checks on all content
- Test readability scores

---

## Next Steps

1. **Review Agent Configurations**:
   ```bash
   cd my-content-project/agents
   cat content-creation-*/config.yaml
   ```

2. **Create Custom Slash Commands**:
   - Add content creation workflows
   - Create templates for common tasks

3. **Set Up MCP Servers**:
   - Configure Google Analytics
   - Set up SEO tools integration

4. **Integrate with Your Application**:
   - See FRAMEWORK_AS_PACKAGE_GUIDE.md
   - Use the examples above

5. **Test the Workflow**:
   ```bash
   python run.py --project my-content-project
   ```

---

## Support

For issues or questions:
1. Review the main framework documentation
2. Check agent prompt.md files for capabilities
3. Run `claude-agents test` to verify setup
4. Review agent config.yaml for customization options

---

## Summary

Your content creation project is ready with:
- ✅ 4 specialized agents (Strategy, Writing, Editing, SEO)
- ✅ Pre-configured tools and commands
- ✅ MCP server integrations
- ✅ Four Core Keys framework structure
- ✅ Ready for immediate use or further customization

Start creating content with: `python run.py --project my-content-project`
