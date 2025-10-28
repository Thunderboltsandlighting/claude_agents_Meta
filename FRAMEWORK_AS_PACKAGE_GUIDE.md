# Using Claude-Agents Framework as a Reusable Package

**Your framework is now a modular, reusable package that can be integrated into any project!**

---

## 🎯 Overview

Your Claude-Agents framework can:
- ✅ Be imported into any Python project
- ✅ Dynamically create new agents based on project needs
- ✅ Auto-detect and deploy appropriate agents
- ✅ Adapt to different domains (finance, data science, SQL, web analytics, etc.)
- ✅ Scale with your project requirements

---

## 📦 Installation

### Option 1: Direct Usage (Development)

```bash
# From any project
import sys
sys.path.insert(0, '/path/to/Claude_Agents_Meta/Claude-Agents')

from core.agent_factory import AgentFactory
```

### Option 2: Install as Package (Recommended)

```bash
cd /path/to/Claude_Agents_Meta/Claude-Agents
pip install -e .
```

Now you can import from anywhere:
```python
from claude_agents.core.agent_factory import AgentFactory
```

---

## 🚀 Quick Start Examples

### Example 1: SQL Database Analysis Project

```python
from pathlib import Path
from core.agent_factory import AgentFactory

# Initialize factory
factory = AgentFactory(framework_dir="/path/to/Claude-Agents")

# Auto-create agents for SQL project
agents = factory.auto_create_agents_for_project(
    project_type="sql_database_analysis",
    project_name="customer-db",
    output_dir=Path("my_project/agents")
)

# This creates:
# - customer-db-sql-analyst (data scientist template, customized for SQL)
# - customer-db-business-reporter (business analyst template)

print(f"✓ Created {len(agents)} agents ready for SQL analysis")
```

### Example 2: Custom Agent for Specific Need

```python
# Create a specialized agent for your exact requirements
factory = AgentFactory()

custom_agent = factory.create_agent(
    agent_name="sales-performance-analyst",
    agent_type="business_analyst",  # Use business analyst template
    context={
        'role': 'Sales Performance Analyst',
        'expertise': [
            'Sales metrics and KPIs',
            'Territory analysis',
            'Quota tracking',
            'Commission calculations',
            'Sales forecasting'
        ],
        'scope': 'Sales team performance analysis and reporting',
        'constraints': [
            'Real-time data requirements',
            'Multi-region support',
            'Confidential compensation data'
        ]
    },
    model={
        'name': 'claude-sonnet-4-20250514',
        'max_tokens': 5000,
        'temperature': 0.1,
        'response_format': 'structured'
    },
    tools={
        'skills': ['xlsx', 'salesforce-integration', 'reporting'],
        'slash_commands': [
            '/sales-analysis',
            '/territory-report',
            '/quota-tracker',
            '/commission-calc'
        ],
        'mcp_servers': ['salesforce', 'google-sheets']
    },
    output_dir=Path("my_project/agents")
)

print(f"✓ Custom agent created: {custom_agent}")
```

### Example 3: Complete Project Integration

