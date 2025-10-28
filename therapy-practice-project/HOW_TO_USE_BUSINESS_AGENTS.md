# How to Use Business Intelligence Agents

## Overview

This guide shows you exactly how to interact with your **4 business intelligence agents** and how to provide them with your practice data for analysis.

---

## Your 4 Business Intelligence Agents

### 1. Business Analyst
**Role**: Practice financials, KPIs, and forecasting

**What it analyzes**:
- Revenue and profitability
- Client acquisition and retention
- Therapist utilization rates
- Service demand trends
- Insurance billing and reimbursement
- Practice growth opportunities

### 2. Marketing Analytics
**Role**: Content performance and ROI tracking

**What it analyzes**:
- Social media performance
- Content engagement metrics
- Client acquisition sources
- Marketing ROI calculation
- Conversion tracking (inquiries → bookings)
- Integrated business + content performance

### 3. Market Research
**Role**: Local market intelligence and competitive analysis

**What it analyzes**:
- Local mental health service demand
- Competitor analysis (other practices)
- Service gap identification
- Demographics and community needs
- Treatment modality trends (EMDR, DBT, CBT)
- Insurance network opportunities

### 4. Practice Operations
**Role**: Scheduling and efficiency optimization

**What it analyzes**:
- Therapist scheduling efficiency
- Appointment capacity planning
- Waitlist management
- Service delivery efficiency
- Client flow optimization
- Practice workflow improvement

---

## 📊 How to Provide Data to Business Agents

### Data Format Options

Your business agents can accept data in multiple formats:

1. **Python Dictionary** (easiest for scripts)
2. **JSON File** (good for automation)
3. **CSV Export** (from practice management software)
4. **Manual Input** (for quick analysis)

---

## 📁 Data Templates

### Template 1: Weekly Practice Data (Python Dictionary)

```python
weekly_practice_data = {
    # Financial Metrics
    'revenue': 8500,              # Total revenue this week
    'revenue_previous_week': 7850,
    'avg_session_rate': 150,      # Average per session
    'outstanding_billing': 2400,   # Unpaid invoices

    # Client Metrics
    'new_clients': 3,              # New clients this week
    'total_active_clients': 42,    # Currently active
    'total_sessions': 45,          # Sessions completed
    'cancellations': 2,            # Last-minute cancellations
    'no_shows': 1,                 # No-shows
    'retention_rate': 0.92,        # 92% retention

    # Operational Metrics
    'therapist_utilization': 0.85, # 85% of available hours used
    'available_slots': 12,         # Open appointment slots
    'waitlist_size': 3,            # Clients waiting

    # Service Breakdown
    'service_breakdown': {
        'individual_therapy': 28,
        'couples_therapy': 8,
        'family_therapy': 4,
        'emdr': 5
    },

    # Referral Sources
    'referral_sources': {
        'social_media': 1,
        'psychology_today': 1,
        'word_of_mouth': 1,
        'insurance_directory': 0,
        'google_search': 0
    },

    # Week identifier
    'week_of': '2025-10-20'  # Monday of the week
}
```

### Template 2: Monthly Practice Data (JSON)

Save as `monthly_data.json`:

```json
{
  "month": "October 2025",
  "financial": {
    "total_revenue": 45000,
    "revenue_change_pct": 8.0,
    "avg_session_rate": 150,
    "outstanding_billing": 2500,
    "expenses": 12000,
    "profit": 33000
  },
  "clients": {
    "new_clients": 12,
    "total_active": 85,
    "retention_rate": 92.0,
    "cancellation_rate": 5.0,
    "churn_clients": 3
  },
  "operations": {
    "total_sessions": 180,
    "therapist_count": 3,
    "therapist_utilization": 0.87,
    "available_slots": 15,
    "waitlist_size": 3,
    "avg_wait_time_days": 12
  },
  "services": {
    "individual_therapy": {
      "sessions": 120,
      "revenue": 18000,
      "utilization": 0.90
    },
    "couples_therapy": {
      "sessions": 35,
      "revenue": 10500,
      "utilization": 0.65
    },
    "family_therapy": {
      "sessions": 18,
      "revenue": 5400,
      "utilization": 0.75
    },
    "emdr": {
      "sessions": 7,
      "revenue": 2100,
      "utilization": 0.85
    }
  },
  "marketing": {
    "social_media_reach": 15000,
    "social_media_engagement": 630,
    "website_visits": 1250,
    "inquiries": 18,
    "inquiry_to_booking_rate": 0.67
  }
}
```

