# AI Investment Justification Dashboard

A sophisticated web application for evaluating the business impact and financial returns of AI use case initiatives. Built with Streamlit for interactive exploration and real-time financial modeling.

## Features

### 🎯 Four Pre-Built Use Case Templates
- **Order Management & Validation** - Complex product configurations, order capture, exception handling
- **Invoice Processing & Approval** - AP automation, exception handling, early payment optimization
- **Insurance Claims Adjudication** - Automated validation, fraud detection, straight-through processing
- **Customer Service Automation** - Inquiry deflection, agent productivity, customer retention

### 💰 Comprehensive Financial Analysis
- **Net Present Value (NPV)** with proper discounting
- **Return on Investment (ROI)** with annual breakdown
- **Payback Period** calculation
- **Multi-year projections** with realistic ramp-up curves (60% Year 1 → 100% by Year 3)
- **3% annual growth** modeling

### 📊 Interactive Visualizations
- Cash flow projection charts (bar + cumulative line)
- Stacked impact analysis by benefit category
- Year-over-year comparison tables
- Real-time metric updates as you adjust inputs

### 🔧 Fully Customizable Inputs
- Initial investment and maintenance costs
- Transaction volumes and values
- Revenue lift and cost savings percentages
- Discount rate and time horizon
- Domain-specific parameters per use case

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run use_case_dashboard_app.py
   ```

3. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to the URL shown in your terminal

## Usage Guide

### 1. Select Your Use Case
Click one of the four use case buttons at the top:
- Order Management & Validation
- Invoice Processing & Approval  
- Insurance Claims Adjudication
- Customer Service Automation

Each template loads domain-specific defaults and calculations.

### 2. Adjust Investment Parameters (Left Sidebar)

**Investment Costs:**
- Initial Investment - Upfront implementation cost
- Annual Maintenance - Ongoing costs as % of initial investment

**Business Assumptions:**
- Annual Transaction Volume - Number of transactions processed per year
- Average Transaction Value - Revenue or value per transaction
- Process Cost per Transaction - Current operational cost per unit

**Expected Improvements:**
- Revenue Lift % - Expected increase from faster cycles and reduced errors
- Cost Savings % - Expected reduction in operational costs

**Financial Assumptions:**
- Discount Rate - Cost of capital for NPV calculation
- Time Horizon - Number of years to analyze (3, 5, or 7)

### 3. Review Results

**Key Metrics Cards:**
- NPV with positive/negative indicator
- ROI with annualized return
- Payback period in years and months
- Total benefits over analysis period

**Interactive Charts:**
- **Cash Flow Projection** - Shows net annual cash flow (bars) and cumulative cash flow (line)
- **Impact Analysis** - Stacked bars showing benefit breakdown by category

**Financial Summary Table:**
- Year-by-year breakdown of costs, benefits, and cash flows
- Green highlighting when cumulative cash flow turns positive
- Downloadable as CSV

## How the Calculations Work

### Revenue Lift
```
Annual Revenue Lift = Transaction Volume × Avg Transaction Value × Revenue Factor × Revenue Lift %
```

### Cost Savings
```
Annual Cost Savings = Transaction Volume × Process Cost × Savings Factor × Cost Savings %
```

### Ramp-Up Model
- **Year 0 (Implementation):** 15% of full benefit
- **Year 1:** 60% of full benefit
- **Year 2:** 75% of full benefit  
- **Year 3+:** 100% of full benefit
- **Annual Growth:** 3% year-over-year

### NPV Calculation
```
NPV = Σ (Net Cash Flow_year / (1 + Discount Rate)^year)
```

### ROI Calculation
```
ROI = (Total Benefits - Total Costs) / Total Costs × 100%
```

### Payback Period
First year when cumulative cash flow equals or exceeds total investment costs.

## Domain Intelligence

Each use case template includes:

### Order Management
- **Revenue Factor:** 65% (revenue impact from faster order cycles)
- **Savings Factor:** 35% (cost reduction from error elimination)
- **Impact Categories:** Process Automation, Error Reduction, Cycle Time

### Invoice Processing  
- **Revenue Factor:** 45% (working capital benefits)
- **Savings Factor:** 55% (labor and exception reduction)
- **Impact Categories:** Straight-Through Processing, Early Payment Capture, Compliance

### Claims Processing
- **Revenue Factor:** 50% (fraud prevention value)
- **Savings Factor:** 50% (automation efficiency)
- **Impact Categories:** Automation Rate, Fraud Prevention, Cycle Time

### Customer Service
- **Revenue Factor:** 40% (retention value)
- **Savings Factor:** 60% (deflection and productivity)
- **Impact Categories:** Deflection & Automation, Customer Retention, Agent Productivity

## Customization

### Adding New Use Cases

Edit `use_case_dashboard_app.py` and add to the `USE_CASE_TEMPLATES` dictionary:

```python
'your-use-case': UseCaseTemplate(
    name='Your Use Case Name',
    description='Brief description of the use case',
    base_volume=100000,  # Typical annual volume
    base_value=1000,     # Average transaction value
    process_cost=50,     # Cost per transaction
    revenue_factor=0.5,  # Portion attributed to revenue
    savings_factor=0.5,  # Portion attributed to savings
    default_revenue_lift=0.20,
    default_cost_savings=0.25,
    default_investment=500000,
    default_maintenance_pct=0.20,
    impact_categories=['Category 1', 'Category 2', 'Category 3'],
    category_colors=['#3B82F6', '#10B981', '#8B5CF6']
)
```

### Modifying Calculations

All financial logic is in the `calculate_financials()` function. Key parameters:
- **Ramp-up factors** - Line 228: `ramp_factor = min(0.6 + (year * 0.15), 1.0)`
- **Growth rate** - Line 229: `growth_factor = 1 + (0.03 * (year - 1))`
- **Year 0 benefit** - Line 207: `year0_benefit = ... * 0.15`

## Deployment Options

### Local Development
```bash
streamlit run use_case_dashboard_app.py
```

### Streamlit Community Cloud (Free)
1. Push code to GitHub
2. Connect at share.streamlit.io
3. Deploy directly from repository

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY use_case_dashboard_app.py .
EXPOSE 8501
CMD ["streamlit", "run", "use_case_dashboard_app.py", "--server.port=8501"]
```

## Troubleshooting

**"Module not found" errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Port already in use:**
```bash
streamlit run use_case_dashboard_app.py --server.port=8502
```

**Charts not displaying:**
- Clear browser cache
- Try a different browser (Chrome recommended)
- Check console for JavaScript errors

## Files

- `use_case_dashboard_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `use_case_dashboard.py` - Original command-line version (reference)

## Comparison to Original Script

| Feature | Original CLI | New Web App |
|---------|-------------|-------------|
| Interface | Command-line prompts | Interactive web UI |
| Use Cases | 2 templates | 4 templates with domain intelligence |
| Charts | Static matplotlib | Interactive Plotly |
| Real-time Updates | No | Yes |
| Parameter Exploration | Re-run required | Instant updates |
| Export | Screenshots only | CSV download |
| Ramp-Up Modeling | Flat benefits | Realistic curves |
| Impact Categories | Generic split | Domain-specific breakdown |

## Support

For questions or issues:
1. Check this README
2. Review code comments in `use_case_dashboard_app.py`
3. Streamlit documentation: docs.streamlit.io

## License

Proprietary - For internal use only
