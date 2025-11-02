import pandas as pd
import seaborn as sns
import pandas as pd
import seaborn as sns

url = "https://cli.fusio.net/cli/climate_data/webdata/hly4935.csv"
columns = ['date','wdsp']
df = pd.read_csv(url, usecols=columns, skiprows=23)
# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y %H:%M', errors='coerce')

# Filter by a specific year (2024) ... Plotting all years taking too long
year = 2024
df_year = df[df['date'].dt.year == year]
#sns.lineplot(data=df_year, x='date', y='wdsp').set_title(f'Mean Wind Speed Data for {year}')

#Output to CSV for testing
df.to_csv('testdata.csv', index=True)