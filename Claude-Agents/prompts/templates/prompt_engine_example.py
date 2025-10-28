#!/usr/bin/env python3
"""
Claude-Agents Prompt Engine Example
Demonstrates how to use the template system
"""

import os
import yaml
from string import Template


class PromptEngine:
    def __init__(self, templates_dir="prompts/templates"):
        self.templates_dir = templates_dir
        self.loaded_templates = {}

    def load_template(self, template_name):
        """Load a template file and return as Template object"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.txt")

        if template_name in self.loaded_templates:
            return self.loaded_templates[template_name]

        try:
            with open(template_path, "r") as f:
                content = f.read()
                template = Template(content)
                self.loaded_templates[template_name] = template
                return template
        except FileNotFoundError:
            print(f"Template {template_name} not found at {template_path}")
            return None

    def generate_agent_prompt(self, agent_type, task_context):
        """Generate a complete agent prompt using templates"""

        # Load the specific agent template
        agent_template = self.load_template(agent_type)
        if not agent_template:
            # Fallback to base template
            agent_template = self.load_template("base_agent_template")

        if not agent_template:
            return "Error: No templates available"

        # Fill in the template with context
        try:
            return agent_template.substitute(**task_context)
        except KeyError as e:
            return f"Error: Missing template variable {e}"


# Example Usage
def main():
    """Example of how to use the prompt engine"""

    engine = PromptEngine()

    # Example 1: Business Analyst Task
    business_context = {
        "task": "Analyze Q3 financial performance and identify growth opportunities",
        "agent_role": "Senior Business Financial Analyst",
        "agent_expertise": "Financial Modeling, KPI Analysis, Forecasting",
        "current_task": "Q3 Financial Analysis",
        "user_background": "Business Owner with 5+ years experience",
        "available_tools": "Excel, Financial databases, Industry reports",
        "constraints": "Confidential data, 2-week deadline",
        "max_tokens": "5000",
        "temperature": "0.1",
        "response_format": "Executive summary with detailed analysis",
        "methodology_steps": """
        1. Review Q3 financial statements and KPIs
        2. Compare against Q2 and previous year Q3
        3. Analyze industry benchmarks
        4. Identify growth drivers and obstacles
        5. Develop actionable recommendations
        """,
        "output_format": "Executive summary with supporting analysis",
        "skills_list": "xlsx, financial-modeling, reporting",
        "slash_commands": "/financial, /kpi, /forecast, /report",
        "mcp_servers": "financial-data-api, reporting-engine",
        "external_apis": "quickbooks, stripe, industry-databases",
    }

    # Generate the prompt
    business_prompt = engine.generate_agent_prompt(
        "business_analyst_template", business_context
    )

    print("=== GENERATED BUSINESS ANALYST PROMPT ===")
    print(business_prompt)
    print("\n" + "=" * 50 + "\n")

    # Example 2: Data Scientist Task
    data_context = {
        "task": "Analyze customer churn patterns in subscription data",
        "agent_role": "Senior Data Scientist",
        "agent_expertise": "Statistical Analysis, Machine Learning, Customer Analytics",
        "current_task": "Customer Churn Analysis",
        "user_background": "Business Owner seeking data-driven insights",
        "available_tools": "Python, pandas, scikit-learn, customer database",
        "constraints": "Customer privacy, interpretable results required",
        "max_tokens": "6000",
        "temperature": "0.2",
        "response_format": "Analysis report with code examples",
        "methodology_steps": """
        1. Explore customer data and churn definitions
        2. Identify key features and patterns
        3. Build predictive models for churn risk
        4. Analyze feature importance and drivers
        5. Recommend retention strategies
        """,
        "output_format": "Structured analysis with code and visualizations",
        "skills_list": "statistical-analysis, ml-algorithms, data-visualization",
        "slash_commands": "/analyze, /visualize, /model, /stats",
        "mcp_servers": "database-connector, analytics-api",
        "external_apis": "pandas, scikit-learn, matplotlib",
    }

    data_prompt = engine.generate_agent_prompt("data_scientist_template", data_context)

    print("=== GENERATED DATA SCIENTIST PROMPT ===")
    print(data_prompt)


if __name__ == "__main__":
    main()


# Agent Configuration Example
def create_agent_config():
    """Example of agent configuration file"""

    config = {
        "agent_name": "business-analyst-v1",
        "version": "1.0",
        "context": {
            "role": "Senior Business Financial Analyst",
            "expertise": [
                "financial_modeling",
                "kpi_analysis",
                "forecasting",
                "strategic_planning",
            ],
            "scope": "Business performance analysis and strategic insights",
            "constraints": [
                "confidential_data",
                "regulatory_compliance",
                "accuracy_required",
            ],
        },
        "model": {
            "name": "claude-sonnet-4-20250514",
            "max_tokens": 5000,
            "temperature": 0.1,
            "response_format": "structured",
        },
        "tools": {
            "skills": ["xlsx", "financial-modeling", "reporting"],
            "slash_commands": ["/financial", "/kpi", "/forecast", "/report"],
            "mcp_servers": [
                {
                    "name": "financial-data-api",
                    "required": True,
                    "config": "config/financial.json",
                }
            ],
        },
    }

    # Save configuration
    with open("agents/business-analyst/config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    return config