```python
"""
Complete example: SQL Database + Agent Analysis Pipeline
"""

import sys
sys.path.insert(0, 'Claude-Agents')

from pathlib import Path
from core.agent_factory import AgentFactory
from core.agent_manager import AgentManager
from core.prompt_engine import PromptEngine
import sqlite3
import pandas as pd

class ProjectWithAgents:
    """Your project using Claude-Agents framework"""

    def __init__(self, project_name: str, project_type: str):
        self.project_name = project_name
        self.project_dir = Path(f"projects/{project_name}")
        self.project_dir.mkdir(parents=True, exist_ok=True)

        # Initialize framework components
        self.factory = AgentFactory(framework_dir="Claude-Agents")
        self.agent_manager = None
        self.prompt_engine = None

        # Create agents for this project
        self.setup_agents(project_type)

    def setup_agents(self, project_type: str):
        """Automatically create and configure agents"""
        print(f"\n{'='*60}")
        print(f"Setting up agents for '{self.project_name}' ({project_type})")
        print(f"{'='*60}")

        # Auto-create agents based on project type
        agents = self.factory.auto_create_agents_for_project(
            project_type=project_type,
            project_name=self.project_name,
            output_dir=self.project_dir / "agents"
        )

        print(f"\n✓ Created {len(agents)} agents:")
        for agent_path in agents:
            print(f"  - {agent_path.name}")

        # Initialize agent manager for this project
        self.agent_manager = AgentManager(
            agents_dir=str(self.project_dir / "agents")
        )
        self.prompt_engine = PromptEngine(
            prompts_dir="Claude-Agents/prompts"
        )

    def analyze_data(self, data_file: str, analysis_type: str = "comprehensive"):
        """Run analysis using project agents"""
        print(f"\n{'='*60}")
        print(f"Analyzing: {data_file}")
        print(f"{'='*60}")

        # Load data
        if data_file.endswith('.csv'):
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)

        print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")

        # Get available agents for this project
        available_agents = self.agent_manager.list_agents()
        print(f"\nAvailable agents: {', '.join(available_agents)}")

        # Use agents to analyze
        results = {}

        for agent_name in available_agents:
            print(f"\n--- Loading {agent_name} ---")
            agent = self.agent_manager.load_agent(agent_name)

            # Generate analysis task
            task = self._generate_task(df, analysis_type, agent.context['role'])

            # Generate prompt
            prompt = self.prompt_engine.generate_prompt(
                context=agent.context,
                model=agent.model,
                tools=agent.tools,
                task=task
            )

            print(f"✓ Generated prompt ({len(prompt)} chars)")

            results[agent_name] = {
                'agent': agent,
                'prompt': prompt,
                'data': df
            }

        return results

    def _generate_task(self, df: pd.DataFrame, analysis_type: str, agent_role: str) -> str:
        """Generate appropriate task based on agent role and data"""

        base_info = f"""
Dataset Overview:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column Names: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}
"""

        if 'Business' in agent_role or 'Finance' in agent_role:
            task = f"""Perform business analysis on the provided dataset.

{base_info}

Required Analysis:
1. Key business metrics and KPIs
2. Trends and patterns
3. Performance insights
4. Actionable recommendations

Deliverables:
- Executive summary
- Detailed metrics
- Visualizations
- Excel report
"""
        elif 'Data Scientist' in agent_role or 'SQL' in agent_role:
            task = f"""Perform statistical and data science analysis.

{base_info}

Required Analysis:
1. Exploratory data analysis (EDA)
2. Statistical summaries
3. Correlation analysis
4. Anomaly detection
5. Predictive insights (if applicable)

Deliverables:
- Statistical report
- Visualizations
- Reproducible code
- Recommendations
"""
        else:
            task = f"""Analyze the dataset and provide comprehensive insights.

{base_info}

Provide thorough analysis with clear findings and recommendations.
"""

        return task

# Example Usage
def main():
    # Create new project with agents
    project = ProjectWithAgents(
        project_name="sales-analysis-2024",
        project_type="sql_database_analysis"  # or "financial_analysis", "data_science", etc.
    )

    # Analyze data with the created agents
    results = project.analyze_data(
        data_file="data/sales_2024.csv",
        analysis_type="comprehensive"
    )

    # Results now contain prompts ready for Claude API
    print(f"\n{'='*60}")
    print("ANALYSIS READY")
    print(f"{'='*60}")
    print(f"Generated {len(results)} analysis prompts")
    print("\nNext: Send prompts to Claude API for insights")

if __name__ == "__main__":
    main()
```

---

## 🏗️ Project Types Supported

The factory recognizes these project types and auto-creates appropriate agents:

### 1. `sql_database_analysis`
**Creates**:
- SQL Database Analyst (data scientist template, customized)
- Business Reporter (business analyst template)

**Use For**:
- Spreadsheet → SQL database projects
- Database performance analysis
- SQL query optimization
- Data reporting pipelines

### 2. `financial_analysis`
**Creates**:
- Finance Analyst (business analyst template)

**Use For**:
- Budget analysis
- Financial forecasting
- KPI dashboards
- Variance reporting

### 3. `data_science`
**Creates**:
- Data Analyst (data scientist template)

**Use For**:
- Statistical analysis
- Machine learning models
- Predictive analytics
- Data exploration

### 4. `customer_analysis`
**Creates**:
- Customer Analyst (data scientist, customized)
- Business Strategist (business analyst)

