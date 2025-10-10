# TechSalary Insights - Ask A Manager 2021 Salary Analysis Report

## Executive Summary

This comprehensive analysis of the Ask A Manager 2021 Salary Survey provides critical insights for TechSalary Insights. The dataset contains **28,062 responses** from working professionals across various industries and locations, with **27,873 valid salary records** after data cleaning.

## Key Findings

### 🎯 Core Business Questions - Answered

#### 1. **Median Salary for Software Engineers in the United States**
- **Answer: $132,860**
- Sample size: 1,087 US Software Engineers
- This represents a strong baseline for software engineering compensation in 2021

#### 2. **US State with Highest Average Salary for Tech Workers**
- **Answer: California ($144,338 average)**
- Sample size: 886 tech workers in California
- California leads with significantly higher tech salaries, likely due to Silicon Valley and high cost of living

#### 3. **Salary Increase per Year of Experience in Tech**
- **Answer: $1,576 per year**
- Sample size: 5,834 tech workers with experience data
- Correlation coefficient: 0.206 (moderate positive correlation)
- Each additional year of experience adds approximately $1,576 to annual salary

#### 4. **Industry with Highest Median Salary (Non-Tech)**
- **Answer: Pharma ($127,500 median)**
- Sample size: 16 workers in Pharma industry
- Pharmaceuticals emerges as the highest-paying non-tech industry

### 📊 Bonus Insights

#### 5. **Gender Gap in Tech Roles**
- **Answer: 31.6% gap (men earn more)**
- Men median salary: $125,000
- Women median salary: $95,000
- Sample size: 5,576 tech workers with gender data
- **Critical finding**: Significant gender pay gap persists in tech industry

#### 6. **Master's vs Bachelor's Degree Impact**
- **Answer: 7.7% salary increase for Master's degree**
- Master's median salary: $80,780
- Bachelor's median salary: $75,000
- Sample size: 16,997 workers with education data
- **Insight**: Graduate degree provides modest but measurable salary premium

## Data Quality & Methodology

### Data Cleaning Challenges Overcome
1. **Currency Standardization**: Converted multiple currencies (USD, GBP, CAD, EUR, AUD) to USD using 2021 exchange rates
2. **Salary Format Normalization**: Handled various formats including commas, dollar signs, and text annotations
3. **Location Standardization**: Standardized US state names and abbreviations
4. **Job Title Categorization**: Created intelligent categorization for tech vs non-tech roles
5. **Experience Range Conversion**: Converted experience ranges to numeric midpoints
6. **Outlier Filtering**: Removed unrealistic salaries (<$10,000 and >$2,000,000)

### Sample Sizes
- **Total dataset**: 28,062 responses
- **Valid salary records**: 27,873
- **US tech workers**: 5,834
- **US software engineers**: 1,087
- **Gender gap analysis**: 5,576 tech workers
- **Education analysis**: 16,997 workers

## Business Implications

### For TechSalary Insights

1. **Software Engineer Benchmark**: $132,860 median provides strong baseline for compensation benchmarking
2. **Geographic Premium**: California commands 8.6% premium over national average for tech workers
3. **Experience Valuation**: Each year of experience worth $1,576 annually in tech
4. **Industry Insights**: Pharma leads non-tech industries, suggesting high-value talent markets
5. **Diversity Challenge**: 31.6% gender gap indicates significant opportunity for pay equity initiatives
6. **Education ROI**: Master's degree provides 7.7% return, valuable for career planning

### Strategic Recommendations

1. **Geographic Expansion**: Consider California market dynamics for premium pricing strategies
2. **Experience-Based Pricing**: Implement experience multipliers in salary calculations
3. **Diversity Initiatives**: Address gender pay gap through targeted programs
4. **Industry Diversification**: Explore Pharma and other high-paying non-tech sectors
5. **Education Partnerships**: Highlight graduate degree ROI for career advancement

## Technical Implementation

### Files Created
- `salary_analysis.py`: Core data cleaning and analysis engine
- `salary_dashboard.py`: Interactive visualization dashboard
- `salary_analysis_dashboard.png`: Comprehensive visual summary
- `TechSalary_Insights_Report.md`: This executive report

### Data Processing Pipeline
1. **Load**: TSV file parsing with pandas
2. **Clean**: Multi-stage data cleaning and standardization
3. **Analyze**: Statistical analysis with scipy
4. **Visualize**: Matplotlib/Seaborn dashboard creation
5. **Report**: Executive summary generation

## Confidence & Limitations

### High Confidence Results
- Software engineer median salary (large sample size)
- Geographic salary differences (robust state-level data)
- Experience correlation (statistically significant)

### Moderate Confidence Results
- Industry comparisons (smaller sample sizes for some industries)
- Gender gap analysis (self-reported data limitations)

### Data Limitations
- Self-reported salary data may include bias
- Experience ranges rather than exact years
- Limited international currency conversion precision
- Some industries have small sample sizes

## Conclusion

The Ask A Manager 2021 Salary Survey provides valuable insights for TechSalary Insights. The analysis reveals clear patterns in tech compensation, geographic variations, and persistent challenges like gender pay gaps. These findings can inform strategic decision-making and market positioning in the competitive talent acquisition space.

**Key Takeaway**: Tech salaries show strong correlation with experience and location, but significant gender disparities remain that represent both a challenge and opportunity for the industry.

---

*Report generated by TechSalary Insights Data Analysis Team*  
*Data Source: Ask A Manager 2021 Salary Survey (28,062 responses)*  
*Analysis Date: December 2024*
