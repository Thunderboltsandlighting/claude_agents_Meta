# /financial - Comprehensive Financial Analysis

## Command Purpose
Perform comprehensive financial analysis including budget variance, forecasting, and KPI reporting in a single workflow.

## Usage
```
/financial <data_source> [analysis_type] [output_format]
```

## Parameters
- `data_source` (required): Path to financial data file (Excel, CSV, or database)
- `analysis_type` (optional): Type of analysis - "full", "budget", "forecast", "kpi" (default: "full")
- `output_format` (optional): Output format - "excel", "pdf", "both" (default: "excel")

## Examples
```
/financial financials_2025.xlsx
/financial budget_data.csv budget excel
/financial revenue_history.xlsx forecast both
/financial quarterly_data.xlsx kpi pdf
```

## Workflow

### Step 1: Data Loading & Validation
- Load financial data from specified source
- Validate data integrity (check for nulls, duplicates, format issues)
- Display data summary (rows, columns, date range, categories)
- Flag any data quality issues

### Step 2: Analysis Execution
Based on `analysis_type`:

**Full Analysis:**
1. Budget variance analysis (actual vs. budget)
2. 12-month financial forecast
3. Key performance indicator dashboard
4. Executive summary with insights

**Budget Analysis:**
1. Calculate variances (amount and percentage)
2. Identify material variances (>10%)
3. Create waterfall chart
4. Provide variance explanations

**Forecast Analysis:**
1. Time series forecasting (multiple methods)
2. Scenario planning (pessimistic, realistic, optimistic)
3. Confidence intervals
4. Forecast accuracy metrics

**KPI Analysis:**
1. Calculate financial ratios
2. Compute operational KPIs
3. Trend analysis (MoM, QoQ, YoY)
4. Target vs. actual comparisons

### Step 3: Visualization Creation
- Generate appropriate charts and graphs
- Professional formatting with labels and legends
- Save as high-resolution images (300 DPI)

### Step 4: Report Generation
- Create formatted Excel workbook (multiple sheets)
- Generate PDF report (if requested)
- Include executive summary
- Document methodology and assumptions

### Step 5: Quality Assurance
- Verify calculation accuracy (99.9% standard)
- Validate formatting and readability
- Check compliance with standards
- Review insights for business relevance

## Output Structure

### Excel Workbook (when output_format = "excel" or "both")
- **Sheet 1: Executive Summary** - Key findings and recommendations
- **Sheet 2: Budget Variance** - Variance analysis with details
- **Sheet 3: Forecast** - Financial projections
- **Sheet 4: KPI Dashboard** - Key performance indicators
- **Sheet 5: Raw Data** - Source data with any transformations
- **Sheet 6: Charts** - Embedded visualizations

### PDF Report (when output_format = "pdf" or "both")
- Cover page with analysis title and date
- Executive summary (1-2 pages)
- Detailed analysis sections
- Charts and visualizations
- Methodology and assumptions appendix

## Expected Output Example
```
✓ Financial analysis completed successfully

Data Summary:
- Source: financials_2025.xlsx
- Records: 1,245 transactions
- Date Range: Jan 2024 - Dec 2024
- Categories: 15 budget categories

Key Findings:
1. Overall budget variance: +$125,000 (2.5% favorable)
2. Revenue forecast: $5.2M for 2025 (+8% growth)
3. Critical KPIs: Gross margin 42%, Net margin 12%

Files Created:
- financial_analysis_2025.xlsx (756 KB)
- variance_waterfall.png (234 KB)
- forecast_trend.png (198 KB)
- kpi_dashboard.png (312 KB)

Recommendations:
- Investigate Material variance in Marketing department (+15%)
- Consider increasing Q2 budget based on forecast trends
- Monitor cash flow given projected growth
```

## Error Handling
- Invalid file path: "Error: Could not find file at specified path"
- Corrupt data: "Warning: Data quality issues detected. Please review before proceeding."
- Insufficient data: "Error: Insufficient data for forecast (minimum 12 months required)"
- Permission issues: "Error: Unable to access file. Check permissions."

## Best Practices
1. Ensure data file has clear column headers
2. Use consistent date formats (YYYY-MM-DD preferred)
3. Include both budget and actual data for variance analysis
4. Provide at least 12 months of historical data for forecasting
5. Specify categories/departments for dimensional analysis

## Related Commands
- `/kpi` - Generate KPI dashboard only
- `/forecast` - Create financial forecast only
- `/variance` - Perform budget variance analysis only
- `/report` - Generate formatted financial report from existing analysis

## Notes
- Analysis typically takes 5-15 minutes depending on data size
- Large datasets (>10,000 rows) may require additional processing time
- Sensitive financial data is never logged per security protocols
- All calculations maintain 99.9% accuracy standard