**Use For**:
- Customer segmentation
- Churn prediction
- LTV analysis
- RFM analysis

### 5. `web_analytics`
**Creates**:
- Web Analyst (data scientist, customized)

**Use For**:
- Website analytics
- User behavior analysis
- Conversion optimization
- A/B testing

### 6. `full_stack`
**Creates**:
- Data Scientist
- Business Analyst

**Use For**:
- Comprehensive projects needing multiple perspectives
- Complex analysis pipelines

---

## 🎨 Customizing Agents

### Light Customization (Use Template)

```python
factory = AgentFactory()

agent = factory.create_agent_from_template(
    agent_name="my-custom-analyst",
    template_name="business_analyst",  # Use existing template
    customizations={
        'context': {
            'scope': 'Specialized for retail analytics'
        },
        'tools': {
            'mcp_servers': ['shopify', 'stripe']  # Add retail-specific tools
        }
    }
)
```

### Heavy Customization (Build from Scratch)

```python
agent = factory.create_agent(
    agent_name="completely-custom-agent",
    agent_type="base_agent",  # Start from base
    context={
        'role': 'Your Custom Role',
        'expertise': ['Skill 1', 'Skill 2', 'Skill 3'],
        'scope': 'Your custom scope',
        'constraints': ['Constraint 1', 'Constraint 2']
    },
    model={
        'name': 'claude-sonnet-4-20250514',
        'max_tokens': 4000,
        'temperature': 0.3,
        'response_format': 'structured'
    },
    tools={
        'skills': ['custom-skill-1', 'custom-skill-2'],
        'slash_commands': ['/custom-command'],
        'mcp_servers': ['custom-server']
    }
)
```

---

## 📊 Real-World Integration Examples

### Example 1: Flask Web App with Agents

```python
from flask import Flask, request, jsonify
from core.agent_factory import AgentFactory
from core.agent_manager import AgentManager
from core.prompt_engine import PromptEngine

app = Flask(__name__)

# Initialize framework on startup
factory = AgentFactory()
agents_created = factory.auto_create_agents_for_project(
    project_type="web_analytics",
    project_name="my-webapp",
    output_dir="agents"
)

agent_manager = AgentManager(agents_dir="agents")
prompt_engine = PromptEngine()

@app.route('/analyze', methods=['POST'])
def analyze_data():
    """API endpoint that uses agents for analysis"""
    data = request.json

    # Load appropriate agent
    agent = agent_manager.load_agent("my-webapp-web-analyst")

    # Generate prompt
    prompt = prompt_engine.generate_prompt(
        context=agent.context,
        model=agent.model,
        tools=agent.tools,
        task=data['analysis_request']
    )

    # Send to Claude (simplified)
    # result = claude_api.analyze(prompt)

    return jsonify({
        'status': 'success',
        'prompt_generated': True,
        'prompt_length': len(prompt)
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Example 2: Jupyter Notebook Integration

```python
# notebook.ipynb

import sys
sys.path.insert(0, '../Claude-Agents')

from core.agent_factory import AgentFactory
import pandas as pd

# Create agents for this analysis
factory = AgentFactory()
agents = factory.auto_create_agents_for_project(
    project_type="data_science",
    project_name="notebook-analysis",
    output_dir="notebook_agents"
)

# Load data
df = pd.read_csv('data.csv')

# Get data scientist agent
from core.agent_manager import AgentManager
manager = AgentManager(agents_dir="notebook_agents")
agent = manager.load_agent("notebook-analysis-data-analyst")

# Generate analysis prompt
from core.prompt_engine import PromptEngine
engine = PromptEngine()

prompt = engine.generate_prompt(
    context=agent.context,
    model=agent.model,
    tools=agent.tools,
    task=f"Analyze this dataset with {len(df)} rows and {len(df.columns)} columns. Provide statistical summary and insights."
)

print(f"✓ Analysis prompt ready ({len(prompt)} characters)")
# Send to Claude API...
```

### Example 3: CLI Tool

```python
# cli_tool.py

