# TechSalary Insights - Interactive Streamlit Dashboard

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**

   ```bash
   streamlit run streamlit_dashboard.py
   ```

3. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, click the link in your terminal

## 📊 Dashboard Features

### Interactive Filters

- **Country Selection**: Filter by country (US, UK, Canada, etc.)
- **State Selection**: For US data, filter by specific states
- **Industry Filter**: Focus on specific industries
- **Tech Roles Only**: Toggle to show only technology-related positions
- **Gender Filter**: Analyze by gender (Man, Woman, All)
- **Salary Range**: Interactive slider to filter salary ranges

### Analysis Tabs

#### 1. 💰 Salary Analysis

- Interactive salary distribution histogram
- Median salary line overlay
- Statistical summary (mean, median, quartiles)
- Real-time updates based on filters

#### 2. 📊 Industry Comparison

- Top 10 industries by median salary
- Horizontal bar chart for easy comparison
- Industry-specific insights

#### 3. 🌍 Geographic Analysis

- Top 10 US states by average salary
- Geographic salary patterns
- Location-based recommendations

#### 4. ⚖️ Gender Analysis

- Gender pay gap visualization
- Median salary comparison by gender
- Gap percentage calculation

#### 5. 📈 Experience Correlation

- Scatter plot of experience vs salary
- Trend line showing salary growth
- Color-coded by gender
- Interactive hover data

#### 6. 💡 Dynamic Insights

- Real-time insights based on current filters
- Personalized recommendations
- Key statistics and correlations

### Key Performance Indicators (KPIs)

- Total records processed
- US tech workers count
- Median tech salary
- Gender pay gap percentage

## 🔧 Technical Details

### Data Processing

- **Caching**: Data is cached for fast loading
- **Real-time Filtering**: All visualizations update instantly
- **Error Handling**: Graceful handling of missing data
- **Performance**: Optimized for large datasets

### Visualization Libraries

- **Plotly**: Interactive charts with hover details
- **Streamlit**: Modern web interface
- **Custom CSS**: Professional styling

### Data Sources

- Ask A Manager 2021 Salary Survey
- 28,062 survey responses
- 27,873 valid salary records after cleaning

## 📱 Usage Tips

### Getting Started

1. **Start with Overview**: Begin with all filters set to "All" to see the full dataset
2. **Use Filters Gradually**: Apply filters one at a time to understand their impact
3. **Compare Scenarios**: Use different filter combinations to compare groups
4. **Explore Tabs**: Each tab provides different insights - explore them all

### Best Practices

- **Sample Size**: Pay attention to sample sizes in insights
- **Correlation vs Causation**: Remember that correlations don't imply causation
- **Filter Combinations**: Some filter combinations may result in small sample sizes

### Common Use Cases

- **Salary Benchmarking**: Compare your role/industry against market data
- **Location Analysis**: Understand geographic salary variations
- **Career Planning**: Use experience correlation to plan career growth
- **Gender Equity**: Analyze and address pay gaps

## 🐛 Troubleshooting

### Common Issues

**App won't start:**

```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Data not loading:**

- Ensure `Ask A Manager Salary Survey 2021 (Responses) - Form Responses 1.tsv` is in the same directory
- Check file permissions

**Slow performance:**

- The app uses caching - first load may be slower
- Try reducing filter ranges for faster updates

**Empty charts:**

- Check that your filter combinations have data
- Try resetting filters to "All"

### Getting Help

- Check the console for error messages
- Ensure all required files are present
- Verify Python and package versions

## 📈 Sample Insights

### Key Findings from the Data

- **Software Engineer Median**: $132,860 (US)
- **Highest Paying State**: California ($144,338 average)
- **Experience Premium**: $1,576 per year in tech
- **Gender Gap**: 31.6% in tech roles
- **Education Premium**: 7.7% for Master's vs Bachelor's

### Business Applications

- **Compensation Planning**: Set competitive salary ranges
- **Market Analysis**: Understand industry and geographic trends
- **Diversity & Inclusion**: Identify and address pay gaps
- **Career Development**: Plan experience and education investments

## 🔮 Future Enhancements

Potential improvements for the dashboard:

- Export functionality for filtered data
- Advanced statistical analysis
- Salary prediction models
- Industry trend analysis over time
- Custom report generation

---

**Built with ❤️ using Streamlit, Pandas, and Plotly**