### Template 3: CSV Export (From Practice Management Software)

**sessions.csv**:
```csv
date,therapist,client_id,service_type,duration_min,fee,paid,referral_source
2025-10-20,Dr. Smith,C001,individual,50,150,yes,social_media
2025-10-20,Dr. Jones,C042,couples,60,200,yes,word_of_mouth
2025-10-21,Dr. Smith,C013,individual,50,150,no,psychology_today
2025-10-21,Dr. Brown,C025,emdr,90,200,yes,insurance_directory
```

**clients.csv**:
```csv
client_id,start_date,status,service_type,sessions_completed,outstanding_balance
C001,2025-08-15,active,individual,8,0
C042,2025-09-01,active,couples,4,200
C013,2025-10-15,active,individual,2,150
C025,2025-07-20,active,emdr,6,0
```

---

## 🔄 How to Upload Data to Agents

### Method 1: Direct Script (Recommended)

**Create `analyze_practice_data.py`:**

```python
#!/usr/bin/env python3
"""Analyze practice data with Business Analyst agent"""

import sys
from pathlib import Path
import importlib.util
import anthropic
import os
import json

# Setup paths
FRAMEWORK_DIR = Path(__file__).parent.parent / "Claude-Agents"

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules
agent_manager_mod = load_module("agent_manager", FRAMEWORK_DIR / "core" / "agent-manager.py")
prompt_engine_mod = load_module("prompt_engine", FRAMEWORK_DIR / "core" / "prompt-engine.py")

AgentManager = agent_manager_mod.AgentManager
PromptEngine = prompt_engine_mod.PromptEngine

def analyze_practice_data(data_file=None, data_dict=None):
    """
    Analyze practice data with Business Analyst agent.

    Args:
        data_file: Path to JSON file with practice data
        data_dict: Python dictionary with practice data
    """

    # Load data
    if data_file:
        with open(data_file, 'r') as f:
            practice_data = json.load(f)
    elif data_dict:
        practice_data = data_dict
    else:
        print("❌ Error: Provide either data_file or data_dict")
        return None

    # Initialize
    agents_dir = Path(__file__).parent / "agents"
    manager = AgentManager(agents_dir=str(agents_dir))
    engine = PromptEngine()

    # Load business analyst
    print("Loading Business Analyst agent...")
    analyst = manager.load_agent("therapy-practice-business-analyst")

    if not analyst:
        print("❌ Error: Could not load business analyst")
        return None

    print(f"✓ Loaded: {analyst.context['role']}\n")

    # Create analysis task
    analysis_task = f"""
Analyze this week's/month's practice performance data:

{json.dumps(practice_data, indent=2)}

Provide comprehensive analysis including:

1. **Financial Summary**:
   - Revenue trends and changes
   - Profitability analysis
   - Outstanding billing concerns
   - Revenue per therapist/service

2. **Client Metrics**:
   - New client acquisition
   - Retention rate analysis
   - Cancellation/no-show patterns
   - Client lifetime value estimation

3. **Operational Efficiency**:
   - Therapist utilization analysis
   - Schedule optimization opportunities
   - Waitlist management recommendations
   - Capacity planning

4. **Service Demand Analysis**:
   - Which services are in highest demand
   - Which services are underutilized
   - Service mix optimization
   - Pricing considerations

5. **Growth Opportunities**:
   - Where to focus marketing efforts
   - Which services to expand
   - Therapist hiring needs
   - New service opportunities

6. **Content Marketing Opportunities**:
   - Which topics should we create content about
   - Which services need more awareness
   - Target audience priorities

7. **Key Recommendations**:
   - Top 3 immediate actions
   - 30-day priorities
   - 90-day strategic goals

**Format**: Executive summary + detailed analysis with specific numbers and actionable recommendations.
"""

    # Generate prompt
    print("Generating analysis prompt...")
    prompt = engine.generate_prompt(
        context=analyst.context,
        model=analyst.model,
        tools=analyst.tools,
        task=analysis_task
    )

    print(f"✓ Generated prompt ({len(prompt):,} characters)\n")

    # Call Claude API
    print("Analyzing practice data with Claude API...")
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        temperature=0.1,  # Business analyst uses 0.1 for precision
        messages=[{"role": "user", "content": prompt}]
    )

    analysis = response.content[0].text

    # Display results
    print("\n" + "="*70)
    print("BUSINESS INTELLIGENCE ANALYSIS")
    print("="*70 + "\n")
    print(analysis)
    print("\n" + "="*70)

    # Save to file
    output_file = f"business_analysis_{practice_data.get('week_of', practice_data.get('month', 'report'))}.md"
    with open(output_file, 'w') as f:
        f.write(f"# Business Intelligence Analysis\n\n")
        f.write(f"**Generated**: {pd.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(analysis)

    print(f"\n✓ Analysis saved to: {output_file}\n")

    return analysis


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Analyze practice data')
    parser.add_argument('--file', help='Path to JSON data file')
    parser.add_argument('--sample', action='store_true', help='Use sample data')

    args = parser.parse_args()

    if args.sample:
        # Use sample data
        sample_data = {
            'week_of': '2025-10-20',
            'revenue': 8500,
            'revenue_previous_week': 7850,
            'new_clients': 3,
            'total_sessions': 45,
            'therapist_utilization': 0.85,
            'service_breakdown': {
                'individual_therapy': 28,
                'couples_therapy': 8,
                'family_therapy': 4,
                'emdr': 5
            },
            'referral_sources': {
                'social_media': 1,
                'psychology_today': 1,
                'word_of_mouth': 1
            }
        }
        analyze_practice_data(data_dict=sample_data)

    elif args.file:
        analyze_practice_data(data_file=args.file)

    else:
        print("Usage:")
        print("  python analyze_practice_data.py --sample")
        print("  python analyze_practice_data.py --file monthly_data.json")
```

