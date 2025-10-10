# NYC Licensed Dog Data Downloader

This Python script downloads data from the [NYC Open Data API](https://data.cityofnewyork.us/resource/nu7n-tubp.csv) for licensed dogs with comprehensive filtering and query parameter support.

## Features

- **Flexible Data Download**: Download all data or filtered subsets
- **Query Parameter Support**: Full support for NYC Open Data API query parameters
- **Multiple Filtering Options**: Filter by zipcode, breed, gender, date ranges, and more
- **License Expiry Detection**: Find licenses expiring within specified days
- **Multiple Output Formats**: CSV and JSON support
- **Pagination Support**: Handle large datasets with limit/offset parameters
- **Error Handling**: Robust error handling and validation
- **Command Line Interface**: Easy-to-use CLI with comprehensive help

## Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):

```bash
chmod +x download_data.py
```

## Usage

### Basic Usage

```bash
# Download all data
python download_data.py --output dog_data.csv

# Get sample data (100 records)
python download_data.py --sample 100 --output sample.csv

# Show dataset information
python download_data.py --info
```

### Filtering Examples

```bash
# Filter by zipcodes
python download_data.py --zipcodes 10001,10002,10003 --output manhattan_dogs.csv

# Filter by breeds
python download_data.py --breeds "Labrador Retriever","Golden Retriever" --output labs.csv

# Filter by gender
python download_data.py --gender F --output female_dogs.csv

# Filter by date range
python download_data.py --start-date 2020-01-01 --end-date 2020-12-31 --output 2020_data.csv

# Get licenses expiring in next 30 days
python download_data.py --expiring 30 --output expiring_soon.csv
```

### Advanced Filtering

```bash
# Combine multiple filters
python download_data.py \
  --zipcodes 10001,10002 \
  --breeds "Labrador Retriever","Golden Retriever" \
  --gender M \
  --start-date 2020-01-01 \
  --end-date 2020-12-31 \
  --output filtered_data.csv

# Use custom SQL WHERE clause
python download_data.py --where "breedname like '%Labrador%'" --output labs.csv

# Use custom ORDER BY clause
python download_data.py --order "licenseissueddate desc" --output recent_licenses.csv

# Select specific columns only
python download_data.py --select "animalname,breedname,zipcode" --output selected_fields.csv
```

### Pagination

```bash
# Download first 1000 records
python download_data.py --limit 1000 --output first_1000.csv

# Download records 1001-2000
python download_data.py --limit 1000 --offset 1000 --output second_1000.csv
```

### Output Formats

```bash
# CSV format (default)
python download_data.py --output data.csv --format csv

# JSON format
python download_data.py --output data.json --format json
```

## Command Line Arguments

### Basic Options

- `--output`, `-o`: Output file path
- `--format`: Output format (csv or json, default: csv)
- `--limit`: Maximum number of records to download
- `--offset`: Number of records to skip

### Filtering Options

- `--zipcodes`: Comma-separated list of zipcodes
- `--breeds`: Comma-separated list of breeds
- `--gender`: Filter by gender (M or F)
- `--start-date`: Start date for license issued date filter (YYYY-MM-DD)
- `--end-date`: End date for license issued date filter (YYYY-MM-DD)
- `--expiring`: Get licenses expiring within specified days

### Utility Options

- `--sample`: Download sample data with specified number of records
- `--info`: Show dataset information
- `--where`: Custom SQL WHERE clause
- `--order`: Custom SQL ORDER BY clause
- `--select`: Custom SQL SELECT clause for specific columns

## Data Schema

Based on the [NYC Licensed Dog Dataset](https://data.cityofnewyork.us/resource/nu7n-tubp.csv), the data includes:

- `animalname`: Dog's name
- `animalgender`: Gender (M/F)
- `animalbirth`: Birth year
- `breedname`: Dog breed
- `zipcode`: Owner's zip code
- `licenseissueddate`: When license was issued
- `licenseexpireddate`: When license expires
- `extract_year`: Year data was extracted

## API Endpoint

The script uses the NYC Open Data API endpoint:

```
https://data.cityofnewyork.us/resource/nu7n-tubp.csv
```

## Error Handling

The script includes comprehensive error handling for:

- Network connectivity issues
- API rate limiting
- Invalid query parameters
- Data format errors
- File I/O errors

## Examples for Dashboard Questions

Here are specific examples for answering the analytical questions from your PRD:

### 1. Most Common Dog Names

```bash
python download_data.py --select "animalname" --order "animalname" --output names.csv
```

### 2. Oldest/Youngest Dogs

```bash
python download_data.py --order "animalbirth asc" --limit 10 --output oldest_dogs.csv
python download_data.py --order "animalbirth desc" --limit 10 --output youngest_dogs.csv
```

### 3. Most/Least Common Breeds

```bash
python download_data.py --select "breedname" --order "breedname" --output breeds.csv
```

### 4. Zipcodes with Most/Least Dogs

```bash
python download_data.py --select "zipcode" --order "zipcode" --output zipcodes.csv
```

### 5. Licenses Expiring Next Month

```bash
python download_data.py --expiring 30 --output expiring_next_month.csv
```

### 6. License Issuance Patterns

```bash
python download_data.py --select "licenseissueddate" --order "licenseissueddate" --output issuance_patterns.csv
```

## Troubleshooting

### Common Issues

1. **Network Timeout**: Increase timeout in the script or check internet connection
2. **Large Dataset**: Use `--limit` parameter to download data in chunks
3. **Invalid Date Format**: Use YYYY-MM-DD format for date parameters
4. **Special Characters**: Escape special characters in breed names or use quotes

### Performance Tips

- Use `--limit` for large datasets to avoid memory issues
- Use `--select` to download only needed columns
- Use specific filters to reduce data size
- Consider using `--offset` for pagination

## License

This script is provided as-is for educational and research purposes. Please respect the NYC Open Data API terms of service.
