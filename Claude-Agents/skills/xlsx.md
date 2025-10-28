# Excel (XLSX) Skill

## Skill Purpose
Advanced Excel file manipulation, formatting, and data processing for financial analysis.

## Capabilities
- Read Excel files (.xlsx, .xls)
- Write formatted Excel workbooks
- Apply professional styling and formatting
- Create multi-sheet workbooks
- Generate Excel charts and graphs
- Apply conditional formatting
- Data validation and formulas
- Pivot tables and summaries

## Dependencies
```python
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, PieChart, Reference
from openpyxl.utils import get_column_letter
import xlsxwriter
```

## Usage Examples

### Reading Excel Files
```python
import pandas as pd

# Read single sheet
df = pd.read_excel('financial_data.xlsx', sheet_name='Data')

# Read multiple sheets
excel_file = pd.ExcelFile('report.xlsx')
sheets = {sheet: excel_file.parse(sheet) for sheet in excel_file.sheet_names}

# Read with specific columns
df = pd.read_excel('data.xlsx', usecols=['Date', 'Amount', 'Category'])
```

### Writing Formatted Workbooks
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create workbook
wb = Workbook()
ws = wb.active
ws.title = "Financial Report"

# Add data
ws['A1'] = 'Budget Analysis'
ws['A2'] = 'Category'
ws['B2'] = 'Budget'
ws['C2'] = 'Actual'
ws['D2'] = 'Variance'

# Format header
header_font = Font(bold=True, color='FFFFFF', size=12)
header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')

for cell in ws[2]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center')

# Save
wb.save('formatted_report.xlsx')
```

### Creating Multi-Sheet Workbooks
```python
with pd.ExcelWriter('comprehensive_report.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    details_df.to_excel(writer, sheet_name='Details', index=False)
    kpis_df.to_excel(writer, sheet_name='KPIs', index=True)
```

### Advanced Formatting
```python
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

wb = load_workbook('report.xlsx')
ws = wb['Summary']

# Add borders
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    for cell in row:
        cell.border = thin_border

# Number formatting
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=4):
    for cell in row:
        cell.number_format = '$#,##0.00'

# Auto-adjust column widths
for column in ws.columns:
    max_length = 0
    column_letter = get_column_letter(column[0].column)
    for cell in column:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    adjusted_width = min(max_length + 2, 50)
    ws.column_dimensions[column_letter].width = adjusted_width

wb.save('formatted_report.xlsx')
```

### Creating Charts
```python
from openpyxl.chart import LineChart, BarChart, Reference

# Create line chart
chart = LineChart()
chart.title = "Revenue Trend"
chart.x_axis.title = "Month"
chart.y_axis.title = "Revenue ($)"

# Add data to chart
data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=13)
categories = Reference(ws, min_col=1, min_row=2, max_row=13)
chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

# Add chart to sheet
ws.add_chart(chart, "E2")
```

### Conditional Formatting
```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.styles import PatternFill

# Color scale (red to green)
ws.conditional_formatting.add(
    'D2:D100',
    ColorScaleRule(
        start_type='min', start_color='F8696B',
        mid_type='percentile', mid_value=50, mid_color='FFEB84',
        end_type='max', end_color='63BE7B'
    )
)

# Highlight negative values
red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
ws.conditional_formatting.add(
    'D2:D100',
    CellIsRule(operator='lessThan', formula=['0'], fill=red_fill)
)
```

## Common Operations

### Budget Variance Report Template
```python
def create_variance_report(budget_df, actuals_df, output_file):
    """Create formatted variance report"""

    # Calculate variances
    variance_df = pd.merge(budget_df, actuals_df, on='Category', suffixes=('_Budget', '_Actual'))
    variance_df['Variance'] = variance_df['Amount_Actual'] - variance_df['Amount_Budget']
    variance_df['Variance_%'] = (variance_df['Variance'] / variance_df['Amount_Budget'] * 100).round(2)

    # Create Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        variance_df.to_excel(writer, sheet_name='Variance Analysis', index=False)

        wb = writer.book
        ws = writer.sheets['Variance Analysis']

        # Format header
        for cell in ws[1]:
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')

        # Format numbers
        for row in range(2, len(variance_df) + 2):
            ws[f'B{row}'].number_format = '$#,##0.00'
            ws[f'C{row}'].number_format = '$#,##0.00'
            ws[f'D{row}'].number_format = '$#,##0.00'
            ws[f'E{row}'].number_format = '0.00%'

        # Conditional formatting for variances
        red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
        green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')

        for row in range(2, len(variance_df) + 2):
            if ws[f'D{row}'].value and ws[f'D{row}'].value < 0:
                ws[f'D{row}'].fill = red_fill
            elif ws[f'D{row}'].value and ws[f'D{row}'].value > 0:
                ws[f'D{row}'].fill = green_fill
```

### KPI Dashboard Template
```python
def create_kpi_dashboard(kpis_dict, output_file):
    """Create visual KPI dashboard"""

    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet('KPI Dashboard')

    # Define formats
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'bg_color': '#366092',
        'font_color': 'white'
    })

    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'center',
        'bg_color': '#D9E1F2'
    })

    metric_format = workbook.add_format({
        'font_size': 14,
        'align': 'center',
        'num_format': '#,##0.00'
    })

    # Add title
    worksheet.merge_range('A1:D1', 'Financial KPI Dashboard', title_format)

    # Add KPIs
    row = 2
    for kpi_name, kpi_value in kpis_dict.items():
        worksheet.write(row, 0, kpi_name, header_format)
        worksheet.write(row, 1, kpi_value, metric_format)
        row += 1

    # Set column widths
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 15)

    workbook.close()
```

## Best Practices
1. Always use `with` statement for file operations
2. Close workbooks properly to avoid corruption
3. Validate data before writing to Excel
4. Use appropriate number formats for financial data
5. Apply consistent styling across sheets
6. Auto-adjust column widths for readability
7. Add borders and colors to enhance clarity
8. Include headers and titles
9. Use conditional formatting sparingly
10. Test file integrity after creation

## Performance Tips
- Use `openpyxl` for formatting-heavy operations
- Use `xlsxwriter` for large datasets with charts
- Use `pandas` for data manipulation before writing
- Avoid reading entire large files - use `chunksize`
- Close files properly to free memory

## Error Handling
```python
import pandas as pd
from openpyxl.utils.exceptions import InvalidFileException

try:
    df = pd.read_excel('data.xlsx')
except FileNotFoundError:
    print("Error: File not found")
except InvalidFileException:
    print("Error: Invalid or corrupted Excel file")
except PermissionError:
    print("Error: Permission denied to access file")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Integration with Agent
This skill is automatically available to agents that declare it in their `tools.skills` configuration.

```yaml
tools:
  skills:
    - xlsx
```

## Related Skills
- `pdf` - PDF report generation
- `reporting` - Professional report formatting
- `financial-modeling` - Advanced financial calculations