import argparse
from core.agent_factory import AgentFactory
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Claude-Agents CLI')
    parser.add_argument('--project-type', required=True,
                       help='Type of project (sql_database_analysis, financial_analysis, etc.)')
    parser.add_argument('--project-name', required=True,
                       help='Name of your project')
    parser.add_argument('--output-dir', default='.',
                       help='Where to create agents')

    args = parser.parse_args()

    factory = AgentFactory(framework_dir="Claude-Agents")

    print(f"Creating agents for {args.project_name}...")

    agents = factory.auto_create_agents_for_project(
        project_type=args.project_type,
        project_name=args.project_name,
        output_dir=Path(args.output_dir)
    )

    print(f"\n✓ Success! Created {len(agents)} agents:")
    for agent in agents:
        print(f"  - {agent.name}")

if __name__ == '__main__':
    main()

# Usage:
# python cli_tool.py --project-type sql_database_analysis --project-name my-project
```

---

## 🔄 Workflow Integration

### Your Complete Workflow:

```
1. Start New Project
   ↓
2. Auto-Create Agents (AgentFactory)
   ↓
3. Load Data (your code)
   ↓
4. Generate Analysis Prompts (AgentManager + PromptEngine)
   ↓
5. Send to Claude API (your code)
   ↓
6. Receive Insights (Claude's response)
   ↓
7. Generate Reports (your code)
```

### Code Example:

```python
from pathlib import Path
from core.agent_factory import AgentFactory
from core.agent_manager import AgentManager
from core.prompt_engine import PromptEngine
import pandas as pd
import anthropic

def complete_workflow(data_file: str, project_name: str):
    """Complete analysis workflow with agents"""

    # Step 1: Create project agents
    factory = AgentFactory()
    agents = factory.auto_create_agents_for_project(
        project_type="sql_database_analysis",
        project_name=project_name,
        output_dir=Path(f"projects/{project_name}/agents")
    )

    # Step 2: Load data
    df = pd.read_csv(data_file)
    print(f"✓ Loaded {len(df)} rows")

    # Step 3: Generate prompts
    manager = AgentManager(agents_dir=f"projects/{project_name}/agents")
    engine = PromptEngine()

    agent_names = manager.list_agents()
    prompts = {}

    for agent_name in agent_names:
        agent = manager.load_agent(agent_name)
        task = f"Analyze dataset with {len(df)} rows: {', '.join(df.columns[:5])}"

        prompt = engine.generate_prompt(
            context=agent.context,
            model=agent.model,
            tools=agent.tools,
            task=task
        )

        prompts[agent_name] = prompt

    # Step 4: Send to Claude
    claude = anthropic.Anthropic(api_key="your-key")
    results = {}

    for agent_name, prompt in prompts.items():
        print(f"Analyzing with {agent_name}...")

        message = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=5000,
            messages=[{"role": "user", "content": prompt}]
        )

        results[agent_name] = message.content[0].text

    # Step 5: Save results
    output_dir = Path(f"projects/{project_name}/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    for agent_name, result in results.items():
        with open(output_dir / f"{agent_name}_report.md", 'w') as f:
            f.write(result)

    print(f"\n✅ Analysis complete! Results in {output_dir}")
    return results

# Run it
complete_workflow("data/sales.csv", "sales-analysis-2024")
```

---

## 📦 Available Templates

List all available templates:

```python
factory = AgentFactory()
templates = factory.list_available_templates()

print("Available Templates:")
for template in templates:
    print(f"  - {template}")

# Output:
# Available Templates:
#   - base_agent
#   - business_analyst
#   - data_scientist
#   - therapist_assistant
```

---

## ✅ Summary

**Your framework is now a fully reusable package that:**

1. ✅ **Integrates into any project** - Just import and use
2. ✅ **Auto-creates agents** - Based on project type
3. ✅ **Customizes dynamically** - Agents adapt to your needs
4. ✅ **Scales effortlessly** - Add agents as projects grow
5. ✅ **Works everywhere** - Web apps, CLI tools, notebooks, APIs

**Key Files Created:**
- [setup.py](Claude-Agents/setup.py) - Package installation
- [__init__.py](Claude-Agents/__init__.py) - Package interface
- [core/agent-factory.py](Claude-Agents/core/agent-factory.py) - Dynamic agent creation

**Ready to integrate into your SQL database project!** 🚀

