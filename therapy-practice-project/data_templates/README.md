# Data Templates for Therapy Practice Agents

This directory contains example data templates for uploading your practice data to business intelligence agents.

---

## Available Templates

### 1. weekly_practice_data.json
**Use for**: Weekly business intelligence analysis (Monday reviews)

**Contains**:
- Financial metrics (revenue, billing)
- Client metrics (new clients, retention)
- Operations (sessions, utilization)
- Service breakdown
- Referral sources
- Marketing data

**When to use**: Every Monday morning for weekly performance review

---

### 2. monthly_practice_data.json
**Use for**: Monthly comprehensive analysis

**Contains**:
- All weekly metrics (monthly totals)
- Profit and expense tracking
- Therapist-by-therapist breakdown
- Client lifetime value
- Marketing ROI
- Trends and changes

**When to use**: First Monday of each month for monthly review

---

## How to Use These Templates

### Method 1: Copy and Fill In

```bash
# Copy template
cp data_templates/weekly_practice_data.json my_data_week_2025-10-27.json

# Edit with your data
nano my_data_week_2025-10-27.json

# Analyze
python analyze_practice_data.py --file my_data_week_2025-10-27.json
```

### Method 2: Export from Practice Software

Most practice management systems can export session and client data. Convert it to match the template format:

```python
import pandas as pd
import json

# Read your exports
sessions = pd.read_csv('sessions_export.csv')
clients = pd.read_csv('clients_export.csv')

# Calculate metrics
weekly_data = {
    'week_of': '2025-10-27',
    'financial': {
        'revenue': sessions['fee'].sum(),
        'avg_session_rate': sessions['fee'].mean()
    },
    'clients': {
        'new_clients': len(clients[clients['start_date'] >= '2025-10-20']),
        'total_active_clients': len(clients[clients['status'] == 'active'])
    },
    'operations': {
        'total_sessions': len(sessions)
    }
    # ... add more as needed
}

# Save
with open('my_weekly_data.json', 'w') as f:
    json.dump(weekly_data, f, indent=2)
```

### Method 3: Automated Data Collection

Create a script that runs weekly/monthly:

```python
#!/usr/bin/env python3
"""Automated data collection for practice"""

from datetime import datetime, timedelta
import json

def collect_weekly_data():
    """Collect data for the past week"""

    # Get date range
    today = datetime.now()
    week_start = today - timedelta(days=7)

    # Query your practice management system
    # (This is pseudocode - adapt to your system)
    sessions = query_sessions(start_date=week_start, end_date=today)
    clients = query_clients(start_date=week_start, end_date=today)

    # Format as template
    data = {
        'week_of': week_start.strftime('%Y-%m-%d'),
        'financial': {
            'revenue': sum(s['fee'] for s in sessions),
            'avg_session_rate': sum(s['fee'] for s in sessions) / len(sessions)
        },
        'clients': {
            'new_clients': len([c for c in clients if c['is_new']]),
            'total_active_clients': len([c for c in clients if c['status'] == 'active'])
        },
        'operations': {
            'total_sessions': len(sessions)
        }
        # ... etc
    }

    # Save
    filename = f"weekly_data_{week_start.strftime('%Y-%m-%d')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Data saved to {filename}")
    return filename

if __name__ == "__main__":
    collect_weekly_data()
```

---

## Required vs. Optional Fields

### Absolutely Required (Minimum)
- `week_of` or `month` (date identifier)
- `financial.revenue`
- `clients.new_clients`
- `operations.total_sessions`

### Highly Recommended
- `financial.revenue_previous_week` (for trend analysis)
- `clients.total_active_clients`
- `operations.therapist_utilization`
- `service_breakdown` (which services are busy)
- `referral_sources` (where clients come from)

### Optional but Valuable
- `marketing_data` (for ROI analysis)
- `therapist_breakdown` (for individual performance)
- `outstanding_billing` (for cash flow)
- `waitlist_size` (for capacity planning)

---

## Field Descriptions

### Financial Fields

**revenue**: Total revenue for the period
**revenue_previous_week/month**: Previous period's revenue (for comparison)
**avg_session_rate**: Average fee per session
**outstanding_billing**: Unpaid invoices
**collections_rate**: Percentage of billed amount actually collected (0.0-1.0)
**total_expenses**: Total expenses for the period
**profit**: Revenue minus expenses
**profit_margin**: Profit divided by revenue (0.0-1.0)

### Client Fields

**new_clients**: Number of new clients who started therapy
**total_active_clients**: Total clients currently in treatment
**retention_rate**: Percentage of clients who continue (0.0-1.0)
**cancellation_rate**: Percentage of sessions canceled (0.0-1.0)
**no_show_rate**: Percentage of sessions missed without notice (0.0-1.0)
**clients_discharged**: Number of clients who completed/ended therapy
**avg_sessions_per_client**: Average number of sessions per client
**client_lifetime_value**: Average total revenue per client

### Operations Fields

**total_sessions**: Number of sessions completed
**therapist_utilization**: Percentage of available time that's booked (0.0-1.0)
**available_slots**: Number of open appointment slots
**waitlist_size**: Number of clients waiting for appointments
**avg_wait_time_days**: Average days clients wait for first appointment
**cancellation_count**: Number of cancellations
**no_show_count**: Number of no-shows

