# /variance - Budget Variance Analysis

## Command Purpose
Perform comprehensive budget variance analysis comparing actual vs. budget with detailed reporting.

## Usage
```
/variance <budget_file> <actuals_file> [threshold] [dimension]
```

## Parameters
- `budget_file` (required): Path to budget data file
- `actuals_file` (required): Path to actual results file
- `threshold` (optional): Variance threshold % for flagging material variances (default: 10)
- `dimension` (optional): Analysis dimension - "category", "department", "time", "all" (default: "all")

## Examples
```
/variance budget_2025.xlsx actuals_jan_2025.xlsx
/variance budget.csv actuals.csv 15 department
/variance annual_budget.xlsx q1_actuals.xlsx 5 all
```

## Variance Analysis Components

### 1. Overall Variance Summary
- Total budget vs. actual
- Favorable vs. unfavorable variances
- Material variances (exceeding threshold)
- Variance percentage calculation

### 2. Dimensional Analysis
- By category (revenue, expenses, investments)
- By department (sales, marketing, operations, etc.)
- By time period (monthly, quarterly, YTD)
- Cross-dimensional drill-down

### 3. Variance Classification
- **Favorable**: Actual > Budget (revenue) or Actual < Budget (expenses)
- **Unfavorable**: Actual < Budget (revenue) or Actual > Budget (expenses)
- **Material**: Variance exceeds specified threshold
- **On Target**: Variance within acceptable range

## Workflow

### Step 1: Data Loading & Validation
- Load budget and actual data files
- Validate data structures match
- Check for common dimensions (categories, departments, periods)
- Identify any missing data

### Step 2: Data Alignment
- Merge budget and actual data on common keys
- Handle missing categories or departments
- Align time periods
- Convert to common currency/units

### Step 3: Variance Calculation
```
Variance (Amount) = Actual - Budget
Variance (%) = (Actual - Budget) / Budget × 100
```

### Step 4: Classification & Flagging
- Classify variances (favorable/unfavorable)
- Flag material variances (> threshold)
- Identify trends and patterns
- Rank by significance

### Step 5: Root Cause Analysis
- Analyze variance drivers
- Identify anomalies
- Compare period-over-period
- Suggest potential explanations

### Step 6: Visualization Creation
- Waterfall chart showing variance bridge
- Heat map of variances by dimension
- Trend charts for significant items
- Summary dashboard

### Step 7: Report Generation
- Executive summary
- Detailed variance tables
- Visual representations
- Recommendations

## Output Structure

### Excel Workbook
- **Sheet 1: Executive Summary** - Key variances and insights
- **Sheet 2: Overall Variance** - Total budget vs. actual
- **Sheet 3: By Category** - Category-level variances
- **Sheet 4: By Department** - Department-level variances
- **Sheet 5: By Time Period** - Monthly/quarterly trends
- **Sheet 6: Material Variances** - Items exceeding threshold
- **Sheet 7: Raw Data** - Budget and actual data merged

### Visualizations
- Variance waterfall chart
- Heat map (departments × categories)
- Trend lines for key categories
- Pareto chart (80/20 analysis)

