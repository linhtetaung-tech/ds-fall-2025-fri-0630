#!/usr/bin/env python3
"""
Salary Analysis Dashboard - Interactive Visualization
Ask A Manager Salary Survey 2021
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from salary_analysis import SalaryDataAnalyzer
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SalaryDashboard:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.results = {}
        
    def run_analysis_and_visualize(self):
        """Run analysis and create comprehensive dashboard."""
        print("Running salary analysis...")
        self.results = self.analyzer.run_all_analyses()
        
        # Create dashboard
        fig = plt.figure(figsize=(20, 16))
        
        # Main title
        fig.suptitle('TechSalary Insights - Ask A Manager 2021 Salary Analysis Dashboard', 
                    fontsize=24, fontweight='bold', y=0.98)
        
        # 1. Software Engineer Salary Distribution
        ax1 = plt.subplot(3, 3, 1)
        self._plot_software_engineer_salaries(ax1)
        
        # 2. Top 10 States for Tech Workers
        ax2 = plt.subplot(3, 3, 2)
        self._plot_top_tech_states(ax2)
        
        # 3. Experience vs Salary Correlation
        ax3 = plt.subplot(3, 3, 3)
        self._plot_experience_salary_correlation(ax3)
        
        # 4. Industry Comparison
        ax4 = plt.subplot(3, 3, 4)
        self._plot_industry_comparison(ax4)
        
        # 5. Gender Gap Analysis
        ax5 = plt.subplot(3, 3, 5)
        self._plot_gender_gap(ax5)
        
        # 6. Education Impact
        ax6 = plt.subplot(3, 3, 6)
        self._plot_education_impact(ax6)
        
        # 7. Salary Distribution by Tech vs Non-Tech
        ax7 = plt.subplot(3, 3, 7)
        self._plot_tech_vs_nontech_salaries(ax7)
        
        # 8. Top Job Titles in Tech
        ax8 = plt.subplot(3, 3, 8)
        self._plot_top_tech_job_titles(ax8)
        
        # 9. Summary Statistics
        ax9 = plt.subplot(3, 3, 9)
        self._plot_summary_stats(ax9)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.94)
        plt.savefig('salary_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return self.results
    
    def _plot_software_engineer_salaries(self, ax):
        """Plot software engineer salary distribution."""
        us_software_engineers = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.analyzer.cleaned_df['is_software_engineer'] == True) &
            (self.analyzer.cleaned_df['salary_usd'].notna())
        ]
        
        ax.hist(us_software_engineers['salary_usd'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        median_salary = us_software_engineers['salary_usd'].median()
        ax.axvline(median_salary, color='red', linestyle='--', linewidth=2, 
                  label=f'Median: ${median_salary:,.0f}')
        
        ax.set_title('Software Engineer Salary Distribution (US)', fontweight='bold')
        ax.set_xlabel('Annual Salary (USD)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.ticklabel_format(style='plain', axis='x')
    
    def _plot_top_tech_states(self, ax):
        """Plot top 10 states for tech worker salaries."""
        us_tech_workers = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.analyzer.cleaned_df['state_cleaned'].notna()) &
            ((self.analyzer.cleaned_df['is_tech_role'] == True) | 
             (self.analyzer.cleaned_df['is_tech_industry'] == True)) &
            (self.analyzer.cleaned_df['salary_usd'].notna())
        ]
        
        state_salaries = us_tech_workers.groupby('state_cleaned')['salary_usd'].mean().sort_values(ascending=True)
        state_salaries = state_salaries[state_salaries.index.notna()]
        
        # Get top 10 states
        top_10 = state_salaries.tail(10)
        
        bars = ax.barh(range(len(top_10)), top_10.values, color='lightcoral')
        ax.set_yticks(range(len(top_10)))
        ax.set_yticklabels([state.replace(' ', '\n') for state in top_10.index], fontsize=9)
        ax.set_xlabel('Average Salary (USD)')
        ax.set_title('Top 10 States - Tech Worker Salaries', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, top_10.values)):
            ax.text(value + 1000, i, f'${value:,.0f}', va='center', fontsize=8)
    
    def _plot_experience_salary_correlation(self, ax):
        """Plot experience vs salary correlation."""
        us_tech_with_exp = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.analyzer.cleaned_df['is_tech_role'] == True) | 
             (self.analyzer.cleaned_df['is_tech_industry'] == True)) &
            (self.analyzer.cleaned_df['salary_usd'].notna()) &
            (self.analyzer.cleaned_df['years_experience_overall'].notna())
        ]
        
        # Sample for better visualization
        sample_size = min(1000, len(us_tech_with_exp))
        sample_data = us_tech_with_exp.sample(n=sample_size, random_state=42)
        
        ax.scatter(sample_data['years_experience_overall'], sample_data['salary_usd'], 
                  alpha=0.6, color='green', s=20)
        
        # Add trend line
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            us_tech_with_exp['years_experience_overall'], us_tech_with_exp['salary_usd'])
        
        x_trend = np.linspace(0, 45, 100)
        y_trend = slope * x_trend + intercept
        ax.plot(x_trend, y_trend, 'r-', linewidth=2, 
               label=f'Trend: ${slope:,.0f}/year (r={r_value:.2f})')
        
        ax.set_xlabel('Years of Experience')
        ax.set_ylabel('Annual Salary (USD)')
        ax.set_title('Experience vs Salary in Tech', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_industry_comparison(self, ax):
        """Plot top industries by median salary."""
        us_nontech = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.analyzer.cleaned_df['is_tech_industry'] == False) &
            (self.analyzer.cleaned_df['salary_usd'].notna())
        ]
        
        industry_salaries = us_nontech.groupby('What industry do you work in?')['salary_usd'].median()
        industry_salaries = industry_salaries.sort_values(ascending=True).tail(10)
        
        bars = ax.barh(range(len(industry_salaries)), industry_salaries.values, color='lightblue')
        ax.set_yticks(range(len(industry_salaries)))
        ax.set_yticklabels([ind.replace(' ', '\n')[:20] for ind in industry_salaries.index], fontsize=8)
        ax.set_xlabel('Median Salary (USD)')
        ax.set_title('Top 10 Non-Tech Industries', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, industry_salaries.values)):
            ax.text(value + 1000, i, f'${value:,.0f}', va='center', fontsize=8)
    
    def _plot_gender_gap(self, ax):
        """Plot gender gap in tech salaries."""
        us_tech_gender = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.analyzer.cleaned_df['is_tech_role'] == True) | 
             (self.analyzer.cleaned_df['is_tech_industry'] == True)) &
            (self.analyzer.cleaned_df['salary_usd'].notna()) &
            (self.analyzer.cleaned_df['gender_cleaned'].isin(['Man', 'Woman']))
        ]
        
        gender_salaries = us_tech_gender.groupby('gender_cleaned')['salary_usd'].median()
        
        bars = ax.bar(['Men', 'Women'], [gender_salaries.get('Man', 0), gender_salaries.get('Woman', 0)], 
                     color=['lightblue', 'lightpink'])
        
        # Add value labels on bars
        for bar, value in zip(bars, [gender_salaries.get('Man', 0), gender_salaries.get('Woman', 0)]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1000,
                   f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        gap = ((gender_salaries.get('Man', 0) - gender_salaries.get('Woman', 0)) / 
               gender_salaries.get('Woman', 1)) * 100
        
        ax.set_ylabel('Median Salary (USD)')
        ax.set_title(f'Gender Gap in Tech: {gap:.1f}%', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _plot_education_impact(self, ax):
        """Plot education level impact on salaries."""
        us_with_education = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.analyzer.cleaned_df['salary_usd'].notna()) &
            (self.analyzer.cleaned_df['education_cleaned'].str.contains('Master|College degree', case=False, na=False))
        ]
        
        # Categorize education
        us_with_education = us_with_education.copy()
        us_with_education['education_category'] = us_with_education['education_cleaned'].apply(
            lambda x: 'Master\'s' if 'master' in str(x).lower() else 'Bachelor\'s' if 'college' in str(x).lower() else 'Other'
        )
        
        education_salaries = us_with_education.groupby('education_category')['salary_usd'].median()
        
        bars = ax.bar(['Bachelor\'s', 'Master\'s'], 
                     [education_salaries.get('Bachelor\'s', 0), education_salaries.get('Master\'s', 0)],
                     color=['lightgreen', 'lightcoral'])
        
        # Add value labels
        for bar, value in zip(bars, [education_salaries.get('Bachelor\'s', 0), education_salaries.get('Master\'s', 0)]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1000,
                   f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        increase = ((education_salaries.get('Master\'s', 0) - education_salaries.get('Bachelor\'s', 0)) / 
                   education_salaries.get('Bachelor\'s', 1)) * 100
        
        ax.set_ylabel('Median Salary (USD)')
        ax.set_title(f'Education Impact: {increase:.1f}% Increase', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _plot_tech_vs_nontech_salaries(self, ax):
        """Plot salary distribution comparison between tech and non-tech."""
        us_workers = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.analyzer.cleaned_df['salary_usd'].notna())
        ]
        
        tech_salaries = us_workers[
            (us_workers['is_tech_role'] == True) | (us_workers['is_tech_industry'] == True)
        ]['salary_usd']
        
        nontech_salaries = us_workers[
            (us_workers['is_tech_role'] == False) & (us_workers['is_tech_industry'] == False)
        ]['salary_usd']
        
        ax.hist([tech_salaries, nontech_salaries], bins=30, alpha=0.7, 
               label=['Tech', 'Non-Tech'], color=['skyblue', 'lightcoral'])
        
        tech_median = tech_salaries.median()
        nontech_median = nontech_salaries.median()
        
        ax.axvline(tech_median, color='blue', linestyle='--', linewidth=2, 
                  label=f'Tech Median: ${tech_median:,.0f}')
        ax.axvline(nontech_median, color='red', linestyle='--', linewidth=2, 
                  label=f'Non-Tech Median: ${nontech_median:,.0f}')
        
        ax.set_xlabel('Annual Salary (USD)')
        ax.set_ylabel('Frequency')
        ax.set_title('Tech vs Non-Tech Salary Distribution', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_top_tech_job_titles(self, ax):
        """Plot most common tech job titles."""
        us_tech_workers = self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.analyzer.cleaned_df['is_tech_role'] == True) | 
             (self.analyzer.cleaned_df['is_tech_industry'] == True)) &
            (self.analyzer.cleaned_df['salary_usd'].notna())
        ]
        
        # Get most common job titles
        job_counts = us_tech_workers['Job title'].value_counts().head(10)
        
        bars = ax.barh(range(len(job_counts)), job_counts.values, color='lightsteelblue')
        ax.set_yticks(range(len(job_counts)))
        ax.set_yticklabels([title.replace(' ', '\n')[:15] for title in job_counts.index], fontsize=8)
        ax.set_xlabel('Number of Workers')
        ax.set_title('Top 10 Tech Job Titles', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, job_counts.values)):
            ax.text(value + 1, i, str(value), va='center', fontsize=8)
    
    def _plot_summary_stats(self, ax):
        """Plot summary statistics."""
        ax.axis('off')
        
        # Create summary text
        summary_text = f"""
        📊 SALARY ANALYSIS SUMMARY
        
        💰 Software Engineers (US): ${self.results.get('software_engineer_median', 0):,.0f}
        
        🏆 Top Tech State: {self.results.get('highest_tech_state', (None, 0))[0] or 'N/A'}
        💵 Average: ${self.results.get('highest_tech_state', (None, 0))[1]:,.0f}
        
        📈 Experience Premium: ${self.results.get('experience_salary_slope', 0):,.0f}/year
        
        🏢 Top Non-Tech Industry: {self.results.get('highest_nontech_industry', (None, 0))[0] or 'N/A'}
        💵 Median: ${self.results.get('highest_nontech_industry', (None, 0))[1]:,.0f}
        
        ⚖️ Gender Gap: {self.results.get('gender_gap', 0):.1f}%
        
        🎓 Education Premium: {self.results.get('education_impact', (0, 0, 0))[2]:.1f}%
        
        📊 Total Records Analyzed: {len(self.analyzer.cleaned_df):,}
        🇺🇸 US Tech Workers: {len(self.analyzer.cleaned_df[
            (self.analyzer.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.analyzer.cleaned_df['is_tech_role'] == True) | 
             (self.analyzer.cleaned_df['is_tech_industry'] == True))
        ]):,}
        """
        
        ax.text(0.1, 0.9, summary_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))

if __name__ == "__main__":
    # Initialize analyzer and dashboard
    analyzer = SalaryDataAnalyzer("Ask A Manager Salary Survey 2021 (Responses) - Form Responses 1.tsv")
    dashboard = SalaryDashboard(analyzer)
    
    # Run analysis and create dashboard
    results = dashboard.run_analysis_and_visualize()
    
    print("\n" + "="*80)
    print("DASHBOARD CREATED: salary_analysis_dashboard.png")
    print("="*80)