### Service Breakdown

For each service type (individual_therapy, couples_therapy, etc.):
**sessions**: Number of sessions
**revenue**: Revenue generated
**new_clients**: New clients for this service
**utilization**: How full this service is (0.0-1.0)

### Referral Sources

Count of new clients from each source:
**social_media**: Instagram, Facebook, LinkedIn
**psychology_today**: Psychology Today directory
**word_of_mouth**: Client referrals
**insurance_directory**: Insurance company listings
**google_search**: Organic search
**physician_referral**: Medical doctor referrals

### Marketing Data

**social_media_reach**: Number of people who saw posts
**social_media_engagement**: Likes, comments, shares
**engagement_rate**: Engagement divided by reach (0.0-1.0)
**website_visits**: Number of website visitors
**blog_posts_published**: Number of blog posts this period
**social_posts_published**: Number of social media posts
**inquiries_total**: Number of inquiries/leads
**inquiry_to_booking_rate**: Percentage who book after inquiring (0.0-1.0)
**cost_per_acquisition**: Marketing cost divided by new clients

---

## Data Quality Tips

### DO:
- ✅ Be consistent with date formats (YYYY-MM-DD)
- ✅ Use decimals for percentages (0.92 not 92%)
- ✅ Include all available data (more is better)
- ✅ Track referral sources accurately
- ✅ Save historical data files (don't overwrite)
- ✅ Add notes for unusual weeks (holidays, etc.)

### DON'T:
- ❌ Mix different time periods in one file
- ❌ Use percentages as whole numbers (use 0.85 not 85)
- ❌ Include PHI (no client names or identifying info)
- ❌ Forget to update date identifiers
- ❌ Skip weeks (maintain consistency)

---

## Example: SimplePractice Export to Template

**Step 1: Export from SimplePractice**
1. Go to Reports → Custom Reports
2. Select date range (last 7 days)
3. Export Sessions as CSV
4. Export Clients as CSV

**Step 2: Convert to Template Format**

```python
import pandas as pd
import json
from datetime import datetime

# Read exports
sessions = pd.read_csv('simplepractice_sessions.csv')
clients = pd.read_csv('simplepractice_clients.csv')

# Filter to date range
week_start = '2025-10-20'
week_end = '2025-10-27'
sessions_week = sessions[
    (sessions['date'] >= week_start) &
    (sessions['date'] < week_end)
]

# Calculate metrics
template = {
    'week_of': week_start,
    'financial': {
        'revenue': sessions_week['amount'].sum(),
        'avg_session_rate': sessions_week['amount'].mean(),
        'outstanding_billing': sessions_week[
            sessions_week['status'] == 'unpaid'
        ]['amount'].sum()
    },
    'clients': {
        'new_clients': len(clients[clients['intake_date'] >= week_start]),
        'total_active_clients': len(clients[clients['status'] == 'Active'])
    },
    'operations': {
        'total_sessions': len(sessions_week),
        'therapist_utilization': len(sessions_week) / 45  # Adjust denominator to your capacity
    },
    'service_breakdown': sessions_week.groupby('service_type').agg({
        'amount': ['count', 'sum']
    }).to_dict()
}

# Save
with open(f'practice_data_{week_start}.json', 'w') as f:
    json.dump(template, f, indent=2)

print(f"✓ Converted SimplePractice data to template format")
```

---

## Sample Data

Both templates include realistic sample data. You can use them to:
- Test the analysis system
- Understand what each field means
- See expected data ranges

**To analyze sample data:**
```bash
python analyze_practice_data.py --file data_templates/weekly_practice_data.json
```

---

## Custom Fields

You can add custom fields to track practice-specific metrics:

```json
{
  "week_of": "2025-10-27",
  "financial": {...},
  "clients": {...},

  "custom_metrics": {
    "group_therapy_sessions": 3,
    "telehealth_percentage": 0.40,
    "sliding_scale_clients": 8,
    "pro_bono_hours": 4,
    "supervision_hours": 2
  }
}
```

The business analyst will incorporate custom fields into analysis.

---

## Automation Examples

### Weekly Cron Job (Linux/Mac)

```bash
# Add to crontab (crontab -e)

# Run every Monday at 8am
0 8 * * 1 cd /path/to/project && python collect_weekly_data.py && python analyze_practice_data.py --file latest_data.json
```

### Python Scheduler

```python
import schedule
import time

def weekly_analysis():
    """Run weekly analysis"""
    collect_weekly_data()
    analyze_practice_data()

# Run every Monday at 8am
schedule.every().monday.at("08:00").do(weekly_analysis)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Questions?

**Documentation:**
- [HOW_TO_USE_BUSINESS_AGENTS.md](../HOW_TO_USE_BUSINESS_AGENTS.md)
- [analyze_practice_data.py](../analyze_practice_data.py)

**Agent Configurations:**
- [business-analyst/config.yaml](../agents/therapy-practice-business-analyst/config.yaml)

**Support:**
- Review templates with real data first
- Test with sample data before production
- Track all metrics consistently

---

**Start tracking your practice data today!**

```bash
cp data_templates/weekly_practice_data.json my_first_week.json
# Edit my_first_week.json with your data
python analyze_practice_data.py --file my_first_week.json
```