**Run it:**
```bash
# With sample data
python analyze_practice_data.py --sample

# With your JSON file
python analyze_practice_data.py --file monthly_data.json
```

---

### Method 2: Export from Practice Management Software

**Step 1: Export Data**

Most practice management software (SimplePractice, TherapyNotes, etc.) can export:
- Session reports (CSV)
- Client reports (CSV)
- Financial reports (CSV/Excel)

**Step 2: Convert to JSON**

```python
import pandas as pd
import json

# Read CSV exports
sessions = pd.read_csv('sessions.csv')
clients = pd.read_csv('clients.csv')

# Calculate metrics
practice_data = {
    'month': 'October 2025',
    'financial': {
        'total_revenue': sessions['fee'].sum(),
        'avg_session_rate': sessions['fee'].mean(),
        'outstanding_billing': sessions[sessions['paid'] == 'no']['fee'].sum()
    },
    'clients': {
        'new_clients': len(clients[clients['start_date'] >= '2025-10-01']),
        'total_active': len(clients[clients['status'] == 'active']),
        'total_sessions': len(sessions)
    },
    'services': sessions.groupby('service_type')['fee'].agg(['count', 'sum']).to_dict()
}

# Save as JSON
with open('practice_data.json', 'w') as f:
    json.dump(practice_data, f, indent=2)

print("✓ Data converted to practice_data.json")
```

**Step 3: Analyze**
```bash
python analyze_practice_data.py --file practice_data.json
```

---

### Method 3: Manual Data Entry (Quick Analysis)

**For quick weekly check-ins:**

```python
# Quick manual data entry
quick_data = {
    'week_of': '2025-10-27',
    'revenue': int(input("This week's revenue: $")),
    'new_clients': int(input("New clients this week: ")),
    'total_sessions': int(input("Total sessions: ")),
    'cancellations': int(input("Cancellations: ")),
    'therapist_utilization': float(input("Utilization (0.0-1.0): "))
}

# Analyze
analyze_practice_data(data_dict=quick_data)
```

---

## 📊 Using Marketing Analytics Agent

**Track content → business outcomes:**

```python
def analyze_marketing_roi(business_data, content_data):
    """Analyze how content impacts business results"""

    # Load marketing analytics agent
    analyst = manager.load_agent("therapy-practice-marketing-analytics")

    # Combine data
    integrated_data = {
        'business_metrics': business_data,
        'content_metrics': content_data,
        'week_of': business_data.get('week_of')
    }

    task = f"""
Analyze integrated business + content performance:

{json.dumps(integrated_data, indent=2)}

Provide:
1. **Content Attribution**: Which content drove inquiries/bookings
2. **ROI Calculation**: Content investment vs. revenue generated
3. **Conversion Analysis**: Inquiry → booking rate by source
4. **Performance by Platform**: Instagram vs. Facebook vs. blog
5. **Best Performing Content**: What topics/formats worked best
6. **Recommendations**: What to double down on, what to improve

Output: Executive summary + detailed metrics + actionable insights
"""

    # Generate and analyze
    prompt = engine.generate_prompt(
        context=analyst.context,
        model=analyst.model,
        tools=analyst.tools,
        task=task
    )

    # Call API and return results
    # [Same API call pattern as above]
```

