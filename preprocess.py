# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv('./data/historical_air_quality_2021_en.csv')

# %%
# Remove empty rows
df = df[df.sum(axis=1) != 0]
# Remove unused columns
df = df.drop(columns=['Station ID', 'Url', 'Status', 'Alert level', 'Data Time Tz'])
# Replace unwanted characters
df = df.replace('-', np.nan)
# Split location to long and lat
t = df['Location'].str.split(',')
df['Longitude'] = t.apply(lambda x: x[0])
df['Latitude'] = t.apply(lambda x: x[1])
df = df.drop(columns='Location')
del t
# Conver data type 
df['Pressure'] = df['Pressure'].str.replace(',', '')
features = ['AQI index', 'CO', 'Dew', 
'Humidity', 'NO2', 'O3', 'Pressure', 
'PM10', 'PM2.5', 'SO2', 'Temperature', 'Wind',
'Longitude', 'Latitude']
df[features] = df[features].astype('float64')
# Fill nan by median
df[features[1:]] = df[features[1:]].apply(lambda x: x.fillna(x.median()), axis=0)
# Drop rows with unknown AQI index
df = df[~df['AQI index'].isna()]
# Drop unknown pollutant
df = df[df['Dominent pollutant'] != 'aqi']
df = df[~df['Dominent pollutant'].isna()]

# %%
# Add status
def status(x):
    if 0 <= x <= 50:
        return 'Good'
    if 51 <= x <= 100:
        return 'Moderate'
    if 101 <= x <= 150:
        return 'Unhealthy for sensitive groups'
    if 151 <= x <= 200:
        return 'Unhealthy'
    if 201 <= x <= 300:
        return 'Very unhealthy'
    if 301 <= x:
        return 'Hazardous'
df['Status'] = df['AQI index'].apply(status)

# %%
df.to_csv('./data/processed.csv', index=False)


