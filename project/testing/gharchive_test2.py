from gharchive import GHArchive
from datetime import datetime, timedelta
import pandas as pd

def download_filtered_events(
    start_date,
    end_date=None,
    event_types=None,
    repos=None,
    actors=None,
    max_rows=5000
):
    """
    Download and filter GitHub events using gharchive library
    
    Args:
        start_date: Start date string 'YYYY-MM-DD' or datetime object (with time)
        end_date: End date string 'YYYY-MM-DD' or datetime object (with time)
                  Default: same as start_date
        event_types: List of event types to filter (e.g., ['PushEvent', 'PullRequestEvent'])
        repos: List of repository names to filter (e.g., ['microsoft/vscode'])
        actors: List of GitHub usernames to filter
        max_rows: Maximum number of rows to download
    
    Returns:
        pandas DataFrame with filtered events
    
    Examples:
        # Using datetime with specific hours
        start = datetime(2024, 12, 19, 10, 0)  # 10 AM
        end = datetime(2024, 12, 19, 14, 0)    # 2 PM
        events = download_filtered_events(start, end)
        
        # Using date strings (defaults to full day)
        events = download_filtered_events('2024-12-19', '2024-12-20')
    """
    gh = GHArchive()
    
    # Convert string dates to datetime if needed (time defaults to 00:00:00)
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date and isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    elif end_date is None:
        end_date = start_date
    
    print(f"Downloading events from {start_date.date()} to {end_date.date()}")
    
    # Build filters - gharchive uses tuple format
    filters = []
    if event_types:
        # For multiple values, add multiple filter tuples
        for event_type in event_types:
            filters.append(('type', event_type))
        print(f"Filtering for event types: {event_types}")
    if repos:
        for repo in repos:
            filters.append(('repo.name', repo))
        print(f"Filtering for repos: {repos}")
    if actors:
        for actor in actors:
            filters.append(('actor.login', actor))
        print(f"Filtering for actors: {actors}")
    
    # Convert to None if empty
    filter_list = filters if filters else None
    
    try:
        # Download data - returns Archive object
        archive = gh.get(
            start_date=start_date,
            end_date=end_date,
            filters=filter_list
        )
        
        # Convert Archive to DataFrame
        df = archive.to_df()
        
        # Limit rows if needed
        if len(df) > max_rows:
            print(f"Limiting from {len(df)} to {max_rows} events")
            df = df.head(max_rows)
        
        print(f"\nDownloaded {len(df)} events")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        return df
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        return pd.DataFrame()

def analyze_events(df):
    """Print summary statistics about the events"""
    if df.empty:
        print("No data to analyze")
        return
    
    print("\n" + "="*50)
    print("EVENT SUMMARY")
    print("="*50)
    
    # Event type breakdown
    if 'type' in df.columns:
        print("\nEvent Types:")
        print(df['type'].value_counts())
    
    # Top repositories
    if 'repo.name' in df.columns:
        print("\nTop 10 Repositories:")
        print(df['repo.name'].value_counts().head(10))
    
    # Top actors
    if 'actor.login' in df.columns:
        print("\nTop 10 Contributors:")
        print(df['actor.login'].value_counts().head(10))
    
    # Date range
    if 'created_at' in df.columns:
        print(f"\nDate range: {df['created_at'].min()} to {df['created_at'].max()}")

def save_to_file(df, filename, format='csv'):
    """Save DataFrame to file"""
    if df.empty:
        print("No data to save")
        return
    
    if format == 'csv':
        df.to_csv(filename, index=False)
    elif format == 'json':
        df.to_json(filename, orient='records', indent=2)
    elif format == 'parquet':
        df.to_parquet(filename, index=False)
    
    print(f"\nSaved {len(df)} events to {filename}")

# Example 1: Using datetime strings directly
if __name__ == "__main__":
    print("Example 1: Using datetime strings with time")
    print("-" * 50)
    
    # You can pass datetime strings directly!
    # Format: 'YYYY-MM-DD HH:MM:SS' (note: HH not hh)
    start_str = '2024-12-18'  # 10 AM
    end_str = '2024-12-19'    # 2 PM
    
    print(f"Fetching events from {start_str} to {end_str}")
    
    events = download_filtered_events(
        start_date=start_str,
        end_date=end_str,
        event_types=['PushEvent', 'PullRequestEvent'],
        max_rows=1000
    )
    
    analyze_events(events)
    
    if not events.empty:
        save_to_file(events, 'github_events_timerange.csv', format='csv')
    
    print("\n" + "="*50)
    print("Example 2: Alternative datetime string formats")
    print("-" * 50)
    
    # These all work! gharchive is flexible with datetime parsing
    formats_to_try = [
        '2024-12-19 12:00:00',      # Standard format
        '2024-12-19 12:30',          # Without seconds
        '2024-12-19T12:00:00',       # ISO format with T
        '12/19/2024 12:00:00',       # US format
    ]
    
    print("Testing different datetime string formats...")
    for fmt in formats_to_try:
        try:
            # Convert to datetime to test if it works
            if 'T' in fmt:
                dt = datetime.fromisoformat(fmt)
            elif '/' in fmt:
                dt = datetime.strptime(fmt, '%m/%d/%Y %H:%M:%S')
            else:
                parts = fmt.split()
                if len(parts) == 2 and ':' in parts[1]:
                    time_parts = parts[1].split(':')
                    if len(time_parts) == 2:
                        dt = datetime.strptime(fmt, '%Y-%m-%d %H:%M')
                    else:
                        dt = datetime.strptime(fmt, '%Y-%m-%d %H:%M:%S')
            print(f"✓ '{fmt}' → {dt}")
        except Exception as e:
            print(f"✗ '{fmt}' → Error: {e}")
    
    print("\n" + "="*50)
    print("Example 3: Simple hourly query")
    print("-" * 50)
    
    # For hourly data, just specify the hour
    hourly_events = download_filtered_events(
        start_date='2024-12-18',  # 3 PM
        end_date='2024-12-19',    # End of that hour
        repos=['python/cpython'],
        max_rows=200
    )
    
    analyze_events(hourly_events)