**Usage:**
```python
business_data = {
    'new_clients': 4,
    'referral_sources': {
        'social_media': 2,
        'blog': 1,
        'other': 1
    }
}

content_data = {
    'blog_posts_published': 1,
    'social_posts': 5,
    'total_reach': 1200,
    'engagement': 85,
    'website_visits_from_content': 245
}

analyze_marketing_roi(business_data, content_data)
```

---

## 🔍 Using Market Research Agent

**Research local demand and competitors:**

```python
def research_local_market(location, services):
    """Research local market opportunities"""

    # Load market research agent
    researcher = manager.load_agent("therapy-practice-market-research")

    task = f"""
Conduct market research for therapy practice:

**Location**: {location}
**Current Services**: {', '.join(services)}

Research and provide:

1. **Local Demand Analysis**:
   - Mental health service demand in {location}
   - Population demographics
   - Insurance coverage patterns
   - Underserved populations

2. **Competitor Analysis**:
   - Number of therapy practices in area
   - Services they offer
   - Pricing comparison
   - Online presence strength
   - What they're doing well
   - Gaps we can fill

3. **Service Opportunities**:
   - Which therapy types are in high demand
   - Which are underserved
   - Treatment modalities trending (EMDR, DBT, etc.)
   - Specialized populations needing services

4. **Marketing Recommendations**:
   - Where to focus marketing efforts
   - Content topics that would attract local clients
   - Local SEO opportunities
   - Partnership opportunities (gyms, schools, etc.)

5. **Growth Strategy**:
   - Should we add therapists? Which specialties?
   - New services to consider
   - Geographic expansion opportunities
   - Insurance networks to join

**Output**: Comprehensive market analysis with specific recommendations
"""

    # [Same pattern - generate prompt, call API, return results]
```

**Usage:**
```bash
python research_market.py \
  --location "Austin, Texas" \
  --services "anxiety,couples,emdr,individual"
```

---

## ⚙️ Using Practice Operations Agent

**Optimize scheduling and efficiency:**

```python
def optimize_operations(scheduling_data):
    """Analyze and optimize practice operations"""

    # Load operations agent
    ops = manager.load_agent("therapy-practice-practice-operations")

    task = f"""
Analyze practice operations and scheduling:

**Current State**:
{json.dumps(scheduling_data, indent=2)}

Analyze and provide:

1. **Utilization Analysis**:
   - Current utilization by therapist
   - Comparison to industry benchmarks (target: 75-85%)
   - Peak vs. slow times
   - Revenue per hour analysis

2. **Schedule Optimization**:
   - Which time slots consistently empty
   - Which are overbooked/waitlisted
   - Optimal schedule recommendations
   - How to fill gaps

3. **Capacity Planning**:
   - Current capacity (hours available)
   - Used vs. available
   - Waitlist analysis
   - When to add therapist hours

4. **Efficiency Improvements**:
   - Reduce cancellations/no-shows
   - Optimize session lengths
   - Back-to-back scheduling
   - Admin time reduction

5. **Client Flow**:
   - Intake process efficiency
   - Session frequency optimization
   - Discharge planning
   - Retention strategies

6. **Recommendations**:
   - Immediate actions (next week)
   - Short-term improvements (next month)
   - Long-term strategy (next quarter)

**Output**: Operations analysis with specific, actionable recommendations
"""

    # [Same pattern]
```

**Usage:**
```python
scheduling_data = {
    'therapists': [
        {
            'name': 'Dr. Smith',
            'hours_available': 40,
            'hours_scheduled': 36,
            'utilization': 0.90,
            'specialty': 'anxiety'
        },
        {
            'name': 'Dr. Jones',
            'hours_available': 30,
            'hours_scheduled': 18,
            'utilization': 0.60,
            'specialty': 'couples'
        }
    ],
    'empty_slots': [
        'Tuesday 2pm',
        'Thursday 10am',
        'Friday 3pm'
    ],
    'waitlist': 3
}

optimize_operations(scheduling_data)
```

---

## 🔄 Complete Weekly Workflow

### Monday Morning: Business Intelligence

