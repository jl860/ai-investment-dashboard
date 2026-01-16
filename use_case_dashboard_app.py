"""
AI Investment Justification Dashboard
======================================

A sophisticated web application for evaluating the business impact of AI use cases.
Built with Streamlit for interactive data exploration and financial modeling.

Run with:
    streamlit run use_case_dashboard_app.py

Requirements:
    pip install streamlit pandas numpy plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Page configuration
st.set_page_config(
    page_title="AI Investment Justification Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .use-case-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class UseCaseTemplate:
    name: str
    description: str
    base_volume: int
    base_value: float
    process_cost: float
    revenue_factor: float
    savings_factor: float
    default_revenue_lift: float
    default_cost_savings: float
    default_investment: float
    default_maintenance_pct: float
    impact_categories: List[str]
    category_colors: List[str]

# Define use case templates
USE_CASE_TEMPLATES = {
    'order-management': UseCaseTemplate(
        name='Order Management & Validation',
        description='Improve order capture, validation, and exception handling for complex product configurations',
        base_volume=50000,
        base_value=2500,
        process_cost=85,
        revenue_factor=0.65,
        savings_factor=0.35,
        default_revenue_lift=0.18,
        default_cost_savings=0.25,
        default_investment=500000,
        default_maintenance_pct=0.20,
        impact_categories=['Process Automation', 'Error Reduction', 'Cycle Time Improvement'],
        category_colors=['#3B82F6', '#10B981', '#8B5CF6']
    ),
    'invoice-processing': UseCaseTemplate(
        name='Invoice Processing & Approval',
        description='Automate invoice validation, exception handling, and payment optimization',
        base_volume=120000,
        base_value=3500,
        process_cost=45,
        revenue_factor=0.45,
        savings_factor=0.55,
        default_revenue_lift=0.22,
        default_cost_savings=0.30,
        default_investment=450000,
        default_maintenance_pct=0.18,
        impact_categories=['Straight-Through Processing', 'Early Payment Capture', 'Compliance'],
        category_colors=['#3B82F6', '#10B981', '#8B5CF6']
    ),
    'claims-processing': UseCaseTemplate(
        name='Insurance Claims Adjudication',
        description='Accelerate claims processing with automated validation and fraud detection',
        base_volume=85000,
        base_value=4200,
        process_cost=120,
        revenue_factor=0.50,
        savings_factor=0.50,
        default_revenue_lift=0.28,
        default_cost_savings=0.35,
        default_investment=650000,
        default_maintenance_pct=0.22,
        impact_categories=['Automation Rate', 'Fraud Prevention', 'Cycle Time'],
        category_colors=['#3B82F6', '#10B981', '#8B5CF6']
    ),
    'customer-service': UseCaseTemplate(
        name='Customer Service Automation',
        description='Deflect routine inquiries and improve agent productivity with AI assistance',
        base_volume=250000,
        base_value=85,
        process_cost=12,
        revenue_factor=0.40,
        savings_factor=0.60,
        default_revenue_lift=0.15,
        default_cost_savings=0.45,
        default_investment=380000,
        default_maintenance_pct=0.25,
        impact_categories=['Deflection & Automation', 'Customer Retention', 'Agent Productivity'],
        category_colors=['#3B82F6', '#10B981', '#8B5CF6']
    )
}

def calculate_financials(
    template: UseCaseTemplate,
    initial_investment: float,
    annual_maintenance_pct: float,
    revenue_lift_pct: float,
    cost_savings_pct: float,
    discount_rate: float,
    time_horizon: int,
    base_volume: int,
    base_value: float,
    process_cost: float
) -> Tuple[pd.DataFrame, Dict]:
    """Calculate financial projections and metrics"""
    
    annual_maintenance = initial_investment * annual_maintenance_pct
    
    # Calculate annual benefits
    revenue_lift_amount = base_volume * base_value * template.revenue_factor * revenue_lift_pct
    cost_savings_amount = base_volume * process_cost * template.savings_factor * cost_savings_pct
    
    # Build year-by-year projections
    years = []
    cumulative_cf = 0
    
    # Year 0 - Implementation year
    year0_benefit = (revenue_lift_amount + cost_savings_amount) * 0.15  # 15% benefit in year 0
    year0_net = year0_benefit - initial_investment
    cumulative_cf = year0_net
    
    years.append({
        'year': 0,
        'investment_cost': initial_investment,
        'maintenance_cost': 0,
        'revenue_lift': revenue_lift_amount * 0.15,
        'cost_savings': cost_savings_amount * 0.15,
        'operational_benefit': year0_benefit,
        'net_cash_flow': year0_net,
        'cumulative_cf': cumulative_cf,
        'discounted_cf': year0_net / ((1 + discount_rate) ** 0)
    })
    
    # Years 1-N
    for year in range(1, time_horizon + 1):
        ramp_factor = min(0.6 + (year * 0.15), 1.0)  # Ramp to full benefit
        growth_factor = 1 + (0.03 * (year - 1))  # 3% annual growth
        
        year_revenue = revenue_lift_amount * ramp_factor * growth_factor
        year_savings = cost_savings_amount * ramp_factor * growth_factor
        total_benefit = year_revenue + year_savings
        
        net_cf = total_benefit - annual_maintenance
        cumulative_cf += net_cf
        discounted_cf = net_cf / ((1 + discount_rate) ** year)
        
        years.append({
            'year': year,
            'investment_cost': 0,
            'maintenance_cost': annual_maintenance,
            'revenue_lift': year_revenue,
            'cost_savings': year_savings,
            'operational_benefit': total_benefit,
            'net_cash_flow': net_cf,
            'cumulative_cf': cumulative_cf,
            'discounted_cf': discounted_cf
        })
    
    df = pd.DataFrame(years)
    
    # Calculate metrics
    npv = df['discounted_cf'].sum()
    total_benefits = df['operational_benefit'].sum()
    total_costs = initial_investment + (annual_maintenance * time_horizon)
    roi = ((total_benefits - total_costs) / total_costs) * 100
    
    # Payback period
    payback = 'N/A'
    for idx, row in df.iterrows():
        if row['cumulative_cf'] > 0:
            if idx == 0:
                payback = 0
            else:
                prev_cf = df.loc[idx - 1, 'cumulative_cf']
                curr_cf = row['cumulative_cf']
                year_fraction = abs(prev_cf) / (curr_cf - prev_cf)
                payback = (idx - 1) + year_fraction
            break
    
    metrics = {
        'npv': npv,
        'roi': roi,
        'payback': payback,
        'total_benefits': total_benefits,
        'total_costs': total_costs
    }
    
    return df, metrics

def create_cash_flow_chart(df: pd.DataFrame) -> go.Figure:
    """Create interactive cash flow projection chart"""
    fig = go.Figure()
    
    # Net cash flow bars
    fig.add_trace(go.Bar(
        x=df['year'],
        y=df['net_cash_flow'],
        name='Net Annual Cash Flow',
        marker_color='#3B82F6',
        hovertemplate='Year %{x}<br>Net CF: $%{y:,.0f}<extra></extra>'
    ))
    
    # Cumulative cash flow line
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['cumulative_cf'],
        name='Cumulative Cash Flow',
        mode='lines+markers',
        marker=dict(size=8, color='#F59E0B'),
        line=dict(width=3, color='#F59E0B'),
        hovertemplate='Year %{x}<br>Cumulative: $%{y:,.0f}<extra></extra>'
    ))
    
    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title='Cash Flow Projection',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_impact_chart(df: pd.DataFrame, template: UseCaseTemplate) -> go.Figure:
    """Create stacked bar chart showing impact by category"""
    
    # Distribute benefits across categories with variation
    categories_data = []
    for idx, category in enumerate(template.impact_categories):
        variation = [1.2, 1.0, 0.8][idx]  # Vary by category
        values = df[df['year'] > 0]['operational_benefit'] * (variation / 3)
        categories_data.append(values)
    
    fig = go.Figure()
    
    years = df[df['year'] > 0]['year'].tolist()
    
    for idx, (category, values) in enumerate(zip(template.impact_categories, categories_data)):
        fig.add_trace(go.Bar(
            x=years,
            y=values,
            name=category,
            marker_color=template.category_colors[idx],
            hovertemplate=f'{category}<br>Year %{{x}}<br>$%{{y:,.0f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Use Case Impact Analysis',
        xaxis_title='Year',
        yaxis_title='Annual Benefit ($)',
        barmode='stack',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        template='plotly_white'
    )
    
    return fig

def main():
    # Header
    st.title("📊 AI Investment Justification Dashboard")
    st.markdown("**Strategic Framework for Evaluating Agentic AI Initiatives**")
    
    # Use Case Selection
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    use_case_buttons = {
        'order-management': col1,
        'invoice-processing': col2,
        'claims-processing': col3,
        'customer-service': col4
    }
    
    if 'selected_use_case' not in st.session_state:
        st.session_state.selected_use_case = 'order-management'
    
    for key, col in use_case_buttons.items():
        with col:
            template = USE_CASE_TEMPLATES[key]
            if st.button(
                template.name,
                key=f"btn_{key}",
                use_container_width=True,
                type="primary" if st.session_state.selected_use_case == key else "secondary"
            ):
                st.session_state.selected_use_case = key
                st.rerun()
    
    template = USE_CASE_TEMPLATES[st.session_state.selected_use_case]
    
    # Use case description
    st.markdown(f"""
    <div class="use-case-card">
        <h3>{template.name}</h3>
        <p>{template.description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Input Parameters
    st.sidebar.header("📈 Investment Parameters")
    
    st.sidebar.subheader("Investment Costs")
    initial_investment = st.sidebar.number_input(
        "Initial Investment ($)",
        min_value=0,
        value=int(template.default_investment),
        step=10000,
        help="Upfront cost for implementation, licensing, and integration"
    )
    
    annual_maintenance_pct = st.sidebar.slider(
        "Annual Maintenance (% of initial)",
        min_value=0.1,
        max_value=0.5,
        value=template.default_maintenance_pct,
        step=0.01,
        format="%.0f%%",
        help="Ongoing costs as percentage of initial investment"
    )
    
    st.sidebar.subheader("Business Assumptions")
    base_volume = st.sidebar.number_input(
        "Annual Transaction Volume",
        min_value=1000,
        value=template.base_volume,
        step=1000,
        help="Number of transactions processed annually"
    )
    
    base_value = st.sidebar.number_input(
        "Average Transaction Value ($)",
        min_value=10.0,
        value=float(template.base_value),
        step=10.0,
        help="Average revenue or value per transaction"
    )
    
    process_cost = st.sidebar.number_input(
        "Process Cost per Transaction ($)",
        min_value=1.0,
        value=float(template.process_cost),
        step=1.0,
        help="Current cost to process each transaction"
    )
    
    st.sidebar.subheader("Expected Improvements")
    revenue_lift_pct = st.sidebar.slider(
        "Revenue Lift (%)",
        min_value=0.0,
        max_value=0.5,
        value=template.default_revenue_lift,
        step=0.01,
        format="%.0f%%",
        help="Expected increase in revenue from faster cycle times and reduced errors"
    )
    
    cost_savings_pct = st.sidebar.slider(
        "Cost Savings (%)",
        min_value=0.0,
        max_value=0.5,
        value=template.default_cost_savings,
        step=0.01,
        format="%.0f%%",
        help="Expected reduction in operational costs"
    )
    
    st.sidebar.subheader("Financial Assumptions")
    discount_rate = st.sidebar.slider(
        "Discount Rate (%)",
        min_value=0.05,
        max_value=0.20,
        value=0.08,
        step=0.01,
        format="%.0f%%",
        help="Cost of capital for NPV calculation"
    )
    
    time_horizon = st.sidebar.selectbox(
        "Time Horizon (Years)",
        options=[3, 5, 7],
        index=1,
        help="Number of years to analyze"
    )
    
    # Calculate financials
    df, metrics = calculate_financials(
        template,
        initial_investment,
        annual_maintenance_pct,
        revenue_lift_pct,
        cost_savings_pct,
        discount_rate,
        time_horizon,
        base_volume,
        base_value,
        process_cost
    )
    
    # Key Metrics Display
    st.markdown("---")
    st.subheader("💰 Key Financial Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Net Present Value",
            value=f"${metrics['npv']:,.0f}",
            delta="Positive Return" if metrics['npv'] > 0 else "Negative Return",
            delta_color="normal" if metrics['npv'] > 0 else "inverse"
        )
    
    with col2:
        st.metric(
            label="Return on Investment",
            value=f"{metrics['roi']:.0f}%",
            delta=f"{metrics['roi']/time_horizon:.0f}% Annual"
        )
    
    with col3:
        payback_display = f"{metrics['payback']:.1f} Years" if metrics['payback'] != 'N/A' else 'N/A'
        months_display = f"{metrics['payback']*12:.0f} Months" if metrics['payback'] != 'N/A' else 'Not Achieved'
        st.metric(
            label="Payback Period",
            value=payback_display,
            delta=months_display
        )
    
    with col4:
        st.metric(
            label="Total Benefits",
            value=f"${metrics['total_benefits']:,.0f}",
            delta=f"Over {time_horizon} Years"
        )
    
    # Charts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_cash_flow_chart(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_impact_chart(df, template), use_container_width=True)
    
    # Financial Summary Table
    st.markdown("---")
    st.subheader("📋 Financial Summary Table")
    
    # Format DataFrame for display
    display_df = df.copy()
    display_df['Year'] = display_df['year'].astype(int)
    display_df['Investment Cost'] = display_df['investment_cost'].apply(lambda x: f"${x:,.0f}" if x > 0 else "—")
    display_df['Maintenance'] = display_df['maintenance_cost'].apply(lambda x: f"${x:,.0f}" if x > 0 else "—")
    display_df['Operational Benefits'] = display_df['operational_benefit'].apply(lambda x: f"${x:,.0f}")
    display_df['Net Cash Flow'] = display_df['net_cash_flow'].apply(lambda x: f"${x:,.0f}")
    display_df['Cumulative CF'] = display_df['cumulative_cf'].apply(lambda x: f"${x:,.0f}")
    
    display_df = display_df[['Year', 'Investment Cost', 'Maintenance', 'Operational Benefits', 'Net Cash Flow', 'Cumulative CF']]
    
    # Highlight positive cumulative CF
    def highlight_positive(row):
        cf_value = float(row['Cumulative CF'].replace('$', '').replace(',', ''))
        if cf_value > 0:
            return ['background-color: #d4edda'] * len(row)
        return [''] * len(row)
    
    styled_df = display_df.style.apply(highlight_positive, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"{template.name.replace(' ', '_')}_analysis.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>AI Investment Justification Dashboard</strong></p>
        <p>Built with Streamlit • Financial calculations use industry-standard NPV and ROI methodologies</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
