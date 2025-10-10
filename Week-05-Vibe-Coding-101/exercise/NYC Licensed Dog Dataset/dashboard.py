#!/usr/bin/env python3
"""
Interactive Streamlit Dashboard for NYC Licensed Dog Data Analysis

This dashboard provides an interactive web interface for exploring and analyzing
NYC Licensed Dog Dataset with comprehensive visualizations and filtering options.

Author: Bryan
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="NYC Licensed Dog Data Dashboard",
    page_icon="🐕",
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
        border-left: 5px solid #1f77b4;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitDogAnalyzer:
    """Streamlit-based interactive analyzer for NYC Dog Data."""

    def __init__(self):
        """Initialize the analyzer."""
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and preprocess the data."""
        try:
            self.df = pd.read_csv('sample_data.csv')
            self.preprocess_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")

    def preprocess_data(self):
        """Clean and preprocess the data."""
        # Convert date columns
        self.df['licenseissueddate'] = pd.to_datetime(
            self.df['licenseissueddate'])
        self.df['licenseexpireddate'] = pd.to_datetime(
            self.df['licenseexpireddate'])

        # Calculate current age
        current_year = datetime.now().year
        self.df['current_age'] = current_year - self.df['animalbirth']

        # Calculate days until expiry
        self.df['days_until_expiry'] = (
            self.df['licenseexpireddate'] - datetime.now()).dt.days

        # Extract temporal components
        self.df['issue_year'] = self.df['licenseissueddate'].dt.year
        self.df['issue_month'] = self.df['licenseissueddate'].dt.month
        self.df['issue_weekday'] = self.df['licenseissueddate'].dt.day_name()

        # Clean data
        self.df['breedname'] = self.df['breedname'].str.strip()
        self.df['animalname'] = self.df['animalname'].str.strip().str.upper()

    def render_header(self):
        """Render the dashboard header."""
        st.markdown(
            '<h1 class="main-header">🐕 NYC Licensed Dog Data Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("---")

    def render_overview_metrics(self):
        """Render overview metrics cards."""
        st.subheader("📊 Overview Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Licensed Dogs",
                value=f"{len(self.df):,}",
                delta=None
            )

        with col2:
            expiring_30 = len(self.df[self.df['days_until_expiry'] <= 30])
            st.metric(
                label="Licenses Expiring (30 days)",
                value=expiring_30,
                delta=f"{expiring_30/len(self.df)*100:.1f}%"
            )

        with col3:
            most_common_breed = self.df['breedname'].value_counts().index[0]
            breed_count = self.df['breedname'].value_counts().iloc[0]
            st.metric(
                label="Most Common Breed",
                value=most_common_breed[:20],
                delta=f"{breed_count} dogs"
            )

        with col4:
            avg_age = self.df['current_age'].mean()
            st.metric(
                label="Average Dog Age",
                value=f"{avg_age:.1f} years",
                delta=None
            )

    def render_sidebar_filters(self):
        """Render sidebar filters."""
        st.sidebar.header("🔍 Filters")

        # Breed filter
        all_breeds = ['All'] + sorted(self.df['breedname'].unique().tolist())
        selected_breed = st.sidebar.selectbox("Select Breed", all_breeds)

        # Zip code filter
        all_zipcodes = ['All'] + sorted(self.df['zipcode'].unique().tolist())
        selected_zipcode = st.sidebar.selectbox(
            "Select Zip Code", all_zipcodes)

        # Gender filter
        gender_filter = st.sidebar.selectbox(
            "Select Gender", ['All', 'M', 'F'])

        # Age range filter
        age_range = st.sidebar.slider(
            "Age Range",
            min_value=int(self.df['current_age'].min()),
            max_value=int(self.df['current_age'].max()),
            value=(int(self.df['current_age'].min()),
                   int(self.df['current_age'].max()))
        )

        # Apply filters
        filtered_df = self.df.copy()

        if selected_breed != 'All':
            filtered_df = filtered_df[filtered_df['breedname']
                                      == selected_breed]

        if selected_zipcode != 'All':
            filtered_df = filtered_df[filtered_df['zipcode']
                                      == selected_zipcode]

        if gender_filter != 'All':
            filtered_df = filtered_df[filtered_df['animalgender']
                                      == gender_filter]

        filtered_df = filtered_df[
            (filtered_df['current_age'] >= age_range[0]) &
            (filtered_df['current_age'] <= age_range[1])
        ]

        st.sidebar.write(f"**Filtered Results:** {len(filtered_df)} dogs")

        return filtered_df

    def render_name_analysis(self, df):
        """Render dog names analysis."""
        st.subheader("🏷️ Dog Names Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Most common names
            name_counts = Counter(df['animalname'].dropna())
            top_names = name_counts.most_common(15)

            if top_names:
                names, counts = zip(*top_names)

                fig = px.bar(
                    x=counts,
                    y=names,
                    orientation='h',
                    title="Top 15 Most Common Dog Names",
                    labels={'x': 'Count', 'y': 'Dog Name'},
                    color=counts,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Name length distribution
            name_lengths = [len(name) for name in df['animalname'].dropna()]

            fig = px.histogram(
                x=name_lengths,
                nbins=15,
                title="Dog Name Length Distribution",
                labels={'x': 'Name Length (characters)', 'y': 'Count'},
                color_discrete_sequence=['#ff7f0e']
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    def render_demographics_analysis(self, df):
        """Render dog demographics analysis."""
        st.subheader("👥 Dog Demographics Analysis")

        # Find oldest and youngest dogs
        oldest_dog = df.loc[df['current_age'].idxmax()]
        youngest_dog = df.loc[df['current_age'].idxmin()]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🐕‍🦺 Oldest Dog")
            st.markdown(f"""
            **Name:** {oldest_dog['animalname']}  
            **Age:** {oldest_dog['current_age']} years  
            **Breed:** {oldest_dog['breedname']}  
            **Zip Code:** {oldest_dog['zipcode']}
            """)

        with col2:
            st.markdown("### 🐶 Youngest Dog")
            st.markdown(f"""
            **Name:** {youngest_dog['animalname']}  
            **Age:** {youngest_dog['current_age']} years  
            **Breed:** {youngest_dog['breedname']}  
            **Zip Code:** {youngest_dog['zipcode']}
            """)

        col1, col2 = st.columns(2)

        with col1:
            # Age distribution
            fig = px.histogram(
                df,
                x='current_age',
                nbins=20,
                title="Age Distribution",
                labels={'current_age': 'Age (years)', 'count': 'Count'},
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Age by gender
            fig = px.box(
                df,
                x='animalgender',
                y='current_age',
                title="Age Distribution by Gender",
                labels={'animalgender': 'Gender',
                        'current_age': 'Age (years)'},
                color='animalgender',
                color_discrete_sequence=['#d62728', '#ff7f0e']
            )
            st.plotly_chart(fig, use_container_width=True)

    def render_breed_analysis(self, df):
        """Render breed analysis."""
        st.subheader("🐕 Dog Breed Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Top 10 breeds
            breed_counts = df['breedname'].value_counts().head(10)

            fig = px.bar(
                x=breed_counts.values,
                y=breed_counts.index,
                orientation='h',
                title="Top 10 Most Common Breeds",
                labels={'x': 'Count', 'y': 'Breed'},
                color=breed_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Breed distribution pie chart
            top_breeds = df['breedname'].value_counts().head(8)
            other_count = len(df) - top_breeds.sum()

            pie_labels = list(top_breeds.index) + ['Others']
            pie_values = list(top_breeds.values) + [other_count]

            fig = px.pie(
                values=pie_values,
                names=pie_labels,
                title="Breed Distribution (Top 8 + Others)"
            )
            st.plotly_chart(fig, use_container_width=True)

    def render_geographic_analysis(self, df):
        """Render geographic analysis."""
        st.subheader("🗺️ Geographic Distribution Analysis")

        col1, col2 = st.columns(2)

        with col1:
            # Top zip codes
            zip_counts = df['zipcode'].value_counts().head(10)

            fig = px.bar(
                x=zip_counts.values,
                y=[str(z) for z in zip_counts.index],
                orientation='h',
                title="Top 10 Zip Codes by Dog Count",
                labels={'x': 'Count', 'y': 'Zip Code'},
                color=zip_counts.values,
                color_continuous_scale='Plasma'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Dogs per zip code histogram
            zip_counts = df['zipcode'].value_counts()

            fig = px.histogram(
                x=zip_counts.values,
                nbins=20,
                title="Distribution of Dogs per Zip Code",
                labels={'x': 'Dogs per Zip Code', 'y': 'Number of Zip Codes'},
                color_discrete_sequence=['#9467bd']
            )
            st.plotly_chart(fig, use_container_width=True)

    def render_license_analysis(self, df):
        """Render license expiry analysis."""
        st.subheader("📋 License Expiry Analysis")

        # License status
        expiring_30 = len(df[df['days_until_expiry'] <= 30])
        expiring_90 = len(df[df['days_until_expiry'] <= 90])
        expired = len(df[df['days_until_expiry'] < 0])
        active = len(df[df['days_until_expiry'] > 30])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Active Licenses", active)
        with col2:
            st.metric("Expiring in 30 days", expiring_30)
        with col3:
            st.metric("Expiring in 90 days", expiring_90)
        with col4:
            st.metric("Already Expired", expired)

        col1, col2 = st.columns(2)

        with col1:
            # License status pie chart
            status_data = {
                'Active (>30 days)': active,
                'Expiring Soon (≤30 days)': expiring_30,
                'Expired': expired
            }

            fig = px.pie(
                values=list(status_data.values()),
                names=list(status_data.keys()),
                title="License Status Distribution",
                color_discrete_sequence=['#2ca02c', '#ff7f0e', '#d62728']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Expiry timeline
            fig = px.histogram(
                df,
                x='days_until_expiry',
                nbins=30,
                title="License Expiry Timeline",
                labels={'days_until_expiry': 'Days Until Expiry',
                        'count': 'Count'},
                color_discrete_sequence=['#17becf']
            )
            fig.add_vline(x=30, line_dash="dash",
                          line_color="red", annotation_text="30 days")
            fig.add_vline(x=0, line_dash="dash",
                          line_color="orange", annotation_text="Expired")
            st.plotly_chart(fig, use_container_width=True)

        # Expiring licenses table
        if expiring_30 > 0:
            st.subheader("⚠️ Licenses Expiring in Next 30 Days")
            expiring_df = df[df['days_until_expiry'] <= 30].head(20)
            st.dataframe(
                expiring_df[['animalname', 'breedname', 'zipcode',
                             'licenseexpireddate', 'days_until_expiry']],
                use_container_width=True
            )

    def render_temporal_analysis(self, df):
        """Render temporal patterns analysis."""
        st.subheader("📅 License Issuance Patterns")

        col1, col2 = st.columns(2)

        with col1:
            # Monthly patterns
            monthly_counts = df.groupby('issue_month').size()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            fig = px.bar(
                x=month_names,
                y=[monthly_counts.get(i, 0) for i in range(1, 13)],
                title="Licenses Issued by Month",
                labels={'x': 'Month', 'y': 'Count'},
                color=[monthly_counts.get(i, 0) for i in range(1, 13)],
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Weekday patterns
            weekday_counts = df.groupby('issue_weekday').size()
            weekday_order = ['Monday', 'Tuesday', 'Wednesday',
                             'Thursday', 'Friday', 'Saturday', 'Sunday']

            fig = px.bar(
                x=weekday_order,
                y=[weekday_counts.get(day, 0) for day in weekday_order],
                title="Licenses Issued by Day of Week",
                labels={'x': 'Day of Week', 'y': 'Count'},
                color=[weekday_counts.get(day, 0) for day in weekday_order],
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

    def render_data_explorer(self, df):
        """Render interactive data explorer."""
        st.subheader("🔍 Interactive Data Explorer")

        # Search functionality
        search_term = st.text_input(
            "🔍 Search by dog name, breed, or zip code:")

        if search_term:
            mask = (
                df['animalname'].str.contains(search_term, case=False, na=False) |
                df['breedname'].str.contains(search_term, case=False, na=False) |
                df['zipcode'].astype(str).str.contains(
                    search_term, case=False, na=False)
            )
            df = df[mask]

        # Display filtered data
        st.write(f"Showing {len(df)} records")

        if len(df) > 0:
            # Sort options
            sort_by = st.selectbox("Sort by:",
                                   ['animalname', 'breedname', 'zipcode', 'current_age', 'days_until_expiry'])
            sort_order = st.selectbox(
                "Sort order:", ['Ascending', 'Descending'])

            ascending = sort_order == 'Ascending'
            df_sorted = df.sort_values(sort_by, ascending=ascending)

            # Display data table
            st.dataframe(
                df_sorted[['animalname', 'breedname', 'animalgender', 'current_age',
                           'zipcode', 'licenseexpireddate', 'days_until_expiry']],
                use_container_width=True,
                height=400
            )

            # Download button
            csv = df_sorted.to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"filtered_dog_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    def run_dashboard(self):
        """Run the complete dashboard."""
        self.render_header()

        # Sidebar filters
        filtered_df = self.render_sidebar_filters()

        # Overview metrics
        self.render_overview_metrics()
        st.markdown("---")

        # Analysis sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏷️ Names", "👥 Demographics", "🐕 Breeds", "🗺️ Geography", "📋 Licenses", "🔍 Explorer"
        ])

        with tab1:
            self.render_name_analysis(filtered_df)

        with tab2:
            self.render_demographics_analysis(filtered_df)

        with tab3:
            self.render_breed_analysis(filtered_df)

        with tab4:
            self.render_geographic_analysis(filtered_df)

        with tab5:
            self.render_license_analysis(filtered_df)

        with tab6:
            self.render_data_explorer(filtered_df)

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>NYC Licensed Dog Data Dashboard | Data from NYC Open Data API</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main function to run the dashboard."""
    analyzer = StreamlitDogAnalyzer()
    analyzer.run_dashboard()


if __name__ == "__main__":
    main()
