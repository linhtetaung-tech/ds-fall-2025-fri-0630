#!/usr/bin/env python3
"""
NYC Licensed Dog Data Downloader

This script downloads data from the NYC Open Data API for licensed dogs
with support for various query parameters and filtering options.

API Endpoint: https://data.cityofnewyork.us/resource/nu7n-tubp.csv

Author: Bryan
Date: 2024
"""

import requests
import pandas as pd
import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import json
import os


class NYCDogDataDownloader:
    """Download and process NYC Licensed Dog Data from Open Data API."""

    def __init__(self, base_url: str = "https://data.cityofnewyork.us/resource/nu7n-tubp.csv"):
        """
        Initialize the downloader.

        Args:
            base_url: Base URL for the NYC Open Data API endpoint
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NYC-Dog-Data-Analyzer/1.0',
            'Accept': 'text/csv, application/json'
        })

    def build_query_params(self,
                           limit: Optional[int] = None,
                           offset: Optional[int] = None,
                           where: Optional[str] = None,
                           order: Optional[str] = None,
                           select: Optional[str] = None,
                           custom_params: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Build query parameters for the API request.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            where: SQL WHERE clause for filtering
            order: SQL ORDER BY clause for sorting
            select: SQL SELECT clause for specific columns
            custom_params: Additional custom parameters

        Returns:
            Dictionary of query parameters
        """
        params = {}

        if limit is not None:
            params['$limit'] = str(limit)

        if offset is not None:
            params['$offset'] = str(offset)

        if where:
            params['$where'] = where

        if order:
            params['$order'] = order

        if select:
            params['$select'] = select

        if custom_params:
            params.update(custom_params)

        return params

    def download_data(self,
                      params: Optional[Dict[str, str]] = None,
                      output_file: Optional[str] = None,
                      format: str = 'csv') -> Union[pd.DataFrame, str]:
        """
        Download data from the NYC Open Data API.

        Args:
            params: Query parameters for the API request
            output_file: Optional file path to save the data
            format: Output format ('csv' or 'json')

        Returns:
            DataFrame if format='csv', JSON string if format='json'
        """
        try:
            # Make the API request
            response = self.session.get(
                self.base_url, params=params, timeout=30)
            response.raise_for_status()

            if format.lower() == 'csv':
                # Read CSV data into DataFrame
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))

                if output_file:
                    df.to_csv(output_file, index=False)
                    print(f"Data saved to {output_file}")

                return df

            elif format.lower() == 'json':
                # Return JSON string
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(response.text)
                    print(f"Data saved to {output_file}")

                return response.text

            else:
                raise ValueError("Format must be 'csv' or 'json'")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading data: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def get_data_info(self) -> Dict:
        """
        Get information about the dataset.

        Returns:
            Dictionary with dataset information
        """
        try:
            # Get metadata about the dataset
            metadata_url = "https://data.cityofnewyork.us/api/views/nu7n-tubp"
            response = self.session.get(metadata_url)
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print(f"Error getting dataset info: {e}")
            return {}

    def filter_by_date_range(self,
                             start_date: str,
                             end_date: str,
                             date_field: str = 'licenseissueddate') -> str:
        """
        Create a WHERE clause for date range filtering.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            date_field: Field name to filter on

        Returns:
            SQL WHERE clause string
        """
        return f"{date_field} between '{start_date}T00:00:00.000' and '{end_date}T23:59:59.999'"

    def filter_by_zipcode(self, zipcodes: List[str]) -> str:
        """
        Create a WHERE clause for zipcode filtering.

        Args:
            zipcodes: List of zipcodes to filter by

        Returns:
            SQL WHERE clause string
        """
        zipcode_list = "', '".join(zipcodes)
        return f"zipcode in ('{zipcode_list}')"

    def filter_by_breed(self, breeds: List[str]) -> str:
        """
        Create a WHERE clause for breed filtering.

        Args:
            breeds: List of breeds to filter by

        Returns:
            SQL WHERE clause string
        """
        breed_list = "', '".join(breeds)
        return f"breedname in ('{breed_list}')"

    def filter_by_gender(self, gender: str) -> str:
        """
        Create a WHERE clause for gender filtering.

        Args:
            gender: Gender to filter by ('M' or 'F')

        Returns:
            SQL WHERE clause string
        """
        return f"animalgender = '{gender}'"

    def get_expiring_licenses(self, days_ahead: int = 30) -> str:
        """
        Create a WHERE clause for licenses expiring within specified days.

        Args:
            days_ahead: Number of days ahead to check for expiring licenses

        Returns:
            SQL WHERE clause string
        """
        future_date = (datetime.now() + timedelta(days=days_ahead)
                       ).strftime('%Y-%m-%d')
        return f"licenseexpireddate <= '{future_date}T23:59:59.999'"

    def get_sample_data(self, sample_size: int = 100) -> pd.DataFrame:
        """
        Get a sample of the data for testing purposes.

        Args:
            sample_size: Number of records to sample

        Returns:
            DataFrame with sample data
        """
        params = self.build_query_params(limit=sample_size)
        return self.download_data(params)


