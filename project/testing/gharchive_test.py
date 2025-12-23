from datetime import datetime, timedelta
from gharchive import GHArchive
import pandas as pd

gh = GHArchive()

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

start = datetime(2017, 8, 19, 9, 0)  # 09 AM
end = datetime(2017, 8, 19, 17, 0)    # 5 PM


data = gh.get(start, end, filters=[('repo.name', 'torvalds/linux')] )

df = data.to_df()

save_to_file(df, 'github_events.csv', format='csv')