# SQL Database + Spreadsheet Analysis Project
## Using Claude-Agents Framework

**Project Goal**: Upload spreadsheets to SQL database and have agents analyze, report, and provide insights.

---

## Project Setup

### 1. Database Setup (SQLite Example)

```python
import sqlite3
import pandas as pd
from pathlib import Path

class SpreadsheetDatabase:
    """Manage spreadsheet data in SQL database"""

    def __init__(self, db_path="data/analysis.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)

    def upload_spreadsheet(self, excel_file, table_name=None):
        """Upload Excel/CSV to database"""

        # Read spreadsheet
        if excel_file.endswith('.csv'):
            df = pd.read_csv(excel_file)
        else:
            df = pd.read_excel(excel_file)

        # Auto-generate table name if not provided
        if table_name is None:
            table_name = Path(excel_file).stem.lower().replace(' ', '_')

        # Upload to database
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

        print(f"✓ Uploaded {len(df)} rows to table '{table_name}'")
        return table_name

    def get_table_info(self, table_name):
        """Get information about a table"""
        query = f"SELECT * FROM {table_name} LIMIT 5"
        df = pd.read_sql_query(query, self.conn)

        return {
            'name': table_name,
            'columns': list(df.columns),
            'sample_data': df,
            'row_count': pd.read_sql_query(
                f"SELECT COUNT(*) as count FROM {table_name}",
                self.conn
            )['count'][0]
        }

    def list_tables(self):
        """List all tables in database"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = pd.read_sql_query(query, self.conn)
        return tables['name'].tolist()

    def query(self, sql):
        """Execute SQL query and return DataFrame"""
        return pd.read_sql_query(sql, self.conn)

    def close(self):
        """Close database connection"""
        self.conn.close()
```

---

## 2. Agent Integration

### Load Agents

```python
import sys
sys.path.insert(0, 'Claude-Agents/core')

from pathlib import Path
import importlib.util

# Load agent manager module
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

core_dir = Path('Claude-Agents/core')
agent_manager_mod = load_module("agent_manager", core_dir / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", core_dir / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine

# Initialize managers
agent_manager = AgentManager(agents_dir="Claude-Agents/agents")
prompt_engine = PromptEngine(prompts_dir="Claude-Agents/prompts")
```

---

## 3. Analysis Pipeline

### Complete Analysis Workflow

