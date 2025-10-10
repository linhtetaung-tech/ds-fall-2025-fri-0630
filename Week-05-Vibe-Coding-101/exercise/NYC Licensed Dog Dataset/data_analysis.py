#!/usr/bin/env python3
"""
NYC Licensed Dog Data Analysis and Visualization Script

This script creates comprehensive graphs and charts based on the NYC Licensed Dog Dataset
to answer the analytical questions outlined in the Product Requirements Document.

Author: Bryan
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class DogDataAnalyzer:
    """Comprehensive analysis and visualization for NYC Licensed Dog Data."""

    def __init__(self, data_file):
        """
        Initialize the analyzer with data file.

        Args:
            data_file: Path to the CSV data file
        """
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and preprocess the data."""
        try:
            self.df = pd.read_csv(self.data_file)
            self.preprocess_data()
            print(f"Data loaded successfully: {len(self.df)} records")
        except Exception as e:
            print(f"Error loading data: {e}")

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

        # Extract year and month for temporal analysis
        self.df['issue_year'] = self.df['licenseissueddate'].dt.year
        self.df['issue_month'] = self.df['licenseissueddate'].dt.month
        self.df['issue_weekday'] = self.df['licenseissueddate'].dt.day_name()

        # Clean breed names
        self.df['breedname'] = self.df['breedname'].str.strip()

        # Clean dog names
        self.df['animalname'] = self.df['animalname'].str.strip().str.upper()

    def create_overview_dashboard(self):
        """Create overview dashboard with key metrics."""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Total Licensed Dogs', 'Gender Distribution', 'Age Distribution',
                            'Top 5 Breeds', 'Top 5 Zip Codes', 'License Status'),
            specs=[[{"type": "indicator"}, {"type": "pie"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]]
        )

        # Total dogs indicator
        total_dogs = len(self.df)
        fig.add_trace(go.Indicator(
            mode="number",
            value=total_dogs,
            title={"text": "Total Licensed Dogs"},
            domain={'x': [0, 1], 'y': [0.5, 1]}
        ), row=1, col=1)

        # Gender distribution
        gender_counts = self.df['animalgender'].value_counts()
        fig.add_trace(go.Pie(
            labels=gender_counts.index,
            values=gender_counts.values,
            name="Gender"
        ), row=1, col=2)

        # Age distribution
        fig.add_trace(go.Histogram(
            x=self.df['current_age'],
            nbinsx=20,
            name="Age Distribution"
        ), row=1, col=3)

        # Top 5 breeds
        top_breeds = self.df['breedname'].value_counts().head(5)
        fig.add_trace(go.Bar(
            x=top_breeds.values,
            y=top_breeds.index,
            orientation='h',
            name="Top Breeds"
        ), row=2, col=1)

        # Top 5 zip codes
        top_zipcodes = self.df['zipcode'].value_counts().head(5)
        fig.add_trace(go.Bar(
            x=top_zipcodes.values,
            y=[str(z) for z in top_zipcodes.index],
            orientation='h',
            name="Top Zip Codes"
        ), row=2, col=2)

        # License status (active vs expiring soon)
        expiring_soon = len(self.df[self.df['days_until_expiry'] <= 30])
        active_licenses = len(self.df[self.df['days_until_expiry'] > 30])

        fig.add_trace(go.Pie(
            labels=['Active Licenses', 'Expiring Soon (30 days)'],
            values=[active_licenses, expiring_soon],
            name="License Status"
        ), row=2, col=3)

        fig.update_layout(
            height=800,
            title_text="NYC Licensed Dogs - Overview Dashboard",
            showlegend=False
        )

        fig.show()
        return fig

    def analyze_dog_names(self):
        """Analyze and visualize dog name patterns."""
        print("\n=== DOG NAMES ANALYSIS ===")

        # Most common dog names
        name_counts = Counter(self.df['animalname'].dropna())
        top_names = name_counts.most_common(20)

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top 20 Most Common Names', 'Name Length Distribution',
                            'Name Categories', 'Names Over Time'),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )

        # Top 20 names horizontal bar chart
        names, counts = zip(*top_names)
        fig.add_trace(go.Bar(
            x=counts,
            y=names,
            orientation='h',
            name="Top Names"
        ), row=1, col=1)

        # Name length distribution
        name_lengths = [len(name) for name in self.df['animalname'].dropna()]
        fig.add_trace(go.Histogram(
            x=name_lengths,
            nbinsx=15,
            name="Name Length"
        ), row=1, col=2)

        # Name categories (simplified)
        human_names = ['MAX', 'BELLA', 'CHARLIE', 'LUCY',
                       'COOPER', 'SADIE', 'ROCKY', 'MOLLY', 'DUKE', 'LOLA']
        human_count = sum(
            1 for name in self.df['animalname'].dropna() if name in human_names)
        other_count = len(self.df['animalname'].dropna()) - human_count

        fig.add_trace(go.Pie(
            labels=['Human-like Names', 'Other Names'],
            values=[human_count, other_count],
            name="Name Categories"
        ), row=2, col=1)

        # Names over time (top 5 names)
        top_5_names = [name for name, count in top_names[:5]]
        name_trends = self.df.groupby(
            ['issue_year', 'animalname']).size().reset_index(name='count')

        for name in top_5_names:
            name_data = name_trends[name_trends['animalname'] == name]
            if not name_data.empty:
                fig.add_trace(go.Scatter(
                    x=name_data['issue_year'],
                    y=name_data['count'],
                    mode='lines+markers',
                    name=name
                ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="Dog Names Analysis",
            showlegend=True
        )

        fig.show()

        # Print summary statistics
        print(f"Total unique names: {len(name_counts)}")
        print(
            f"Most common name: {top_names[0][0]} ({top_names[0][1]} occurrences)")
        print(f"Average name length: {np.mean(name_lengths):.1f} characters")

        return fig, top_names

    def analyze_dog_demographics(self):
        """Analyze and visualize dog age demographics."""
        print("\n=== DOG DEMOGRAPHICS ANALYSIS ===")

        # Find oldest and youngest dogs
        oldest_dog = self.df.loc[self.df['current_age'].idxmax()]
        youngest_dog = self.df.loc[self.df['current_age'].idxmin()]

        print(
            f"Oldest dog: {oldest_dog['animalname']}, Age: {oldest_dog['current_age']}, Breed: {oldest_dog['breedname']}")
        print(
            f"Youngest dog: {youngest_dog['animalname']}, Age: {youngest_dog['current_age']}, Breed: {youngest_dog['breedname']}")

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Age Distribution', 'Age by Gender',
                            'Age by Breed (Top 10)', 'Age vs License Year'),
            specs=[[{"type": "histogram"}, {"type": "box"}],
                   [{"type": "box"}, {"type": "scatter"}]]
        )

        # Age distribution histogram
        fig.add_trace(go.Histogram(
            x=self.df['current_age'],
            nbinsx=20,
            name="Age Distribution"
        ), row=1, col=1)

        # Age by gender box plot
        for gender in ['M', 'F']:
            gender_data = self.df[self.df['animalgender']
                                  == gender]['current_age']
            fig.add_trace(go.Box(
                y=gender_data,
                name=f"Gender {gender}",
                boxpoints='outliers'
            ), row=1, col=2)

        # Age by breed (top 10 breeds)
        top_breeds = self.df['breedname'].value_counts().head(10).index
        for breed in top_breeds:
            breed_data = self.df[self.df['breedname'] == breed]['current_age']
            if len(breed_data) > 0:
                fig.add_trace(go.Box(
                    y=breed_data,
                    name=breed[:15],  # Truncate long breed names
                    boxpoints='outliers'
                ), row=2, col=1)

        # Age vs License Year scatter
        fig.add_trace(go.Scatter(
            x=self.df['issue_year'],
            y=self.df['current_age'],
            mode='markers',
            marker=dict(size=4, opacity=0.6),
            name="Age vs License Year"
        ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="Dog Demographics Analysis",
            showlegend=True
        )

        fig.show()

        # Print summary statistics
        print(f"Average age: {self.df['current_age'].mean():.1f} years")
        print(f"Median age: {self.df['current_age'].median():.1f} years")
        print(
            f"Age range: {self.df['current_age'].min()} to {self.df['current_age'].max()} years")

        return fig, oldest_dog, youngest_dog

    def analyze_breeds(self):
        """Analyze and visualize dog breed distributions."""
        print("\n=== BREED ANALYSIS ===")

        # Breed statistics
        breed_counts = self.df['breedname'].value_counts()
        top_breeds = breed_counts.head(10)
        bottom_breeds = breed_counts.tail(10)

        print(f"Total unique breeds: {len(breed_counts)}")
        print(
            f"Most common breed: {top_breeds.index[0]} ({top_breeds.iloc[0]} dogs)")
        print(
            f"Least common breed: {bottom_breeds.index[-1]} ({bottom_breeds.iloc[-1]} dogs)")

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top 10 Most Common Breeds', 'Bottom 10 Least Common Breeds',
                            'Breed Distribution (Pie)', 'Breed Popularity Over Time'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )

        # Top 10 breeds
        fig.add_trace(go.Bar(
            x=top_breeds.values,
            y=top_breeds.index,
            orientation='h',
            name="Top Breeds"
        ), row=1, col=1)

        # Bottom 10 breeds
        fig.add_trace(go.Bar(
            x=bottom_breeds.values,
            y=bottom_breeds.index,
            orientation='h',
            name="Bottom Breeds"
        ), row=1, col=2)

        # Breed distribution pie chart (top 10 + others)
        top_10_count = top_breeds.sum()
        other_count = len(self.df) - top_10_count

        pie_labels = list(top_breeds.index) + ['Others']
        pie_values = list(top_breeds.values) + [other_count]

        fig.add_trace(go.Pie(
            labels=pie_labels,
            values=pie_values,
            name="Breed Distribution"
        ), row=2, col=1)

        # Breed popularity over time (top 5 breeds)
        top_5_breeds = top_breeds.head(5).index
        breed_trends = self.df.groupby(
            ['issue_year', 'breedname']).size().reset_index(name='count')

        for breed in top_5_breeds:
            breed_data = breed_trends[breed_trends['breedname'] == breed]
            if not breed_data.empty:
                fig.add_trace(go.Scatter(
                    x=breed_data['issue_year'],
                    y=breed_data['count'],
                    mode='lines+markers',
                    name=breed[:15]  # Truncate long names
                ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="Dog Breed Analysis",
            showlegend=True
        )

        fig.show()

        return fig, top_breeds, bottom_breeds

    def analyze_geographic_distribution(self):
        """Analyze and visualize geographic distribution by zip codes."""
        print("\n=== GEOGRAPHIC ANALYSIS ===")

        # Zip code statistics
        zip_counts = self.df['zipcode'].value_counts()
        top_zipcodes = zip_counts.head(10)
        bottom_zipcodes = zip_counts.tail(10)

        print(f"Total unique zip codes: {len(zip_counts)}")
        print(
            f"Zip code with most dogs: {top_zipcodes.index[0]} ({top_zipcodes.iloc[0]} dogs)")
        print(
            f"Zip code with least dogs: {bottom_zipcodes.index[-1]} ({bottom_zipcodes.iloc[-1]} dogs)")

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top 10 Zip Codes by Dog Count', 'Bottom 10 Zip Codes by Dog Count',
                            'Zip Code Distribution', 'Dogs per Zip Code Histogram'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "histogram"}]]
        )

        # Top 10 zip codes
        fig.add_trace(go.Bar(
            x=top_zipcodes.values,
            y=[str(z) for z in top_zipcodes.index],
            orientation='h',
            name="Top Zip Codes"
        ), row=1, col=1)

        # Bottom 10 zip codes
        fig.add_trace(go.Bar(
            x=bottom_zipcodes.values,
            y=[str(z) for z in bottom_zipcodes.index],
            orientation='h',
            name="Bottom Zip Codes"
        ), row=1, col=2)

        # All zip codes (limited to top 20 for readability)
        top_20_zips = zip_counts.head(20)
        fig.add_trace(go.Bar(
            x=[str(z) for z in top_20_zips.index],
            y=top_20_zips.values,
            name="Zip Code Distribution"
        ), row=2, col=1)

        # Dogs per zip code histogram
        fig.add_trace(go.Histogram(
            x=zip_counts.values,
            nbinsx=20,
            name="Dogs per Zip Code"
        ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="Geographic Distribution Analysis",
            showlegend=False
        )

        fig.show()

        return fig, top_zipcodes, bottom_zipcodes

    def analyze_license_expiry(self):
        """Analyze and visualize license expiry patterns."""
        print("\n=== LICENSE EXPIRY ANALYSIS ===")

        # Expiry statistics
        expiring_30_days = self.df[self.df['days_until_expiry'] <= 30]
        expiring_90_days = self.df[self.df['days_until_expiry'] <= 90]
        already_expired = self.df[self.df['days_until_expiry'] < 0]

        print(f"Licenses expiring in next 30 days: {len(expiring_30_days)}")
        print(f"Licenses expiring in next 90 days: {len(expiring_90_days)}")
        print(f"Already expired licenses: {len(already_expired)}")

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('License Status Distribution', 'Expiry Timeline',
                            'Top 10 Breeds Expiring Soon', 'Expiry by Zip Code (Top 10)'),
            specs=[[{"type": "pie"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )

        # License status pie chart
        status_labels = [
            'Active (>30 days)', 'Expiring Soon (≤30 days)', 'Expired']
        status_values = [
            len(self.df[self.df['days_until_expiry'] > 30]),
            len(expiring_30_days),
            len(already_expired)
        ]

        fig.add_trace(go.Pie(
            labels=status_labels,
            values=status_values,
            name="License Status"
        ), row=1, col=1)

        # Expiry timeline histogram
        fig.add_trace(go.Histogram(
            x=self.df['days_until_expiry'],
            nbinsx=30,
            name="Expiry Timeline"
        ), row=1, col=2)

        # Top breeds expiring soon
        expiring_breeds = expiring_30_days['breedname'].value_counts().head(10)
        fig.add_trace(go.Bar(
            x=expiring_breeds.values,
            y=expiring_breeds.index,
            orientation='h',
            name="Breeds Expiring Soon"
        ), row=2, col=1)

        # Top zip codes with expiring licenses
        expiring_zipcodes = expiring_30_days['zipcode'].value_counts().head(10)
        fig.add_trace(go.Bar(
            x=expiring_zipcodes.values,
            y=[str(z) for z in expiring_zipcodes.index],
            orientation='h',
            name="Zip Codes Expiring Soon"
        ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="License Expiry Analysis",
            showlegend=False
        )

        fig.show()

        # Show expiring licenses table
        if len(expiring_30_days) > 0:
            print("\nLicenses expiring in next 30 days:")
            expiring_table = expiring_30_days[[
                'animalname', 'breedname', 'zipcode', 'licenseexpireddate', 'days_until_expiry']].head(20)
            print(expiring_table.to_string(index=False))

        return fig, expiring_30_days

    def analyze_license_issuance_patterns(self):
        """Analyze and visualize license issuance patterns."""
        print("\n=== LICENSE ISSUANCE PATTERNS ANALYSIS ===")

        # Temporal analysis
        monthly_patterns = self.df.groupby('issue_month').size()
        yearly_patterns = self.df.groupby('issue_year').size()
        weekday_patterns = self.df.groupby('issue_weekday').size()

        # Create visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Licenses by Month', 'Licenses by Year', 'Licenses by Day of Week',
                            'Monthly Trends Over Years'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )

        # Monthly patterns
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig.add_trace(go.Bar(
            x=month_names,
            y=[monthly_patterns.get(i, 0) for i in range(1, 13)],
            name="Monthly Patterns"
        ), row=1, col=1)

        # Yearly patterns
        fig.add_trace(go.Bar(
            x=yearly_patterns.index,
            y=yearly_patterns.values,
            name="Yearly Patterns"
        ), row=1, col=2)

        # Weekday patterns
        weekday_order = ['Monday', 'Tuesday', 'Wednesday',
                         'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_values = [weekday_patterns.get(
            day, 0) for day in weekday_order]
        fig.add_trace(go.Bar(
            x=weekday_order,
            y=weekday_values,
            name="Weekday Patterns"
        ), row=2, col=1)

        # Monthly trends over years (heatmap-like scatter)
        monthly_yearly = self.df.groupby(
            ['issue_year', 'issue_month']).size().reset_index(name='count')
        fig.add_trace(go.Scatter(
            x=monthly_yearly['issue_year'],
            y=monthly_yearly['issue_month'],
            mode='markers',
            marker=dict(
                size=monthly_yearly['count'],
                sizemode='diameter',
                sizeref=monthly_yearly['count'].max()/50,
                color=monthly_yearly['count'],
                colorscale='Viridis',
                showscale=True
            ),
            name="Monthly-Yearly Trends"
        ), row=2, col=2)

        fig.update_layout(
            height=800,
            title_text="License Issuance Patterns Analysis",
            showlegend=False
        )

        fig.show()

        # Print summary statistics
        print(
            f"Peak licensing month: {month_names[monthly_patterns.idxmax()-1]} ({monthly_patterns.max()} licenses)")
        print(
            f"Peak licensing year: {yearly_patterns.idxmax()} ({yearly_patterns.max()} licenses)")
        print(
            f"Peak licensing day: {weekday_patterns.idxmax()} ({weekday_patterns.max()} licenses)")

        return fig, monthly_patterns, yearly_patterns, weekday_patterns

    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report with all visualizations."""
        print("="*60)
        print("NYC LICENSED DOG DATA - COMPREHENSIVE ANALYSIS REPORT")
        print("="*60)

        # Overview dashboard
        print("\nGenerating Overview Dashboard...")
        self.create_overview_dashboard()

        # Individual analyses
        name_fig, top_names = self.analyze_dog_names()
        demo_fig, oldest, youngest = self.analyze_dog_demographics()
        breed_fig, top_breeds, bottom_breeds = self.analyze_breeds()
        geo_fig, top_zips, bottom_zips = self.analyze_geographic_distribution()
        expiry_fig, expiring = self.analyze_license_expiry()
        pattern_fig, monthly, yearly, weekday = self.analyze_license_issuance_patterns()

        # Summary report
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        print(f"Dataset contains {len(self.df)} licensed dogs")
        print(
            f"Data spans from {self.df['issue_year'].min()} to {self.df['issue_year'].max()}")
        print(
            f"Most common dog name: {top_names[0][0]} ({top_names[0][1]} occurrences)")
        print(
            f"Oldest dog: {oldest['animalname']}, Age: {oldest['current_age']} years")
        print(
            f"Youngest dog: {youngest['animalname']}, Age: {youngest['current_age']} years")
        print(
            f"Most common breed: {top_breeds.index[0]} ({top_breeds.iloc[0]} dogs)")
        print(
            f"Zip code with most dogs: {top_zips.index[0]} ({top_zips.iloc[0]} dogs)")
        print(f"Licenses expiring in next 30 days: {len(expiring)}")

        return {
            'overview': self.create_overview_dashboard(),
            'names': name_fig,
            'demographics': demo_fig,
            'breeds': breed_fig,
            'geographic': geo_fig,
            'expiry': expiry_fig,
            'patterns': pattern_fig
        }


def main():
    """Main function to run the analysis."""
    # Initialize analyzer
    analyzer = DogDataAnalyzer('sample_data.csv')

    # Generate comprehensive report
    figures = analyzer.generate_comprehensive_report()

    print("\nAnalysis complete! All visualizations have been generated.")
    print("Check your browser for interactive charts.")


if __name__ == "__main__":
    main()
