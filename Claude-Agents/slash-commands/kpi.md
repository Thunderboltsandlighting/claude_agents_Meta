# /kpi - KPI Dashboard Generation

## Command Purpose
Generate comprehensive KPI (Key Performance Indicator) dashboard with financial and operational metrics.

## Usage
```
/kpi <financial_statements> [kpi_list] [period]
```

## Parameters
- `financial_statements` (required): Path to financial statements file
- `kpi_list` (optional): Comma-separated list of specific KPIs to calculate (default: "all")
- `period` (optional): Time period for analysis - "monthly", "quarterly", "yearly" (default: "monthly")

## Examples
```
/kpi statements_q1_2025.xlsx
/kpi financials.xlsx "margin,roi,liquidity" quarterly
/kpi annual_report.xlsx all yearly
```

## Available KPIs

### Financial KPIs
- **Profitability Ratios:**
  - Gross Profit Margin
  - Net Profit Margin
  - EBITDA Margin
  - Operating Margin
  - Return on Assets (ROA)
  - Return on Equity (ROE)
  - Return on Investment (ROI)

- **Liquidity Ratios:**
  - Current Ratio
  - Quick Ratio
  - Cash Ratio
  - Working Capital

- **Efficiency Ratios:**
  - Asset Turnover
  - Inventory Turnover
  - Receivables Turnover
  - Days Sales Outstanding (DSO)
  - Days Payable Outstanding (DPO)
  - Cash Conversion Cycle

- **Leverage Ratios:**
  - Debt-to-Equity Ratio
  - Debt-to-Assets Ratio
  - Interest Coverage Ratio

### Operational KPIs
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Revenue Per Employee
- Cost Per Unit
- Burn Rate and Runway
- Sales Growth Rate
- Churn Rate

## Workflow

### Step 1: Data Loading
- Load financial statement data
- Validate required financial metrics are present
- Extract income statement, balance sheet, cash flow data

### Step 2: KPI Calculation
- Calculate all requested KPIs
- Apply appropriate formulas for each metric
- Validate calculation accuracy

### Step 3: Trend Analysis
- Calculate period-over-period changes (MoM, QoQ, YoY)
- Identify trends (improving, declining, stable)
- Compare to targets (if provided)

### Step 4: Visualization Creation
- Generate KPI dashboard with gauges and charts
- Create trend lines for each metric
- Use color coding (green=good, yellow=warning, red=alert)

### Step 5: Dashboard Assembly
- Create executive dashboard layout
- Add metric cards with current values
- Include trend indicators
- Provide benchmark comparisons

## Output Structure

### Excel Dashboard
- **Overview Tab**: Summary of all KPIs with traffic light indicators
- **Profitability Tab**: Detailed profitability metrics with trends
- **Liquidity Tab**: Liquidity ratios and working capital analysis
- **Efficiency Tab**: Operational efficiency metrics
- **Trends Tab**: Historical trends and projections

### Visual Dashboard (PNG)
- Grid layout with metric cards
- Each card shows:
  - KPI name and current value
  - Change from previous period (% and arrow)
  - Mini trend chart (sparkline)
  - Status indicator (color-coded)

## Expected Output Example
```
✓ KPI Dashboard generated successfully

Period: Q1 2025 (Jan-Mar)
KPIs Calculated: 18 metrics

Financial Health Summary:
┌─────────────────────┬──────────┬────────┬────────┐
│ Metric              │ Current  │ Change │ Status │
├─────────────────────┼──────────┼────────┼────────┤
│ Gross Profit Margin │ 42.5%    │ +2.1%  │ ✓ Good │
│ Net Profit Margin   │ 12.3%    │ +0.8%  │ ✓ Good │
│ Current Ratio       │ 2.1:1    │ -0.1   │ ✓ Good │
│ ROE                 │ 18.5%    │ +1.2%  │ ✓ Good │
│ Debt-to-Equity      │ 0.65:1   │ -0.05  │ ✓ Good │
└─────────────────────┴──────────┴────────┴────────┘

Alerts:
⚠ DSO increased to 45 days (target: 30 days)
⚠ Inventory turnover declined 12% QoQ

Files Created:
- kpi_dashboard_q1_2025.xlsx (345 KB)
- kpi_dashboard_visual.png (412 KB)
- kpi_trends.png (287 KB)

Recommendations:
1. Address DSO increase - review collection processes
2. Investigate inventory turnover decline
3. Maintain strong profitability margins
```

## KPI Formulas Reference

### Profitability
- **Gross Profit Margin** = (Revenue - COGS) / Revenue × 100
- **Net Profit Margin** = Net Income / Revenue × 100
- **EBITDA Margin** = EBITDA / Revenue × 100
- **ROA** = Net Income / Total Assets × 100
- **ROE** = Net Income / Shareholders' Equity × 100

### Liquidity
- **Current Ratio** = Current Assets / Current Liabilities
- **Quick Ratio** = (Current Assets - Inventory) / Current Liabilities
- **Working Capital** = Current Assets - Current Liabilities

### Efficiency
- **Asset Turnover** = Revenue / Average Total Assets
- **DSO** = (Accounts Receivable / Revenue) × Days in Period
- **Inventory Turnover** = COGS / Average Inventory

### Leverage
- **Debt-to-Equity** = Total Debt / Total Equity
- **Interest Coverage** = EBIT / Interest Expense

## Customization Options

### Target Values
Provide target KPI values in a separate file:
```yaml
targets:
  gross_profit_margin: 40
  net_profit_margin: 15
  current_ratio: 2.0
  roe: 20
```

### Industry Benchmarks
Include industry benchmark data for comparison:
```yaml
benchmarks:
  industry: "SaaS Technology"
  gross_profit_margin: 75
  net_profit_margin: 20
```

## Error Handling
- Missing data: "Error: Required financial statement data not found"
- Invalid KPI name: "Warning: KPI 'xyz' not recognized. Available KPIs: [list]"
- Insufficient data: "Error: Need at least 2 periods for trend analysis"
- Division by zero: "Warning: Cannot calculate ratio (denominator is zero)"

## Best Practices
1. Ensure financial statements are complete (income statement, balance sheet)
2. Use consistent accounting periods for trend analysis
3. Provide target values for meaningful comparison
4. Review industry benchmarks for context
5. Update KPIs regularly (monthly or quarterly)

## Related Commands
- `/financial` - Comprehensive financial analysis including KPIs
- `/report` - Generate detailed financial report
- `/forecast` - Financial forecasting
- `/variance` - Budget variance analysis

## Notes
- KPI calculations follow standard accounting formulas (GAAP/IFRS)
- All financial data is handled securely per security protocols
- Dashboard generation typically takes 3-5 minutes
- Supports multiple currencies (specify in data)
