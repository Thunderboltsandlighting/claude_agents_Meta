# /report - Financial Report Generation

## Command Purpose
Generate professionally formatted financial reports from existing analysis data or raw financial data.

## Usage
```
/report <data_source> [report_type] [format] [audience]
```

## Parameters
- `data_source` (required): Path to financial data or analysis results
- `report_type` (optional): Type of report - "executive", "detailed", "board", "investor" (default: "executive")
- `format` (optional): Output format - "excel", "pdf", "powerpoint", "all" (default: "pdf")
- `audience` (optional): Target audience - "c-suite", "board", "managers", "analysts" (default: "c-suite")

## Examples
```
/report financial_analysis.xlsx
/report q1_results.xlsx detailed pdf analysts
/report annual_data.xlsx board powerpoint board
/report monthly_analysis.xlsx executive all c-suite
```

## Report Types

### 1. Executive Summary Report
- **Length**: 2-3 pages
- **Focus**: Key insights and recommendations
- **Content**:
  - Financial highlights (top 5 metrics)
  - Key variances and trends
  - Critical issues and opportunities
  - Strategic recommendations
- **Audience**: C-suite, senior leadership

### 2. Detailed Financial Report
- **Length**: 10-15 pages
- **Focus**: Comprehensive analysis
- **Content**:
  - Complete financial statements
  - Detailed variance analysis
  - Full KPI dashboard
  - Forecasts and projections
  - Supporting schedules
- **Audience**: Financial analysts, controllers

### 3. Board Report
- **Length**: 5-7 pages
- **Focus**: Governance and oversight
- **Content**:
  - Financial performance summary
  - Key risks and opportunities
  - Strategic initiatives status
  - Compliance and audit items
  - Forward-looking statements
- **Audience**: Board of Directors

### 4. Investor Report
- **Length**: 8-12 pages
- **Focus**: Performance and growth
- **Content**:
  - Revenue and profitability trends
  - Growth metrics
  - Market position
  - Capital allocation
  - Risk factors
- **Audience**: Investors, shareholders

## Workflow

### Step 1: Data Analysis
- Load source data
- Validate completeness
- Perform required calculations
- Generate summary statistics

### Step 2: Content Generation
Based on report_type:
- **Executive**: Extract key insights
- **Detailed**: Compile comprehensive data
- **Board**: Focus on governance items
- **Investor**: Highlight growth and performance

### Step 3: Visualization Creation
- Generate appropriate charts and graphs
- Apply professional styling
- Ensure consistency across visuals

### Step 4: Report Assembly
- Create report structure
- Add cover page and table of contents
- Insert analysis sections
- Include visualizations
- Add appendices

### Step 5: Formatting & Polish
- Apply professional formatting
- Check consistency
- Validate all numbers
- Add page numbers and headers
- Include disclaimers

### Step 6: Quality Assurance
- Verify calculation accuracy
- Check formatting consistency
- Validate cross-references
- Review for clarity and readability

## Output Structure

### Executive Summary Report
1. **Cover Page**
   - Report title
   - Period covered
   - Date generated
   - Company name/logo

2. **Executive Summary** (1 page)
   - Financial highlights
   - Key takeaways (3-5 bullets)
   - Critical actions required

3. **Financial Overview** (1 page)
   - Summary financial statements
   - Key metrics dashboard
   - Period comparisons

4. **Recommendations** (1 page)
   - Strategic recommendations
   - Action items with owners
   - Timeline for implementation

### Detailed Financial Report
1. **Cover & TOC**
2. **Executive Summary**
3. **Financial Statements**
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
4. **Variance Analysis**
   - Budget vs. Actual
   - Prior period comparisons
5. **KPI Dashboard**
   - Financial KPIs
   - Operational KPIs
6. **Forecasts & Projections**
7. **Appendices**
   - Methodology
   - Assumptions
   - Supporting schedules

### Board Report
1. **Cover Page**
2. **Executive Summary**
3. **Financial Performance**
   - Key metrics
   - Variances explained
4. **Strategic Initiatives**
   - Progress on key projects
5. **Risk & Compliance**
   - Key risks identified
   - Mitigation plans
   - Compliance status
6. **Forward-Looking**
   - Forecasts
   - Strategic plans

### Investor Report
1. **Cover & Highlights**
2. **Business Performance**
   - Revenue growth
   - Profitability trends
3. **Market Position**
4. **Growth Initiatives**
5. **Financial Strength**
   - Balance sheet highlights
   - Cash position
6. **Forward Guidance**

