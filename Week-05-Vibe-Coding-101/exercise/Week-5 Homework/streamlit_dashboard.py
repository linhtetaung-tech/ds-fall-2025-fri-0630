#!/usr/bin/env python3
"""
Streamlit Salary Analysis Dashboard
Ask A Manager 2021 Salary Survey - Interactive Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from salary_analysis import SalaryDataAnalyzer
import time

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="TechSalary Insights Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_and_clean_data():
    """Load and clean the salary data with caching."""
    analyzer = SalaryDataAnalyzer(
        "Ask A Manager Salary Survey 2021 (Responses) - Form Responses 1.tsv")
    df = analyzer.run_full_cleaning()
    return df, analyzer


def create_kpi_metrics(df):
    """Create KPI metrics for the dashboard."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_records = len(df)
        st.metric("📊 Total Records", f"{total_records:,}")

    with col2:
        us_tech_workers = len(df[
            (df['country_cleaned'] == 'UNITED STATES') &
            ((df['is_tech_role'] == True) | (df['is_tech_industry'] == True))
        ])
        st.metric("💻 US Tech Workers", f"{us_tech_workers:,}")

    with col3:
        median_tech_salary = df[
            (df['country_cleaned'] == 'UNITED STATES') &
            ((df['is_tech_role'] == True) | (df['is_tech_industry'] == True)) &
            (df['salary_usd'].notna())
        ]['salary_usd'].median()
        st.metric("💰 Median Tech Salary", f"${median_tech_salary:,.0f}")

    with col4:
        gender_gap = calculate_gender_gap(df)
        st.metric("⚖️ Gender Gap", f"{gender_gap:.1f}%")


def calculate_gender_gap(df):
    """Calculate gender gap in tech."""
    us_tech_gender = df[
        (df['country_cleaned'] == 'UNITED STATES') &
        ((df['is_tech_role'] == True) | (df['is_tech_industry'] == True)) &
        (df['salary_usd'].notna()) &
        (df['gender_cleaned'].isin(['Man', 'Woman']))
    ]

    gender_salaries = us_tech_gender.groupby(
        'gender_cleaned')['salary_usd'].median()
    men_median = gender_salaries.get('Man', 0)
    women_median = gender_salaries.get('Woman', 0)

    if men_median > 0 and women_median > 0:
        return ((men_median - women_median) / women_median) * 100
    return 0


def create_salary_distribution_plot(df, filters):
    """Create salary distribution plot."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    fig = px.histogram(
        filtered_df,
        x='salary_usd',
        nbins=30,
        title="Salary Distribution",
        labels={
            'salary_usd': 'Annual Salary (USD)', 'count': 'Number of Workers'}
    )

    # Add median line
    median_salary = filtered_df['salary_usd'].median()
    fig.add_vline(x=median_salary, line_dash="dash", line_color="red",
                  annotation_text=f"Median: ${median_salary:,.0f}")

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def create_experience_salary_plot(df, filters):
    """Create experience vs salary correlation plot."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    # Filter for records with experience data
    exp_df = filtered_df[filtered_df['years_experience_overall'].notna()]

    if len(exp_df) == 0:
        st.warning("No experience data available for selected filters.")
        return

    fig = px.scatter(
        exp_df,
        x='years_experience_overall',
        y='salary_usd',
        color='gender_cleaned',
        size='salary_usd',
        hover_data=['Job title', 'What industry do you work in?'],
        title="Experience vs Salary",
        labels={'years_experience_overall': 'Years of Experience',
                'salary_usd': 'Annual Salary (USD)'}
    )

    # Add trend line
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        exp_df['years_experience_overall'], exp_df['salary_usd'])

    x_trend = np.linspace(0, exp_df['years_experience_overall'].max(), 100)
    y_trend = slope * x_trend + intercept

    fig.add_trace(go.Scatter(
        x=x_trend, y=y_trend,
        mode='lines',
        name=f'Trend: ${slope:,.0f}/year',
        line=dict(dash='dash', color='red')
    ))

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def create_industry_comparison(df, filters):
    """Create industry comparison plot."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    industry_salaries = filtered_df.groupby('What industry do you work in?')[
        'salary_usd'].median().sort_values(ascending=True).tail(10)

    fig = px.bar(
        x=industry_salaries.values,
        y=industry_salaries.index,
        orientation='h',
        title="Top 10 Industries by Median Salary",
        labels={'x': 'Median Salary (USD)', 'y': 'Industry'}
    )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def create_geographic_analysis(df, filters):
    """Create geographic salary analysis."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    # US states analysis
    us_df = filtered_df[
        (filtered_df['country_cleaned'] == 'UNITED STATES') &
        (filtered_df['state_cleaned'].notna())
    ]

    if len(us_df) == 0:
        st.warning("No US state data available for selected filters.")
        return

    state_salaries = us_df.groupby('state_cleaned')[
        'salary_usd'].mean().sort_values(ascending=False).head(10)

    fig = px.bar(
        x=state_salaries.index,
        y=state_salaries.values,
        title="Top 10 States by Average Salary",
        labels={'x': 'State', 'y': 'Average Salary (USD)'}
    )

    fig.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)


