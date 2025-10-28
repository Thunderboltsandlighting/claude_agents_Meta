# /forecast - Financial Forecasting

## Command Purpose
Generate financial forecasts using multiple statistical methods with confidence intervals and scenario analysis.

## Usage
```
/forecast <historical_data> <periods> [method] [scenarios]
```

## Parameters
- `historical_data` (required): Path to historical financial data file
- `periods` (required): Number of periods to forecast (e.g., 12 for 12 months)
- `method` (optional): Forecasting method - "auto", "arima", "exp_smoothing", "regression", "ensemble" (default: "ensemble")
- `scenarios` (optional): Include scenario analysis - "yes", "no" (default: "yes")

## Examples
```
/forecast revenue_history.xlsx 12
/forecast sales_data.csv 24 arima no
/forecast financials.xlsx 6 ensemble yes
```

## Forecasting Methods

### 1. Auto (Automatic Selection)
- Analyzes data characteristics
- Selects best method automatically
- Tests multiple approaches
- Uses the highest-accuracy model

### 2. ARIMA (AutoRegressive Integrated Moving Average)
- Best for: Complex seasonal patterns, trend data
- Requires: Minimum 24 data points
- Accounts for: Trend, seasonality, autocorrelation

### 3. Exponential Smoothing
- Best for: Smooth trends, weighted recent data
- Requires: Minimum 12 data points
- Types: Simple, Holt, Holt-Winters (seasonal)

### 4. Regression
- Best for: Multi-variable relationships
- Requires: Additional predictor variables
- Types: Linear, polynomial, multiple regression

### 5. Ensemble (Recommended)
- Combines multiple methods
- Averages predictions for stability
- Generally most accurate
- Includes confidence intervals

## Workflow

### Step 1: Data Preparation
- Load historical data
- Validate time series continuity
- Check for missing values
- Detect outliers
- Transform data if needed

### Step 2: Exploratory Analysis
- Plot historical trends
- Identify seasonality
- Check for trend components
- Analyze autocorrelation

### Step 3: Model Selection & Training
- Select forecasting method(s)
- Train model on historical data
- Validate model parameters
- Test forecast accuracy (back-testing)

### Step 4: Forecast Generation
- Generate point forecasts
- Calculate confidence intervals (80%, 95%)
- Apply method to specified periods
- Validate forecast reasonability

### Step 5: Scenario Planning (if enabled)
- **Pessimistic**: Apply -10% to forecast
- **Realistic**: Use base forecast
- **Optimistic**: Apply +15% to forecast
- Calculate probability-weighted average

### Step 6: Visualization & Reporting
- Create forecast trend chart
- Show historical data overlay
- Display confidence intervals
- Include forecast table

## Output Structure

### Excel Workbook
- **Sheet 1: Forecast Summary** - Key projections and insights
- **Sheet 2: Detailed Forecast** - Period-by-period projections
- **Sheet 3: Scenarios** - Pessimistic, realistic, optimistic forecasts
- **Sheet 4: Historical Data** - Source data with transformations
- **Sheet 5: Model Performance** - Accuracy metrics and validation
- **Sheet 6: Assumptions** - Methodology and assumptions

### Visualizations
- Forecast trend chart with historical overlay
- Confidence interval bands
- Scenario comparison chart
- Forecast accuracy validation plot