```python
# 1. Export last week's data from practice software
# 2. Convert to JSON
# 3. Analyze

import subprocess

# Analyze business data
subprocess.run([
    "python", "analyze_practice_data.py",
    "--file", "weekly_data.json"
])

# Analysis saved to: business_analysis_2025-10-20.md
```

### Monday Afternoon: Content Strategy

```python
# Use business insights to plan content

# Read business analysis
with open('business_analysis_2025-10-20.md', 'r') as f:
    business_insights = f.read()

# Plan content based on insights
# [Content strategist workflow - see social media guide]
```

### Sunday Evening: Performance Review

```python
# Combine business + content data for ROI analysis

business_data = {...}  # Week's business metrics
content_data = {...}   # Week's content performance

analyze_marketing_roi(business_data, content_data)

# Get recommendations for next week
```

---

## 📋 Data Collection Checklist

### Weekly Data to Collect:
- [ ] Total revenue
- [ ] Number of sessions
- [ ] New clients
- [ ] Cancellations/no-shows
- [ ] Referral sources for new clients
- [ ] Therapist utilization rates
- [ ] Service breakdown (individual, couples, etc.)

### Monthly Data to Collect:
- [ ] All weekly metrics (summarized)
- [ ] Total active clients
- [ ] Retention rate
- [ ] Outstanding billing
- [ ] Expenses
- [ ] Profit margin
- [ ] Content performance (reach, engagement)
- [ ] Website traffic
- [ ] Inquiry → booking conversion rate

### Quarterly Data to Collect:
- [ ] All monthly metrics (trends)
- [ ] Client lifetime value
- [ ] Market share (local)
- [ ] Competitor analysis
- [ ] Service mix evolution
- [ ] Marketing ROI
- [ ] Strategic progress

---

## ❓ Troubleshooting

### Problem: "Don't know how to export data from my practice software"

**Solution:**

Most practice management systems have export functions:

**SimplePractice**:
1. Reports → Custom Reports
2. Select date range
3. Export as CSV

**TherapyNotes**:
1. Reports → Session Reports
2. Choose filters
3. Export to Excel/CSV

**If no export available**: Manually enter key metrics into JSON template

### Problem: "My data doesn't match the template"

**Solution:**

The templates are flexible. Provide what you have:

```python
# Minimal data that still works
minimal_data = {
    'week_of': '2025-10-27',
    'revenue': 8500,
    'new_clients': 3,
    'total_sessions': 45
}

# Agent will analyze what's provided and note what's missing
```

### Problem: "Analysis is too generic"

**Solution:**

Provide more specific context:

```python
task = f"""
Analyze practice data with specific focus on:
- Why is couples therapy utilization only 60%?
- Should we hire another therapist for anxiety (waitlist growing)?
- Is our pricing competitive in Austin market?

Data: {json.dumps(practice_data, indent=2)}

Provide specific, actionable recommendations for these questions.
"""
```

---

## 🎯 Best Practices

### DO:
- ✅ Collect data weekly for trend analysis
- ✅ Track referral sources for new clients
- ✅ Monitor therapist utilization rates
- ✅ Compare month-over-month changes
- ✅ Use insights to inform content strategy
- ✅ Save all analysis reports for historical reference

### DON'T:
- ❌ Only analyze when things go wrong
- ❌ Ignore trends in the data
- ❌ Forget to track content → business impact
- ❌ Make decisions without data
- ❌ Collect data but never analyze it

---

## 📞 Support

**Documentation:**
- [analyze_practice_data.py](./analyze_practice_data.py) - Analysis script
- [therapy_practice_dashboard.py](../Claude-Agents/therapy_practice_dashboard.py) - Dashboard
- [therapy_practice_workflow.py](../Claude-Agents/therapy_practice_workflow.py) - Complete workflow

**Agent Configurations:**
- [business-analyst/config.yaml](./agents/therapy-practice-business-analyst/config.yaml)
- [marketing-analytics/config.yaml](./agents/therapy-practice-marketing-analytics/config.yaml)
- [market-research/config.yaml](./agents/therapy-practice-market-research/config.yaml)
- [practice-operations/config.yaml](./agents/therapy-practice-practice-operations/config.yaml)

---

## 🎉 You're Ready!

You now know how to:
- ✅ Format and upload practice data
- ✅ Request business intelligence analysis
- ✅ Track marketing ROI
- ✅ Research local market opportunities
- ✅ Optimize practice operations
- ✅ Integrate business insights with content strategy

**Start analyzing your practice data today!**

```bash
python analyze_practice_data.py --sample
```