def main():
    """Main function to handle command line arguments and execute data download."""
    parser = argparse.ArgumentParser(
        description="Download NYC Licensed Dog Data from Open Data API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all data
  python download_data.py --output dog_data.csv
  
  # Download data for specific zipcodes
  python download_data.py --zipcodes 10001,10002 --output filtered_data.csv
  
  # Download data for specific breeds
  python download_data.py --breeds "Labrador Retriever","Golden Retriever" --output labs.csv
  
  # Download licenses expiring in next 30 days
  python download_data.py --expiring 30 --output expiring.csv
  
  # Download data from date range
  python download_data.py --start-date 2020-01-01 --end-date 2020-12-31 --output 2020_data.csv
  
  # Get sample data (100 records)
  python download_data.py --sample 100 --output sample.csv
  
  # Download with custom limit and offset
  python download_data.py --limit 1000 --offset 500 --output paginated.csv
        """
    )

    # Basic options
    parser.add_argument('--output', '-o',
                        help='Output file path (CSV format)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--limit', type=int,
                        help='Maximum number of records to download')
    parser.add_argument('--offset', type=int,
                        help='Number of records to skip')

    # Filtering options
    parser.add_argument('--zipcodes',
                        help='Comma-separated list of zipcodes to filter by')
    parser.add_argument('--breeds',
                        help='Comma-separated list of breeds to filter by')
    parser.add_argument('--gender', choices=['M', 'F'],
                        help='Filter by gender (M or F)')
    parser.add_argument('--start-date',
                        help='Start date for license issued date filter (YYYY-MM-DD)')
    parser.add_argument('--end-date',
                        help='End date for license issued date filter (YYYY-MM-DD)')
    parser.add_argument('--expiring', type=int,
                        help='Get licenses expiring within specified days')

    # Utility options
    parser.add_argument('--sample', type=int,
                        help='Download sample data with specified number of records')
    parser.add_argument('--info', action='store_true',
                        help='Show dataset information')
    parser.add_argument('--where',
                        help='Custom SQL WHERE clause')
    parser.add_argument('--order',
                        help='Custom SQL ORDER BY clause')
    parser.add_argument('--select',
                        help='Custom SQL SELECT clause for specific columns')

    args = parser.parse_args()

    # Initialize downloader
    downloader = NYCDogDataDownloader()

    # Show dataset info if requested
    if args.info:
        info = downloader.get_data_info()
        print("Dataset Information:")
        print(json.dumps(info, indent=2))
        return

    # Build query parameters
    params = {}

    # Handle sample data request
    if args.sample:
        df = downloader.get_sample_data(args.sample)
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Sample data saved to {args.output}")
        else:
            print(f"Sample data ({len(df)} records):")
            print(df.head())
        return

    # Build WHERE clause from various filters
    where_conditions = []

    if args.zipcodes:
        zipcode_list = [z.strip() for z in args.zipcodes.split(',')]
        where_conditions.append(downloader.filter_by_zipcode(zipcode_list))

    if args.breeds:
        breed_list = [b.strip() for b in args.breeds.split(',')]
        where_conditions.append(downloader.filter_by_breed(breed_list))

    if args.gender:
        where_conditions.append(downloader.filter_by_gender(args.gender))

    if args.start_date and args.end_date:
        where_conditions.append(downloader.filter_by_date_range(
            args.start_date, args.end_date))

    if args.expiring:
        where_conditions.append(
            downloader.get_expiring_licenses(args.expiring))

    if args.where:
        where_conditions.append(args.where)

    # Combine WHERE conditions
    if where_conditions:
        params['$where'] = ' AND '.join(where_conditions)

    # Add other parameters
    if args.limit:
        params['$limit'] = str(args.limit)

    if args.offset:
        params['$offset'] = str(args.offset)

    if args.order:
        params['$order'] = args.order

    if args.select:
        params['$select'] = args.select

    # Download data
    print("Downloading data from NYC Open Data API...")
    print(f"API Endpoint: {downloader.base_url}")

    if params:
        print("Query Parameters:")
        for key, value in params.items():
            print(f"  {key}: {value}")

    try:
        result = downloader.download_data(params, args.output, args.format)

        if args.format == 'csv' and not args.output:
            print(f"\nDownloaded {len(result)} records")
            print("\nFirst 5 records:")
            print(result.head())
            print(f"\nData shape: {result.shape}")
            print(f"\nColumns: {list(result.columns)}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