```python
class DataAnalysisPipeline:
    """Orchestrate multi-agent analysis pipeline"""

    def __init__(self, db_path="data/analysis.db"):
        self.db = SpreadsheetDatabase(db_path)
        self.agent_manager = AgentManager(agents_dir="Claude-Agents/agents")
        self.prompt_engine = PromptEngine(prompts_dir="Claude-Agents/prompts")
        self.results = {}

    def upload_data(self, file_path, table_name=None):
        """Step 1: Upload spreadsheet to database"""
        print(f"\n{'='*60}")
        print("STEP 1: Uploading Data to Database")
        print(f"{'='*60}")

        table = self.db.upload_spreadsheet(file_path, table_name)
        info = self.db.get_table_info(table)

        print(f"\nTable Info:")
        print(f"  Name: {info['name']}")
        print(f"  Rows: {info['row_count']}")
        print(f"  Columns: {len(info['columns'])}")
        print(f"  Column Names: {', '.join(info['columns'])}")

        return table, info

    def analyze_with_business_analyst(self, table_name, analysis_type="financial"):
        """Step 2: Business Analyst reviews data"""
        print(f"\n{'='*60}")
        print("STEP 2: Business Finance Analyst Analysis")
        print(f"{'='*60}")

        # Load business analyst agent
        agent = self.agent_manager.load_agent("business-analyst")

        # Get data from database
        df = self.db.query(f"SELECT * FROM {table_name}")

        # Create analysis task based on data
        task = self._generate_business_task(df, table_name, analysis_type)

        # Generate prompt
        prompt = self.prompt_engine.generate_prompt(
            context=agent.context,
            model=agent.model,
            tools=agent.tools,
            task=task,
            template_name="business_analyst_template"
        )

        print(f"\n✓ Generated analysis prompt for Business Analyst")
        print(f"  Task: {task[:100]}...")
        print(f"  Prompt length: {len(prompt)} characters")

        # Store for Claude API call
        self.results['business_analyst'] = {
            'agent': agent,
            'prompt': prompt,
            'task': task,
            'data': df
        }

        return prompt

    def analyze_with_data_scientist(self, table_name, analysis_type="statistical"):
        """Step 3: Data Scientist reviews data"""
        print(f"\n{'='*60}")
        print("STEP 3: Data Scientist Analysis")
        print(f"{'='*60}")

        # Load data scientist agent
        agent = self.agent_manager.load_agent("data-scientist")

        # Get data
        df = self.db.query(f"SELECT * FROM {table_name}")

        # Create analysis task
        task = self._generate_data_science_task(df, table_name, analysis_type)

        # Generate prompt
        prompt = self.prompt_engine.generate_prompt(
            context={'role': 'Senior Data Scientist', 'expertise': 'Statistical analysis, ML, visualization', 'scope': 'Data analysis', 'constraints': 'Reproducible, privacy-compliant'},
            model={'name': 'claude-sonnet-4-20250514', 'max_tokens': 6000, 'temperature': 0.2, 'response_format': 'structured'},
            tools={'skills': ['statistical-analysis', 'ml-algorithms', 'data-visualization'], 'slash_commands': ['/analyze', '/visualize', '/model'], 'mcp_servers': ['postgresql', 'sqlite']},
            task=task,
            template_name="data_scientist_template"
        )

        print(f"\n✓ Generated analysis prompt for Data Scientist")
        print(f"  Task: {task[:100]}...")
        print(f"  Prompt length: {len(prompt)} characters")

        self.results['data_scientist'] = {
            'agent': 'data-scientist',
            'prompt': prompt,
            'task': task,
            'data': df
        }

        return prompt

    def _generate_business_task(self, df, table_name, analysis_type):
        """Generate business analysis task based on data"""

        # Analyze data structure
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

        if analysis_type == "financial":
            task = f"""Analyze the financial data in table '{table_name}' with {len(df)} records.

The dataset contains:
- {len(df.columns)} columns: {', '.join(df.columns.tolist())}
- {len(numeric_cols)} numeric columns: {', '.join(numeric_cols)}
- Date range: {df[date_cols[0]].min() if date_cols else 'No date column'} to {df[date_cols[0]].max() if date_cols else 'N/A'}

Please perform:
1. Financial summary analysis (totals, averages, trends)
2. Period-over-period comparison (if time-based data)
3. Key performance indicators calculation
4. Variance analysis (if budget/actual data present)
5. Financial insights and recommendations

Generate:
- Executive summary with 3-5 key insights
- Detailed financial metrics table
- Trend visualizations (if applicable)
- Excel report with professional formatting
"""
        elif analysis_type == "kpi":
            task = f"""Generate a comprehensive KPI dashboard for table '{table_name}'.

Calculate relevant KPIs based on the data:
{', '.join(numeric_cols[:5])}

Include:
- Key financial/operational metrics
- Period comparisons (MoM, QoQ, YoY if applicable)
- Target vs actual (if benchmarks provided)
- Trend indicators
- Alert flags for concerning metrics
"""
        else:
            task = f"""Perform comprehensive business analysis on table '{table_name}' with {len(df)} records.

Analyze patterns, trends, and provide actionable insights."""

        return task

    def _generate_data_science_task(self, df, table_name, analysis_type):
        """Generate data science task based on data"""

        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        if analysis_type == "statistical":
            task = f"""Perform statistical analysis on table '{table_name}' with {len(df)} records.

Dataset characteristics:
- Numeric variables: {', '.join(numeric_cols[:5])}
- Categorical variables: {', '.join(categorical_cols[:3])}

Analysis required:
1. Exploratory Data Analysis (EDA)
   - Descriptive statistics
   - Distribution analysis
   - Outlier detection

2. Statistical Testing
   - Hypothesis tests (as appropriate)
   - Correlation analysis
   - Effect size calculations

3. Visualizations
   - Distribution plots
   - Correlation heatmap
   - Box plots for outliers

4. Insights
   - Key patterns identified
   - Statistical significance findings
   - Recommendations for further analysis

Provide reproducible Python code and clear interpretation of results."""

        elif analysis_type == "predictive":
            task = f"""Build predictive model for table '{table_name}'.

Create a machine learning model to predict [target variable].

Include:
1. Feature engineering
2. Model selection and training
3. Cross-validation
4. Performance metrics
5. Feature importance analysis
6. Recommendations"""

        else:
            task = f"""Analyze table '{table_name}' with {len(df)} records.

Perform comprehensive data science analysis including EDA, statistical tests, and visualizations."""

        return task

    def generate_report(self, output_dir="reports"):
        """Step 4: Generate comprehensive report"""
        print(f"\n{'='*60}")
        print("STEP 4: Generating Comprehensive Report")
        print(f"{'='*60}")

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Summary report
        report_path = Path(output_dir) / "analysis_summary.md"

        with open(report_path, 'w') as f:
            f.write("# Data Analysis Report\n\n")
            f.write(f"Generated: {pd.Timestamp.now()}\n\n")

            f.write("## Analyses Performed\n\n")

            for agent_name, result in self.results.items():
                f.write(f"### {agent_name.replace('_', ' ').title()}\n\n")
                f.write(f"**Task**: {result['task'][:200]}...\n\n")
                f.write(f"**Prompt Length**: {len(result['prompt'])} characters\n\n")
                f.write(f"**Data Shape**: {result['data'].shape}\n\n")
                f.write("---\n\n")

        print(f"✓ Report saved to: {report_path}")
        return report_path

    def close(self):
        """Clean up resources"""
        self.db.close()
```

