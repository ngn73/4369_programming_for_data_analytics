from github import Github, RateLimitExceededException, Auth
import pandas as pd
from datetime import datetime, timedelta
import time
import os



# Get the token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
output_results = []
#Search for repositories by language within a date range using PyGithub.Returns the total count of repositories.
def search_repos_by_language_and_date(g, language, start_date, end_date):
    try:
        # Build the search query
        query = f"language:{language} created:{start_date}..{end_date}"
        
        # Search repositories
        result = g.search_repositories(query=query)
        
        # Get total count
        total_count = result.totalCount
        
        return total_count
        
    except RateLimitExceededException:
        output_results.append(f"    Rate limit exceeded. Waiting...")
        # Get rate limit reset time
        rate_limit = g.get_rate_limit()
        reset_time = rate_limit.search.reset
        sleep_time = (reset_time - datetime.utcnow()).total_seconds() + 10
        
        if sleep_time > 0:
            output_results.append(f"    Sleeping for {sleep_time:.0f} seconds...")
            time.sleep(sleep_time)
        
        # Retry after waiting
        return search_repos_by_language_and_date(g, language, start_date, end_date)
        
    except Exception as e:
        output_results.append(f"    Exception occurred: {e}")
        return None
    

# A github rate limit is a restriction on how many requests you can make to GitHub's API within a certain time period
def check_rate_limit(g):
    rate_limit = g.get_rate_limit()
    output_results.append(f"Rate Limit Status:")
    output_results.append(f"   Core API - Remaining: {rate_limit.resources.core.remaining}/{rate_limit.resources.core.limit}")
    output_results.append(f"   Search API - Remaining: {rate_limit.resources.search.remaining}/{rate_limit.resources.search.limit}")
    
    return rate_limit.resources.search.remaining


#Collect repository creation data for multiple languages over time.
def collect_language_data(languages, start_year, end_year, frequency='quarterly'):
    # Initialize PyGithub
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    
    # Verify authentication
    try:
        user = g.get_user()
        output_results.append(f"Authenticated as: {user.login}")
    except Exception as e:
        output_results.append(f"Authentication failed: {e}")
        return None
    
    # Check initial rate limit
    check_rate_limit(g)
    
    results = []
    
    # Generate date ranges based on frequency
    if frequency == 'monthly':
        periods = generate_monthly_periods(start_year, end_year)
    else:  # yearly
        periods = generate_yearly_periods(start_year, end_year)
    
    total_requests = len(languages) * len(periods)
    current_request = 0
    
    output_results.append(f"\nCollecting data for {len(languages)} languages across {len(periods)} time periods...")
    output_results.append(f"   Total API calls needed: {total_requests}\n")
    
    for language in languages:
        output_results.append(f"\nProcessing {language}...")
        
        for period_name, start_date, end_date in periods:
            current_request += 1
            output_results.append(f"  [{current_request}/{total_requests}] {period_name}...")
            
            count = search_repos_by_language_and_date(g, language, start_date, end_date)
            
            if count is not None:
                results.append({
                    'language': language,
                    'period': period_name,
                    'start_date': start_date,
                    'end_date': end_date,
                    'repo_count': count
                })
                output_results.append(f"{count:,} repos")
            else:
                output_results.append("Failed")
            
            # Small delay to be nice to the API
            time.sleep(2)
            
            # Check rate limit every 10 requests
            if current_request % 10 == 0:
                remaining = check_rate_limit(g)
                if remaining < 5:
                    output_results.append("Rate limit getting low, slowing down...")
                    time.sleep(5)
    
    # Final rate limit check
    output_results.append("\n" + "="*50)
    check_rate_limit(g)
    
    return pd.DataFrame(results)

#Generate a List of monthly date ranges between start_year and end_year.
def generate_monthly_periods(start_year, end_year):
    periods = []
    current = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    
    while current <= end:
        # Calculate end of month
        if current.month == 12:
            next_month = datetime(current.year + 1, 1, 1)
        else:
            next_month = datetime(current.year, current.month + 1, 1)
        
        end_of_month = next_month - timedelta(days=1)
        
        if end_of_month > end:
            end_of_month = end
        
        period_name = current.strftime("%Y-%m")
        periods.append((period_name, current.strftime("%Y-%m-%d"), end_of_month.strftime("%Y-%m-%d")))
        
        current = next_month
    
    return periods

#Generate a list of yearly date ranges between start_year and end_year.
def generate_yearly_periods(start_year, end_year):
    periods = []
    
    for year in range(start_year, end_year + 1):
        period_name = str(year)
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        periods.append((period_name, start_date, end_date))
    
    return periods

# Main execution
if __name__ == "__main__":
    output_results.append("="*50)
    output_results.append("GitHub Language Trends Data Collector")
    output_results.append("Using PyGithub")
    output_results.append("="*50)
    
    # Define the languages tracked
    languages = [
        'Python', 'JavaScript', 'Java', 'TypeScript', 'C++'
        #'C', 'C#', 'Go', 'Rust', 'Ruby',
        #'PHP', 'Swift', 'Kotlin', 'R', 'Dart'
    ]
    
    # Set the date range
    START_YEAR = 2020
    END_YEAR = 2024
    
    # Choose frequency: 'monthly' or 'yearly'
    FREQUENCY = 'monthly'
    
    output_results.append(f"\nConfiguration:")
    output_results.append(f"   Languages: {len(languages)}")
    output_results.append(f"   Date Range: {START_YEAR} - {END_YEAR}")
    output_results.append(f"   Frequency: {FREQUENCY}")
    
    # Collect the data
    df = collect_language_data(languages, START_YEAR, END_YEAR, FREQUENCY)
    
    if df is not None and not df.empty:
        # Save to CSV
        output_file = f"github_language_trends_{START_YEAR}_{END_YEAR}_{FREQUENCY}.csv"
        df.to_csv(output_file, index=False)
        
        output_results.append("\n" + "="*50)
        output_results.append("Data collection complete!")
        output_results.append(f"Saved to: {output_file}")
        output_results.append(f"Total records: {len(df)}")
        
        # Display preview
        output_results.append("\nPreview of data:")
        output_results.append(df.head(10))
        
        # Show summary statistics
        output_results.append("\nSummary by language (total repos across all periods):")
        summary = df.groupby('language')['repo_count'].sum().sort_values(ascending=False)
        output_results.append(summary)
        
        output_results.append("\nNext steps:")
        output_results.append("   1. Open the CSV file in Excel or Python")
        output_results.append("   2. Create visualizations (line charts, bar charts)")
        output_results.append("   3. Analyze trends and patterns")
        output_results.append("="*50)
    else:
        output_results.append("\nData collection failed. Please check your token and try again.")
    
    # Write to file (each item on a new line)
    with open("Github_REST_API_Results.txt", "w") as f:
        for item in output_results:
            f.write(item + "\n")

    print("List written to file Github_REST_API_Results.txt")