## Expected Output Example
```
✓ Financial forecast completed successfully

Forecast Method: Ensemble (ARIMA + Exp. Smoothing + Regression)
Historical Period: Jan 2023 - Dec 2024 (24 months)
Forecast Period: Jan 2025 - Dec 2025 (12 months)

Model Performance:
- Mean Absolute Percentage Error (MAPE): 4.2%
- Root Mean Squared Error (RMSE): $85,234
- Model Fit (R²): 0.94

Forecast Summary:
┌──────────┬─────────────┬───────────────┬─────────────┐
│ Period   │ Forecast    │ 95% CI Lower  │ 95% CI Upper│
├──────────┼─────────────┼───────────────┼─────────────┤
│ Jan 2025 │ $425,000    │ $405,000      │ $445,000    │
│ Feb 2025 │ $430,000    │ $408,000      │ $452,000    │
│ Mar 2025 │ $448,000    │ $423,000      │ $473,000    │
│ ...      │ ...         │ ...           │ ...         │
│ Dec 2025 │ $520,000    │ $482,000      │ $558,000    │
└──────────┴─────────────┴───────────────┴─────────────┘

Annual Projections:
- Total Forecast: $5,400,000
- Growth Rate: +8.5% YoY
- Confidence: High (MAPE < 5%)

Scenario Analysis:
- Pessimistic: $4,860,000 (-10%)
- Realistic:   $5,400,000 (base)
- Optimistic:  $6,210,000 (+15%)

Files Created:
- forecast_2025.xlsx (423 KB)
- forecast_trend_chart.png (289 KB)
- scenario_comparison.png (234 KB)

Key Insights:
1. Strong growth trajectory maintained (+8.5% YoY)
2. Seasonal peak expected in Q4 2025
3. Low forecast uncertainty (tight confidence intervals)

Recommendations:
1. Plan for capacity increase in Q4
2. Monitor actual vs. forecast monthly
3. Update forecast quarterly as new data available
```

## Statistical Details

### Accuracy Metrics
- **MAPE** (Mean Absolute Percentage Error): Average % error
- **RMSE** (Root Mean Squared Error): Average absolute error
- **MAE** (Mean Absolute Error): Average deviation
- **R²** (Coefficient of Determination): Model fit quality

### Confidence Intervals
- **80% CI**: Moderate confidence range
- **95% CI**: High confidence range (standard)
- **99% CI**: Very high confidence range (optional)

### Validation Methods
- **Back-testing**: Test on historical data
- **Cross-validation**: Multiple time windows
- **Residual analysis**: Check forecast errors

## Advanced Options

### Seasonal Adjustment
```
/forecast data.xlsx 12 auto yes --seasonal 12
```
Specify seasonal period (e.g., 12 for monthly data with yearly seasonality)

### External Variables
```
/forecast data.xlsx 12 regression yes --variables "marketing_spend,website_traffic"
```
Include predictor variables for regression models

### Custom Scenarios
```
/forecast data.xlsx 12 ensemble yes --scenarios "conservative:0.95,base:1.0,aggressive:1.20"
```
Define custom scenario multipliers

## Error Handling
- Insufficient data: "Error: Need minimum 12 data points for forecasting"
- Missing values: "Warning: Gaps detected in time series. Interpolating..."
- Unstable trend: "Warning: High volatility detected. Confidence intervals widened"
- Poor fit: "Warning: Model accuracy below threshold (MAPE >10%). Consider different method"

## Best Practices
1. Provide at least 24 months of historical data for accurate forecasts
2. Ensure data is clean (no gaps, outliers handled)
3. Use ensemble method for most accurate results
4. Include scenario analysis for decision-making
5. Update forecasts monthly or quarterly
6. Monitor forecast accuracy and adjust models
7. Document assumptions clearly

## Limitations
- Forecasts assume historical patterns continue
- External shocks (pandemics, economic crises) not predicted
- Accuracy decreases with longer forecast horizons
- Requires stable, consistent data
- Cannot predict unprecedented events

## Related Commands
- `/financial` - Comprehensive analysis including forecasts
- `/variance` - Compare forecast vs. actual
- `/kpi` - Calculate forecast accuracy metrics
- `/report` - Generate forecast report

## Notes
- Forecast generation takes 5-10 minutes depending on method
- Ensemble method recommended for best accuracy
- All forecasts include uncertainty measures
- Models can be retrained as new data becomes available
- Statistical methods follow industry best practices