---

## 4. Example Usage

### Complete Workflow Example

```python
def main():
    """Run complete analysis pipeline"""

    # Initialize pipeline
    pipeline = DataAnalysisPipeline(db_path="data/my_analysis.db")

    # Step 1: Upload your spreadsheet
    print("="*60)
    print("SPREADSHEET TO SQL DATABASE ANALYSIS PIPELINE")
    print("="*60)

    file_path = "data/financial_data_2024.xlsx"  # Your spreadsheet
    table_name, info = pipeline.upload_data(file_path, table_name="financials_2024")

    # Step 2: Business Analyst reviews
    business_prompt = pipeline.analyze_with_business_analyst(
        table_name="financials_2024",
        analysis_type="financial"
    )

    # Step 3: Data Scientist reviews
    data_science_prompt = pipeline.analyze_with_data_scientist(
        table_name="financials_2024",
        analysis_type="statistical"
    )

    # Step 4: Generate report
    report_path = pipeline.generate_report(output_dir="reports")

    # Display summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\n✓ Data uploaded to database")
    print(f"✓ Business Analyst prompt generated ({len(business_prompt)} chars)")
    print(f"✓ Data Scientist prompt generated ({len(data_science_prompt)} chars)")
    print(f"✓ Report saved to: {report_path}")

    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print(f"{'='*60}")
    print("1. Send prompts to Claude API for analysis")
    print("2. Receive and process agent responses")
    print("3. Generate Excel reports and visualizations")
    print("4. Review insights and recommendations")

    # Clean up
    pipeline.close()

    return pipeline

if __name__ == "__main__":
    pipeline = main()
```

---

## 5. Connecting to Claude API

### Send Prompts to Claude

```python
import anthropic

def analyze_with_claude(prompt, agent_name="business-analyst"):
    """Send prompt to Claude and get response"""

    client = anthropic.Anthropic(api_key="your-api-key")

    print(f"\nSending to Claude ({agent_name})...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        temperature=0.1,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = message.content[0].text

    print(f"✓ Received response ({len(response)} characters)")

    return response

# Use it in pipeline
def run_full_analysis_with_claude(file_path):
    """Complete analysis with Claude API calls"""

    pipeline = DataAnalysisPipeline()

    # Upload data
    table, info = pipeline.upload_data(file_path)

    # Business Analyst
    biz_prompt = pipeline.analyze_with_business_analyst(table)
    biz_response = analyze_with_claude(biz_prompt, "business-analyst")

    # Save business analyst response
    with open("reports/business_analyst_findings.md", "w") as f:
        f.write(biz_response)

    # Data Scientist
    ds_prompt = pipeline.analyze_with_data_scientist(table)
    ds_response = analyze_with_claude(ds_prompt, "data-scientist")

    # Save data scientist response
    with open("reports/data_scientist_findings.md", "w") as f:
        f.write(ds_response)

    print("\n✅ COMPLETE ANALYSIS FINISHED!")
    print("   - Business Analyst findings: reports/business_analyst_findings.md")
    print("   - Data Scientist findings: reports/data_scientist_findings.md")

    pipeline.close()
```

---

## 6. Example Scenarios

### Scenario 1: Financial Data Analysis

```python
# Your financial spreadsheet
file = "monthly_financials_2024.xlsx"

# Columns: Date, Revenue, Expenses, Profit, Department, Category

pipeline = DataAnalysisPipeline()
table, info = pipeline.upload_data(file)

# Business analyst analyzes:
# - Revenue trends
# - Expense breakdown
# - Profit margins
# - Department performance
# - Budget variances

business_prompt = pipeline.analyze_with_business_analyst(table, "financial")

# Data scientist analyzes:
# - Statistical significance of trends
# - Correlation analysis
# - Outlier detection
# - Predictive modeling for next quarter

data_prompt = pipeline.analyze_with_data_scientist(table, "statistical")
```