def create_gender_analysis(df, filters):
    """Create gender gap analysis."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    gender_df = filtered_df[filtered_df['gender_cleaned'].isin([
                                                               'Man', 'Woman'])]

    if len(gender_df) == 0:
        st.warning("No gender data available for selected filters.")
        return

    gender_salaries = gender_df.groupby('gender_cleaned')[
        'salary_usd'].median()

    fig = px.bar(
        x=gender_salaries.index,
        y=gender_salaries.values,
        title="Median Salary by Gender",
        labels={'x': 'Gender', 'y': 'Median Salary (USD)'},
        color=gender_salaries.index,
        color_discrete_map={'Man': 'lightblue', 'Woman': 'lightpink'}
    )

    # Calculate and display gap
    men_median = gender_salaries.get('Man', 0)
    women_median = gender_salaries.get('Woman', 0)

    if men_median > 0 and women_median > 0:
        gap = ((men_median - women_median) / women_median) * 100
        fig.add_annotation(
            text=f"Gap: {gap:.1f}%",
            xref="paper", yref="paper",
            x=0.5, y=0.95, showarrow=False,
            font=dict(size=16, color="red")
        )

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def apply_filters(df, filters):
    """Apply filters to the dataframe."""
    filtered_df = df.copy()

    # Country filter
    if filters['country'] != 'All':
        filtered_df = filtered_df[filtered_df['country_cleaned']
                                  == filters['country']]

    # State filter (only for US)
    if filters['country'] == 'UNITED STATES' and filters['state'] != 'All':
        filtered_df = filtered_df[filtered_df['state_cleaned']
                                  == filters['state']]

    # Industry filter
    if filters['industry'] != 'All':
        filtered_df = filtered_df[filtered_df['What industry do you work in?']
                                  == filters['industry']]

    # Tech filter
    if filters['tech_only']:
        filtered_df = filtered_df[
            (filtered_df['is_tech_role'] == True) | (
                filtered_df['is_tech_industry'] == True)
        ]

    # Gender filter
    if filters['gender'] != 'All':
        filtered_df = filtered_df[filtered_df['gender_cleaned']
                                  == filters['gender']]

    # Salary range filter
    if filters['min_salary'] > 0:
        filtered_df = filtered_df[filtered_df['salary_usd']
                                  >= filters['min_salary']]

    if filters['max_salary'] < 1000000:
        filtered_df = filtered_df[filtered_df['salary_usd']
                                  <= filters['max_salary']]

    return filtered_df


def create_sidebar_filters(df):
    """Create sidebar filters."""
    st.sidebar.header("🔍 Filters")

    # Country filter
    countries = ['All'] + \
        sorted(df['country_cleaned'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)

    # State filter (only for US)
    selected_state = 'All'
    if selected_country == 'UNITED STATES':
        states = ['All'] + sorted(df[df['country_cleaned'] == 'UNITED STATES']
                                  ['state_cleaned'].dropna().unique().tolist())
        selected_state = st.sidebar.selectbox("State", states)

    # Industry filter
    industries = [
        'All'] + sorted(df['What industry do you work in?'].dropna().unique().tolist())
    selected_industry = st.sidebar.selectbox("Industry", industries)

    # Tech only filter
    tech_only = st.sidebar.checkbox("Tech roles only", value=False)

    # Gender filter
    genders = ['All', 'Man', 'Woman']
    selected_gender = st.sidebar.selectbox("Gender", genders)

    # Salary range filter
    st.sidebar.subheader("Salary Range")
    salary_range = st.sidebar.slider(
        "Select salary range",
        min_value=0,
        max_value=1000000,
        value=(0, 1000000),
        step=10000
    )

    return {
        'country': selected_country,
        'state': selected_state,
        'industry': selected_industry,
        'tech_only': tech_only,
        'gender': selected_gender,
        'min_salary': salary_range[0],
        'max_salary': salary_range[1]
    }


def create_insights_section(df, filters):
    """Create dynamic insights section."""
    filtered_df = apply_filters(df, filters)

    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
        return

    st.header("📊 Dynamic Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Top insights
        st.subheader("🎯 Key Insights")

        # Median salary
        median_salary = filtered_df['salary_usd'].median()
        st.info(f"**Median Salary**: ${median_salary:,.0f}")

        # Sample size
        st.info(f"**Sample Size**: {len(filtered_df):,} workers")

        # Top industry
        if len(filtered_df) > 0:
            top_industry = filtered_df['What industry do you work in?'].mode(
            ).iloc[0]
            st.info(f"**Most Common Industry**: {top_industry}")

        # Experience correlation
        exp_df = filtered_df[filtered_df['years_experience_overall'].notna()]
        if len(exp_df) > 10:
            from scipy import stats
            correlation = stats.pearsonr(
                exp_df['years_experience_overall'], exp_df['salary_usd'])[0]
            st.info(f"**Experience Correlation**: {correlation:.3f}")

    with col2:
        # Recommendations
        st.subheader("💡 Recommendations")

        # Geographic recommendation
        if filters['country'] == 'All':
            us_median = df[df['country_cleaned'] ==
                           'UNITED STATES']['salary_usd'].median()
            filtered_median = filtered_df['salary_usd'].median()
            if filtered_median < us_median:
                st.success("Consider US opportunities for higher salaries")

        # Industry recommendation
        if not filters['tech_only']:
            tech_median = df[(df['is_tech_role'] == True) | (
                df['is_tech_industry'] == True)]['salary_usd'].median()
            current_median = filtered_df['salary_usd'].median()
            if current_median < tech_median:
                st.success("Tech roles offer higher compensation potential")

        # Experience recommendation
        if len(exp_df) > 10:
            slope, _, _, _, _ = stats.linregress(
                exp_df['years_experience_overall'], exp_df['salary_usd'])
            if slope > 1000:
                st.success(
                    "Strong experience premium - focus on skill development")


def main():
    """Main Streamlit app."""

    # Header
    st.markdown('<h1 class="main-header">💰 TechSalary Insights Dashboard</h1>',
                unsafe_allow_html=True)
    st.markdown("### Ask A Manager 2021 Salary Survey - Interactive Analysis")

    # Load data with progress bar
    with st.spinner('Loading and cleaning data...'):
        df, analyzer = load_and_clean_data()

    st.success(f"✅ Data loaded successfully! {len(df):,} records processed.")

    # Create sidebar filters
    filters = create_sidebar_filters(df)

    # KPI Metrics
    st.header("📈 Key Performance Indicators")
    create_kpi_metrics(df)

    # Main analysis sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Salary Analysis", "📊 Industry Comparison", "🌍 Geographic Analysis",
        "⚖️ Gender Analysis", "📈 Experience Correlation", "💡 Insights"
    ])

    with tab1:
        st.header("Salary Distribution Analysis")
        create_salary_distribution_plot(df, filters)

        # Salary statistics
        filtered_df = apply_filters(df, filters)
        if len(filtered_df) > 0:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Mean Salary",
                          f"${filtered_df['salary_usd'].mean():,.0f}")
            with col2:
                st.metric("Median Salary",
                          f"${filtered_df['salary_usd'].median():,.0f}")
            with col3:
                st.metric("25th Percentile",
                          f"${filtered_df['salary_usd'].quantile(0.25):,.0f}")
            with col4:
                st.metric("75th Percentile",
                          f"${filtered_df['salary_usd'].quantile(0.75):,.0f}")

    with tab2:
        st.header("Industry Comparison")
        create_industry_comparison(df, filters)

    with tab3:
        st.header("Geographic Analysis")
        create_geographic_analysis(df, filters)

    with tab4:
        st.header("Gender Pay Gap Analysis")
        create_gender_analysis(df, filters)

    with tab5:
        st.header("Experience vs Salary Correlation")
        create_experience_salary_plot(df, filters)

    with tab6:
        create_insights_section(df, filters)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📊 TechSalary Insights Dashboard | Ask A Manager 2021 Salary Survey</p>
        <p>Built with Streamlit, Pandas, and Plotly | Data Source: 28,062 survey responses</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