## Expected Output Example
```
✓ Financial report generated successfully

Report Configuration:
- Type: Executive Summary
- Period: Q1 2025 (Jan-Mar)
- Format: PDF + Excel
- Audience: C-Suite
- Pages: 3

Content Summary:
┌────────────────────────────────────┬─────────┐
│ Section                            │ Status  │
├────────────────────────────────────┼─────────┤
│ Cover Page                         │ ✓ Done  │
│ Executive Summary                  │ ✓ Done  │
│ Financial Highlights               │ ✓ Done  │
│ Key Metrics Dashboard              │ ✓ Done  │
│ Variance Analysis Summary          │ ✓ Done  │
│ Recommendations                    │ ✓ Done  │
└────────────────────────────────────┴─────────┘

Key Highlights Included:
- Revenue: $15.2M (+12% YoY)
- Net Margin: 18.5% (+2.1pp)
- Cash Position: $4.8M (Strong)
- 3 strategic recommendations

Visualizations:
- Revenue trend chart (5 quarters)
- KPI dashboard (8 metrics)
- Variance waterfall
- Cash flow summary

Files Created:
- Executive_Report_Q1_2025.pdf (1.2 MB)
- Executive_Report_Q1_2025.xlsx (456 KB)
- Supporting_Charts/ (4 PNG files, 891 KB total)

Quality Checks:
✓ All calculations verified (99.9% accuracy)
✓ Formatting consistent throughout
✓ All cross-references validated
✓ Numbers tied to source data
✓ Professional appearance confirmed

Report Statistics:
- Generation Time: 8 minutes
- Total Pages: 3
- Charts/Tables: 12
- Data Points Analyzed: 1,247

Next Steps:
1. Review report for final approval
2. Distribute to C-suite leadership
3. Schedule follow-up discussion
4. Archive for compliance records
```

## Formatting Standards

### Typography
- **Headings**: Sans-serif, bold, hierarchical sizing
- **Body**: Serif font, 11-12pt, line spacing 1.15
- **Numbers**: Monospace for alignment
- **Emphasis**: Bold for key numbers, italics for notes

### Color Scheme
- **Primary**: Navy blue (#002366)
- **Accent**: Teal (#008B8B)
- **Positive**: Green (#228B22)
- **Negative**: Red (#DC143C)
- **Neutral**: Gray (#708090)

### Layout
- **Margins**: 1 inch all sides
- **Headers**: Company name, report title
- **Footers**: Page numbers, date generated
- **White Space**: Generous spacing for readability

### Tables
- Header row with background color
- Alternating row colors for readability
- Right-align numbers
- Currency symbols and thousand separators
- Total rows with bold and border

### Charts
- Clear titles and axis labels
- Legend when multiple series
- Data labels for key points
- Consistent color scheme
- Professional chart types

## Customization Options

### Branding
```yaml
branding:
  company_name: "Acme Corporation"
  logo_path: "assets/logo.png"
  primary_color: "#002366"
  secondary_color: "#008B8B"
```

### Report Sections
```yaml
sections:
  include:
    - executive_summary
    - financial_statements
    - kpi_dashboard
    - recommendations
  exclude:
    - appendices
    - detailed_schedules
```

### Confidentiality
```yaml
confidentiality:
  level: "Confidential"
  watermark: true
  distribution_list:
    - "C-Suite Only"
```

## Error Handling
- Missing data: "Warning: Some data unavailable. Report generated with available data."
- Format error: "Error: Cannot generate PowerPoint format. Creating PDF instead."
- Incomplete analysis: "Warning: Some sections incomplete. Review before distribution."

## Best Practices
1. **Accuracy First**: Verify all numbers before generation
2. **Clear Communication**: Use plain language, avoid jargon
3. **Visual Appeal**: Professional appearance matters
4. **Actionable Insights**: Include specific recommendations
5. **Appropriate Detail**: Match detail level to audience
6. **Timely Delivery**: Generate reports promptly
7. **Version Control**: Date and version all reports
8. **Confidentiality**: Mark sensitivity appropriately

## Report Distribution

### Automated Distribution
- Email to specified recipients
- Upload to shared drive
- Post to dashboard
- Archive in document management system

### Version Control
- Timestamp on every page
- Version number (v1.0, v1.1, etc.)
- Track changes and updates
- Maintain distribution log

## Related Commands
- `/financial` - Generate analysis to feed into report
- `/kpi` - Calculate metrics for report
- `/forecast` - Include projections in report
- `/variance` - Add variance analysis to report

## Notes
- Report generation takes 5-10 minutes depending on complexity
- All reports maintain 99.9% calculation accuracy
- PDF format recommended for distribution
- Excel format useful for analysis and backup
- PowerPoint for presentations
- Sensitive financial data never logged per security protocols
- Reports automatically archived with timestamp
