#!/usr/bin/env python3
"""
Ask A Manager Salary Survey 2021 - Data Analysis
Real-world data cleaning challenge for TechSalary Insights
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class SalaryDataAnalyzer:
    def __init__(self, file_path: str):
        """Initialize the analyzer with the TSV file path."""
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None

    def load_data(self) -> pd.DataFrame:
        """Load the TSV data into a pandas DataFrame."""
        print("Loading data...")
        self.df = pd.read_csv(self.file_path, sep='\t')
        print(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        return self.df

    def clean_salary_data(self) -> pd.DataFrame:
        """Clean and standardize the salary data."""
        print("\nCleaning salary data...")
        df = self.df.copy()

        # Create a clean salary column
        df['salary_cleaned'] = df['What is your annual salary? (You\'ll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)'].astype(str)

        # Remove commas and convert to numeric
        df['salary_cleaned'] = df['salary_cleaned'].str.replace(
            ',', '').str.replace('$', '')

        # Handle various formats and convert to numeric
        def parse_salary(salary_str):
            if pd.isna(salary_str) or salary_str == 'nan' or salary_str == '':
                return np.nan

            # Remove common text patterns
            salary_str = str(salary_str).lower()
            salary_str = re.sub(r'[^\d.]', '', salary_str)

            try:
                return float(salary_str) if salary_str else np.nan
            except:
                return np.nan

        df['salary_numeric'] = df['salary_cleaned'].apply(parse_salary)

        # Convert to USD using approximate exchange rates (2021)
        exchange_rates = {
            'USD': 1.0,
            'GBP': 1.38,  # GBP to USD in 2021
            'CAD': 0.80,  # CAD to USD in 2021
            'EUR': 1.18,  # EUR to USD in 2021
            'AUD': 0.75,  # AUD to USD in 2021
        }

        def convert_to_usd(row):
            salary = row['salary_numeric']
            currency = str(row['Please indicate the currency']).upper()

            if pd.isna(salary) or salary == 0:
                return np.nan

            # Handle common currency variations
            if 'USD' in currency or 'US' in currency:
                return salary
            elif 'GBP' in currency or 'POUND' in currency:
                return salary * exchange_rates['GBP']
            elif 'CAD' in currency or 'CANADIAN' in currency:
                return salary * exchange_rates['CAD']
            elif 'EUR' in currency or 'EURO' in currency:
                return salary * exchange_rates['EUR']
            elif 'AUD' in currency or 'AUSTRALIAN' in currency:
                return salary * exchange_rates['AUD']
            else:
                return salary  # Assume USD if unknown

        df['salary_usd'] = df.apply(convert_to_usd, axis=1)

        # Filter out unrealistic salaries (too low or too high)
        df = df[(df['salary_usd'] >= 10000) & (df['salary_usd'] <= 2000000)]

        print(f"After cleaning: {len(df)} valid salary records")
        return df

    def clean_location_data(self) -> pd.DataFrame:
        """Clean and standardize location data."""
        print("\nCleaning location data...")
        df = self.cleaned_df.copy()

        # Clean country data
        df['country_cleaned'] = df['What country do you work in?'].astype(str)
        df['country_cleaned'] = df['country_cleaned'].str.upper()

        # Standardize US country names
        us_variations = ['US', 'USA', 'UNITED STATES',
                         'UNITED STATES OF AMERICA']
        df.loc[df['country_cleaned'].isin(
            us_variations), 'country_cleaned'] = 'UNITED STATES'

        # Clean state data
        df['state_cleaned'] = df['If you\'re in the U.S., what state do you work in?'].astype(
            str)
        df['state_cleaned'] = df['state_cleaned'].str.upper()

        # Standardize common state abbreviations and names
        state_mapping = {
            'DC': 'DISTRICT OF COLUMBIA',
            'D.C.': 'DISTRICT OF COLUMBIA',
            'WASHINGTON DC': 'DISTRICT OF COLUMBIA',
            'WASHINGTON, DC': 'DISTRICT OF COLUMBIA',
            'NEW YORK': 'NEW YORK',
            'NY': 'NEW YORK',
            'CALIFORNIA': 'CALIFORNIA',
            'CA': 'CALIFORNIA',
            'TEXAS': 'TEXAS',
            'TX': 'TEXAS',
            'FLORIDA': 'FLORIDA',
            'FL': 'FLORIDA',
            'ILLINOIS': 'ILLINOIS',
            'IL': 'ILLINOIS',
            'PENNSYLVANIA': 'PENNSYLVANIA',
            'PA': 'PENNSYLVANIA',
            'OHIO': 'OHIO',
            'OH': 'OHIO',
            'GEORGIA': 'GEORGIA',
            'GA': 'GEORGIA',
            'NORTH CAROLINA': 'NORTH CAROLINA',
            'NC': 'NORTH CAROLINA',
            'MICHIGAN': 'MICHIGAN',
            'MI': 'MICHIGAN',
            'NEW JERSEY': 'NEW JERSEY',
            'NJ': 'NEW JERSEY',
            'VIRGINIA': 'VIRGINIA',
            'VA': 'VIRGINIA',
            'WASHINGTON': 'WASHINGTON',
            'WA': 'WASHINGTON',
            'ARIZONA': 'ARIZONA',
            'AZ': 'ARIZONA',
            'MASSACHUSETTS': 'MASSACHUSETTS',
            'MA': 'MASSACHUSETTS',
            'TENNESSEE': 'TENNESSEE',
            'TN': 'TENNESSEE',
            'INDIANA': 'INDIANA',
            'IN': 'INDIANA',
            'MISSOURI': 'MISSOURI',
            'MO': 'MISSOURI',
            'MARYLAND': 'MARYLAND',
            'MD': 'MARYLAND',
            'WISCONSIN': 'WISCONSIN',
            'WI': 'WISCONSIN',
            'COLORADO': 'COLORADO',
            'CO': 'COLORADO',
            'MINNESOTA': 'MINNESOTA',
            'MN': 'MINNESOTA',
            'SOUTH CAROLINA': 'SOUTH CAROLINA',
            'SC': 'SOUTH CAROLINA',
            'ALABAMA': 'ALABAMA',
            'AL': 'ALABAMA',
            'LOUISIANA': 'LOUISIANA',
            'LA': 'LOUISIANA',
            'KENTUCKY': 'KENTUCKY',
            'KY': 'KENTUCKY',
            'OREGON': 'OREGON',
            'OR': 'OREGON',
            'OKLAHOMA': 'OKLAHOMA',
            'OK': 'OKLAHOMA',
            'CONNECTICUT': 'CONNECTICUT',
            'CT': 'CONNECTICUT',
            'UTAH': 'UTAH',
            'UT': 'UTAH',
            'IOWA': 'IOWA',
            'IA': 'IOWA',
            'NEVADA': 'NEVADA',
            'NV': 'NEVADA',
            'ARKANSAS': 'ARKANSAS',
            'AR': 'ARKANSAS',
            'MISSISSIPPI': 'MISSISSIPPI',
            'MS': 'MISSISSIPPI',
            'KANSAS': 'KANSAS',
            'KS': 'KANSAS',
            'NEW MEXICO': 'NEW MEXICO',
            'NM': 'NEW MEXICO',
            'NEBRASKA': 'NEBRASKA',
            'NE': 'NEBRASKA',
            'WEST VIRGINIA': 'WEST VIRGINIA',
            'WV': 'WEST VIRGINIA',
            'IDAHO': 'IDAHO',
            'ID': 'IDAHO',
            'HAWAII': 'HAWAII',
            'HI': 'HAWAII',
            'NEW HAMPSHIRE': 'NEW HAMPSHIRE',
            'NH': 'NEW HAMPSHIRE',
            'MAINE': 'MAINE',
            'ME': 'MAINE',
            'MONTANA': 'MONTANA',
            'MT': 'MONTANA',
            'RHODE ISLAND': 'RHODE ISLAND',
            'RI': 'RHODE ISLAND',
            'DELAWARE': 'DELAWARE',
            'DE': 'DELAWARE',
            'SOUTH DAKOTA': 'SOUTH DAKOTA',
            'SD': 'SOUTH DAKOTA',
            'NORTH DAKOTA': 'NORTH DAKOTA',
            'ND': 'NORTH DAKOTA',
            'ALASKA': 'ALASKA',
            'AK': 'ALASKA',
            'VERMONT': 'VERMONT',
            'VT': 'VERMONT',
            'WYOMING': 'WYOMING',
            'WY': 'WYOMING',
        }

        df['state_cleaned'] = df['state_cleaned'].map(
            state_mapping).fillna(df['state_cleaned'])

        return df

    def clean_job_data(self) -> pd.DataFrame:
        """Clean and categorize job titles."""
        print("\nCleaning job data...")
        df = self.cleaned_df.copy()

        # Clean job titles
        df['job_title_cleaned'] = df['Job title'].astype(str).str.lower()

        # Identify software engineers and tech roles
        software_engineer_keywords = [
            'software engineer', 'software developer', 'programmer', 'developer',
            'software architect', 'software lead', 'senior software', 'principal software',
            'staff software', 'software specialist', 'software analyst'
        ]

        tech_keywords = [
            'software', 'developer', 'engineer', 'programmer', 'analyst', 'architect',
            'data scientist', 'data engineer', 'devops', 'sre', 'site reliability',
            'product manager', 'technical', 'systems', 'network', 'security',
            'machine learning', 'ml engineer', 'ai engineer', 'backend', 'frontend',
            'full stack', 'mobile developer', 'ios', 'android', 'web developer',
            'cloud engineer', 'platform engineer', 'infrastructure'
        ]

        # Create boolean flags for categorization
        df['is_software_engineer'] = df['job_title_cleaned'].str.contains(
            '|'.join(software_engineer_keywords), case=False, na=False)
        df['is_tech_role'] = df['job_title_cleaned'].str.contains(
            '|'.join(tech_keywords), case=False, na=False)

        # Also check industry
        df['is_tech_industry'] = df['What industry do you work in?'].astype(
            str).str.contains('Computing or Tech|Technology|Software', case=False, na=False)

        return df

    def clean_experience_data(self) -> pd.DataFrame:
        """Clean experience data."""
        print("\nCleaning experience data...")
        df = self.cleaned_df.copy()

        # Convert experience ranges to numeric values (midpoint)
        def experience_to_years(exp_str):
            if pd.isna(exp_str):
                return np.nan

            exp_str = str(exp_str).lower()

            if '1 year or less' in exp_str:
                return 0.5
            elif '2 - 4 years' in exp_str:
                return 3
            elif '5-7 years' in exp_str or '5 - 7 years' in exp_str:
                return 6
            elif '8 - 10 years' in exp_str:
                return 9
            elif '11 - 20 years' in exp_str:
                return 15.5
            elif '21 - 30 years' in exp_str:
                return 25.5
            elif '31 - 40 years' in exp_str:
                return 35.5
            elif '41 years or more' in exp_str:
                return 45
            else:
                return np.nan

        df['years_experience_overall'] = df['How many years of professional work experience do you have overall?'].apply(
            experience_to_years)
        df['years_experience_field'] = df['How many years of professional work experience do you have in your field?'].apply(
            experience_to_years)

        return df

    def clean_demographics(self) -> pd.DataFrame:
        """Clean demographic data."""
        print("\nCleaning demographic data...")
        df = self.cleaned_df.copy()

        # Clean gender data
        df['gender_cleaned'] = df['What is your gender?'].astype(
            str).str.lower()
        df['gender_cleaned'] = df['gender_cleaned'].map({
            'man': 'Man',
            'woman': 'Woman',
            'non-binary': 'Non-binary',
            'nonbinary': 'Non-binary',
            'nan': np.nan
        }).fillna(df['gender_cleaned'])

        # Clean education data
        df['education_cleaned'] = df['What is your highest level of education completed?'].astype(
            str)

        return df

    def run_full_cleaning(self) -> pd.DataFrame:
        """Run the complete data cleaning pipeline."""
        print("Starting comprehensive data cleaning...")

        # Load data
        self.load_data()

        # Clean salary data
        self.cleaned_df = self.clean_salary_data()

        # Clean other data
        self.cleaned_df = self.clean_location_data()
        self.cleaned_df = self.clean_job_data()
        self.cleaned_df = self.clean_experience_data()
        self.cleaned_df = self.clean_demographics()

        print(
            f"\nData cleaning complete. Final dataset: {len(self.cleaned_df)} rows")
        return self.cleaned_df

    def analyze_software_engineer_salaries(self) -> float:
        """Question 1: Median salary for Software Engineers in the US."""
        print("\n" + "="*60)
        print("QUESTION 1: Median salary for Software Engineers in the US")
        print("="*60)

        # Filter for US software engineers
        us_software_engineers = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.cleaned_df['is_software_engineer'] == True) &
            (self.cleaned_df['salary_usd'].notna())
        ]

        median_salary = us_software_engineers['salary_usd'].median()

        print(f"US Software Engineers found: {len(us_software_engineers)}")
        print(f"Median salary: ${median_salary:,.0f}")

        return median_salary

    def find_highest_tech_state(self) -> Tuple[str, float]:
        """Question 2: US state with highest average salary for tech workers."""
        print("\n" + "="*60)
        print("QUESTION 2: US state with highest average salary for tech workers")
        print("="*60)

        # Filter for US tech workers
        us_tech_workers = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.cleaned_df['state_cleaned'].notna()) &
            ((self.cleaned_df['is_tech_role'] == True) | (self.cleaned_df['is_tech_industry'] == True)) &
            (self.cleaned_df['salary_usd'].notna())
        ]

        # Calculate average salary by state
        state_salaries = us_tech_workers.groupby('state_cleaned').agg({
            'salary_usd': ['mean', 'count']
        }).round(0)

        state_salaries.columns = ['avg_salary', 'count']
        # At least 5 workers
        state_salaries = state_salaries[state_salaries['count'] >= 5]

        highest_state = state_salaries.loc[state_salaries['avg_salary'].idxmax(
        )]
        state_name = state_salaries['avg_salary'].idxmax()

        print(f"States with tech workers analyzed: {len(state_salaries)}")
        print(f"Highest paying state: {state_name}")
        print(f"Average salary: ${highest_state['avg_salary']:,.0f}")
        print(f"Number of workers: {highest_state['count']}")

        return state_name, highest_state['avg_salary']

    def analyze_experience_salary_correlation(self) -> float:
        """Question 3: Salary increase per year of experience in tech."""
        print("\n" + "="*60)
        print("QUESTION 3: Salary increase per year of experience in tech")
        print("="*60)

        # Filter for US tech workers with experience data
        us_tech_with_exp = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.cleaned_df['is_tech_role'] == True) | (self.cleaned_df['is_tech_industry'] == True)) &
            (self.cleaned_df['salary_usd'].notna()) &
            (self.cleaned_df['years_experience_overall'].notna())
        ]

        # Calculate correlation and slope
        from scipy import stats
        correlation = stats.pearsonr(
            us_tech_with_exp['years_experience_overall'], us_tech_with_exp['salary_usd'])
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            us_tech_with_exp['years_experience_overall'], us_tech_with_exp['salary_usd'])

        print(f"Tech workers with experience data: {len(us_tech_with_exp)}")
        print(f"Correlation coefficient: {correlation[0]:.3f}")
        print(f"Salary increase per year: ${slope:,.0f}")

        return slope

    def find_highest_nontech_industry(self) -> Tuple[str, float]:
        """Question 4: Industry (besides tech) with highest median salary."""
        print("\n" + "="*60)
        print("QUESTION 4: Industry (besides tech) with highest median salary")
        print("="*60)

        # Filter for US workers, exclude tech industry
        us_nontech = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.cleaned_df['is_tech_industry'] == False) &
            (self.cleaned_df['salary_usd'].notna())
        ]

        # Calculate median salary by industry
        industry_salaries = us_nontech.groupby('What industry do you work in?').agg({
            'salary_usd': ['median', 'count']
        }).round(0)

        industry_salaries.columns = ['median_salary', 'count']
        # At least 10 workers
        industry_salaries = industry_salaries[industry_salaries['count'] >= 10]

        highest_industry = industry_salaries.loc[industry_salaries['median_salary'].idxmax(
        )]
        industry_name = industry_salaries['median_salary'].idxmax()

        print(f"Non-tech industries analyzed: {len(industry_salaries)}")
        print(f"Highest paying industry: {industry_name}")
        print(f"Median salary: ${highest_industry['median_salary']:,.0f}")
        print(f"Number of workers: {highest_industry['count']}")

        return industry_name, highest_industry['median_salary']

    def analyze_gender_gap_tech(self) -> float:
        """Question 5: Salary gap between men and women in tech roles."""
        print("\n" + "="*60)
        print("QUESTION 5: Salary gap between men and women in tech roles")
        print("="*60)

        # Filter for US tech workers with gender data
        us_tech_gender = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            ((self.cleaned_df['is_tech_role'] == True) | (self.cleaned_df['is_tech_industry'] == True)) &
            (self.cleaned_df['salary_usd'].notna()) &
            (self.cleaned_df['gender_cleaned'].isin(['Man', 'Woman']))
        ]

        # Calculate median salaries by gender
        gender_salaries = us_tech_gender.groupby(
            'gender_cleaned')['salary_usd'].median()

        men_median = gender_salaries.get('Man', 0)
        women_median = gender_salaries.get('Woman', 0)

        if men_median > 0 and women_median > 0:
            gap_percentage = ((men_median - women_median) / women_median) * 100
        else:
            gap_percentage = 0

        print(f"Tech workers with gender data: {len(us_tech_gender)}")
        print(f"Men median salary: ${men_median:,.0f}")
        print(f"Women median salary: ${women_median:,.0f}")
        print(f"Gender gap: {gap_percentage:.1f}% (men earn more)")

        return gap_percentage

    def analyze_education_impact(self) -> Tuple[float, float, float]:
        """Question 6: Master's vs Bachelor's degree salary comparison."""
        print("\n" + "="*60)
        print("QUESTION 6: Master's vs Bachelor's degree salary comparison")
        print("="*60)

        # Filter for US workers with education data
        us_with_education = self.cleaned_df[
            (self.cleaned_df['country_cleaned'] == 'UNITED STATES') &
            (self.cleaned_df['salary_usd'].notna()) &
            (self.cleaned_df['education_cleaned'].str.contains(
                'Master|College degree', case=False, na=False))
        ]

        # Categorize education levels
        us_with_education = us_with_education.copy()
        us_with_education['education_category'] = us_with_education['education_cleaned'].apply(
            lambda x: 'Master\'s' if 'master' in str(x).lower(
            ) else 'Bachelor\'s' if 'college' in str(x).lower() else 'Other'
        )

        # Calculate median salaries by education
        education_salaries = us_with_education.groupby('education_category')[
            'salary_usd'].median()

        masters_median = education_salaries.get('Master\'s', 0)
        bachelors_median = education_salaries.get('Bachelor\'s', 0)

        if masters_median > 0 and bachelors_median > 0:
            difference = masters_median - bachelors_median
            percentage_increase = (difference / bachelors_median) * 100
        else:
            difference = 0
            percentage_increase = 0

        print(f"Workers with education data: {len(us_with_education)}")
        print(f"Master's median salary: ${masters_median:,.0f}")
        print(f"Bachelor's median salary: ${bachelors_median:,.0f}")
        print(f"Difference: ${difference:,.0f}")
        print(f"Percentage increase: {percentage_increase:.1f}%")

        return masters_median, bachelors_median, percentage_increase

    def run_all_analyses(self):
        """Run all business questions and provide summary."""
        print("\n" + "="*80)
        print("TECHSALARY INSIGHTS - ASK A MANAGER 2021 SALARY ANALYSIS")
        print("="*80)

        # Run cleaning
        self.run_full_cleaning()

        # Run all analyses
        results = {}

        try:
            results['software_engineer_median'] = self.analyze_software_engineer_salaries()
        except Exception as e:
            print(f"Error in software engineer analysis: {e}")
            results['software_engineer_median'] = None

        try:
            state, salary = self.find_highest_tech_state()
            results['highest_tech_state'] = (state, salary)
        except Exception as e:
            print(f"Error in state analysis: {e}")
            results['highest_tech_state'] = None

        try:
            results['experience_salary_slope'] = self.analyze_experience_salary_correlation()
        except Exception as e:
            print(f"Error in experience analysis: {e}")
            results['experience_salary_slope'] = None

        try:
            industry, salary = self.find_highest_nontech_industry()
            results['highest_nontech_industry'] = (industry, salary)
        except Exception as e:
            print(f"Error in industry analysis: {e}")
            results['highest_nontech_industry'] = None

        try:
            results['gender_gap'] = self.analyze_gender_gap_tech()
        except Exception as e:
            print(f"Error in gender gap analysis: {e}")
            results['gender_gap'] = None

        try:
            masters, bachelors, increase = self.analyze_education_impact()
            results['education_impact'] = (masters, bachelors, increase)
        except Exception as e:
            print(f"Error in education analysis: {e}")
            results['education_impact'] = None

        # Summary
        print("\n" + "="*80)
        print("FINAL RESULTS SUMMARY")
        print("="*80)

        print(f"1. Median Software Engineer Salary (US): ${results['software_engineer_median']:,.0f}" if results[
              'software_engineer_median'] else "1. Software Engineer analysis failed")

        if results['highest_tech_state']:
            state, salary = results['highest_tech_state']
            print(f"2. Highest Paying Tech State: {state} (${salary:,.0f})")
        else:
            print("2. State analysis failed")

        print(f"3. Salary Increase per Year Experience: ${results['experience_salary_slope']:,.0f}" if results[
              'experience_salary_slope'] else "3. Experience analysis failed")

        if results['highest_nontech_industry']:
            industry, salary = results['highest_nontech_industry']
            print(
                f"4. Highest Paying Non-Tech Industry: {industry} (${salary:,.0f})")
        else:
            print("4. Industry analysis failed")

        print(
            f"5. Gender Gap in Tech: {results['gender_gap']:.1f}%" if results['gender_gap'] else "5. Gender gap analysis failed")

        if results['education_impact']:
            masters, bachelors, increase = results['education_impact']
            print(
                f"6. Master's vs Bachelor's: {increase:.1f}% increase (${masters:,.0f} vs ${bachelors:,.0f})")
        else:
            print("6. Education analysis failed")

        return results


if __name__ == "__main__":
    # Initialize analyzer
    analyzer = SalaryDataAnalyzer(
        "Ask A Manager Salary Survey 2021 (Responses) - Form Responses 1.tsv")

    # Run all analyses
    results = analyzer.run_all_analyses()