## Expected Output Example
```
✓ Budget variance analysis completed

Analysis Period: January 2025
Budget vs. Actual Comparison

Overall Summary:
┌─────────────────┬──────────────┬──────────────┬─────────────┬──────────┐
│ Category        │ Budget       │ Actual       │ Variance $  │ Variance %│
├─────────────────┼──────────────┼──────────────┼─────────────┼──────────┤
│ Revenue         │ $5,000,000   │ $5,125,000   │ +$125,000   │ +2.5%  ✓ │
│ Cost of Sales   │ $2,000,000   │ $1,950,000   │ -$50,000    │ -2.5%  ✓ │
│ Operating Exp   │ $2,500,000   │ $2,650,000   │ +$150,000   │ +6.0%  ⚠ │
│ Net Income      │ $500,000     │ $525,000     │ +$25,000    │ +5.0%  ✓ │
└─────────────────┴──────────────┴──────────────┴─────────────┴──────────┘

Material Variances (>10% threshold):
1. Marketing Dept: +$75,000 (+15.0%) - UNFAVORABLE
   • New campaign spending ahead of schedule
   • Digital advertising costs higher than budgeted

2. IT Department: -$35,000 (-12.3%) - FAVORABLE
   • Cloud service migration completed early
   • Software licensing costs reduced

3. Sales Dept: +$125,000 (+11.2%) - FAVORABLE (Revenue)
   • New product launch exceeded expectations
   • Enterprise client conversions ahead of plan

Department Performance:
┌──────────────┬────────────┬──────────┬────────────┐
│ Department   │ Budget     │ Variance │ Status     │
├──────────────┼────────────┼──────────┼────────────┤
│ Sales        │ $5,000,000 │ +2.5%    │ ✓ On Track │
│ Marketing    │ $500,000   │ +15.0%   │ ⚠ Over     │
│ Operations   │ $1,200,000 │ +3.2%    │ ✓ On Track │
│ IT           │ $285,000   │ -12.3%   │ ✓ Under    │
│ Admin        │ $515,000   │ +1.5%    │ ✓ On Track │
└──────────────┴────────────┴──────────┴────────────┘

Variance Bridge (Waterfall):
Starting Budget: $500,000
+ Revenue Variance: +$125,000
- COGS Savings: +$50,000
- OpEx Overrun: -$150,000
= Actual Net Income: $525,000

Files Created:
- variance_analysis_jan2025.xlsx (456 KB)
- variance_waterfall.png (298 KB)
- variance_heatmap.png (234 KB)
- department_comparison.png (267 KB)

Key Insights:
1. Overall favorable variance of $25,000 (+5.0%)
2. Revenue exceeded budget driven by strong sales performance
3. Marketing overspending requires attention
4. IT cost savings from cloud migration

Recommendations:
1. URGENT: Review marketing spending - adjust Q2 budget if needed
2. Investigate sales success factors for replication
3. Document IT cost savings for future budgeting
4. Monitor operating expenses closely in coming months
5. Update annual forecast based on Jan performance
```

## Variance Analysis Formulas

### Basic Variances
- **Revenue Variance** = Actual Revenue - Budgeted Revenue
- **Expense Variance** = Actual Expense - Budgeted Expense
- **Variance %** = (Variance / Budget) × 100

### Advanced Variances
- **Volume Variance** = (Actual Volume - Budget Volume) × Budget Price
- **Price Variance** = (Actual Price - Budget Price) × Actual Volume
- **Mix Variance** = Change in product/service mix impact

### Year-to-Date Analysis
- **YTD Variance** = Sum of monthly variances
- **Run Rate Impact** = Monthly variance × remaining months

## Analysis Dimensions

### By Category
- Revenue (by product line, service, customer segment)
- Cost of Goods Sold (materials, labor, overhead)
- Operating Expenses (marketing, R&D, G&A)
- Capital Expenditures

### By Department
- Sales & Marketing
- Operations & Production
- Research & Development
- IT & Technology
- Finance & Administration

### By Time Period
- Monthly comparison
- Quarterly trends
- Year-to-date accumulation
- Rolling 12-month analysis

## Threshold Settings

### Conservative (5-10%)
- Use for: Tight budget controls, mature operations
- Flag: Most variances for review
- Risk: High false positives

### Moderate (10-15%)
- Use for: Standard budget management
- Flag: Material variances only
- Risk: Balanced approach

### Aggressive (15-20%)
- Use for: High-growth, volatile environments
- Flag: Significant variances only
- Risk: May miss important items

## Error Handling
- Mismatched dimensions: "Error: Budget and actual files have different categories"
- Missing data: "Warning: No budget data for [category]. Excluding from analysis."
- Zero budget: "Warning: Cannot calculate variance % (budget = 0)"
- Date mismatch: "Error: Budget and actual periods do not align"

## Best Practices
1. Ensure budget and actual data use consistent categories
2. Review material variances promptly
3. Document variance explanations for audit trail
4. Update forecasts based on variance trends
5. Communicate significant variances to stakeholders
6. Track variance patterns over time
7. Adjust future budgets based on learnings

## Integration with Other Analysis
- Combine with `/forecast` to update projections
- Use with `/kpi` to assess budget performance metrics
- Include in `/financial` comprehensive reports
- Feed into `/report` for stakeholder communication

## Related Commands
- `/financial` - Full financial analysis including variance
- `/forecast` - Update forecasts based on variances
- `/kpi` - Calculate budget performance KPIs
- `/report` - Generate variance report for stakeholders

## Notes
- Variance analysis takes 3-7 minutes depending on data size
- Material variances require follow-up explanation
- Both favorable and unfavorable variances need review
- Regular variance analysis improves budget accuracy
- Maintains 99.9% calculation accuracy standard