### Scenario 2: Sales Data Analysis

```python
# Your sales spreadsheet
file = "sales_data_2024.csv"

# Columns: Date, Product, Quantity, Revenue, Region, Salesperson

pipeline = DataAnalysisPipeline()
table, info = pipeline.upload_data(file)

# Business analyst provides:
# - Sales KPIs (revenue per rep, conversion rates)
# - Regional performance comparison
# - Product mix analysis
# - Growth trends

# Data scientist provides:
# - Customer segmentation
# - Churn prediction
# - Sales forecasting model
# - Feature importance (what drives sales)
```

### Scenario 3: Customer Data Analysis

```python
# Your customer spreadsheet
file = "customer_data.xlsx"

# Columns: CustomerID, Age, Location, PurchaseHistory, Satisfaction, Churn

pipeline = DataAnalysisPipeline()
table, info = pipeline.upload_data(file)

# Business analyst provides:
# - Customer lifetime value
# - Retention metrics
# - Segment profitability

# Data scientist provides:
# - Churn prediction model
# - Customer clustering
# - Satisfaction drivers analysis
```

---

## 7. Advanced Features

### Multi-Table Analysis

```python
def analyze_multiple_tables():
    """Analyze relationships between multiple tables"""

    pipeline = DataAnalysisPipeline()

    # Upload multiple spreadsheets
    sales_table = pipeline.db.upload_spreadsheet("sales_2024.xlsx", "sales")
    costs_table = pipeline.db.upload_spreadsheet("costs_2024.xlsx", "costs")
    customers_table = pipeline.db.upload_spreadsheet("customers.xlsx", "customers")

    # Join data with SQL
    combined_df = pipeline.db.query("""
        SELECT
            s.*,
            co.cost_amount,
            cu.customer_segment
        FROM sales s
        LEFT JOIN costs co ON s.product_id = co.product_id
        LEFT JOIN customers cu ON s.customer_id = cu.customer_id
    """)

    # Upload combined data for analysis
    combined_df.to_sql("combined_analysis", pipeline.db.conn, if_exists='replace')

    # Analyze with agents
    business_prompt = pipeline.analyze_with_business_analyst("combined_analysis")
    data_prompt = pipeline.analyze_with_data_scientist("combined_analysis")

    return business_prompt, data_prompt
```

---

## 8. Output Examples

### What You'll Get:

**From Business Analyst**:
```markdown
# Financial Analysis Report - Q1 2024

## Executive Summary
1. Revenue increased 12.5% QoQ, driven by Enterprise segment growth
2. Operating expenses up 8.2%, primarily due to marketing investments
3. Net margin improved to 18.5% (+2.1pp) - exceeds target of 16%

## Key Metrics
- Total Revenue: $5.2M (+12.5% QoQ)
- Gross Margin: 42.3%
- EBITDA: $1.1M
- Cash Position: Strong at $4.8M

## Recommendations
1. Continue marketing investment given positive ROI
2. Investigate Enterprise sales process for scaling
3. Monitor operating expense growth vs revenue
```

**From Data Scientist**:
```markdown
# Statistical Analysis Report

## Data Quality Assessment
- Total records: 1,247
- Missing values: <1% (handled via imputation)
- Outliers: 12 detected, retained for analysis

## Key Findings
1. Revenue shows strong positive trend (p<0.001)
2. Correlation between marketing spend and revenue: r=0.78
3. Seasonal pattern detected (Q4 spike confirmed)

## Predictive Model
- Random Forest Regression
- Cross-validated R² = 0.89
- RMSE = $42,000
- Top features: Marketing spend, Previous quarter revenue, Customer count

[Visualization: Actual vs Predicted, Feature Importance Plot]

## Code (Reproducible)
\`\`\`python
# Load and analyze data
import pandas as pd
df = pd.read_sql("SELECT * FROM financials_2024", conn)
# ... [full analysis code]
\`\`\`
```

---

## Summary

**YES!** You can absolutely:
1. ✅ Upload spreadsheets to SQL database
2. ✅ Have Business Analyst agent review financial aspects
3. ✅ Have Data Scientist agent perform statistical analysis
4. ✅ Get comprehensive reports with findings
5. ✅ Receive actionable recommendations

**Your framework is ready for this exact use case!** 🎯
