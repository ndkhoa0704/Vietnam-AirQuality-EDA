# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# %%
df = pd.read_csv('./data/historical_air_quality_2021_en.csv')

# %%
# Remove empty rows
df = df.dropna(axis=0, how='all')
# Replace unwanted characters
df = df.replace('-', np.nan)

# %%
# Remove unused columns
t = df.isna().sum()
to_be_removed = ['Station ID', 'Url', 'Status', 'Alert level', 'Data Time Tz']
## Select columns whose number of nan is higher than the number of data
for i in t.index:
    if t[i] > df.shape[0]/2:
        to_be_removed.append(i)
df = df.drop(columns=to_be_removed)
del t

# %%
# Split location to long and lat
t = df['Location'].str.split(',')
df['Latitude'] = t.apply(lambda x: x[0])
df['Longitude'] = t.apply(lambda x: x[1])
df = df.drop(columns='Location')
del t
# Conver data type 
df['Pressure'] = df['Pressure'].str.replace(',', '')
features = ['AQI index', 'CO', 'Dew', 
'Humidity', 'NO2', 'Pressure', 
'PM10', 'PM2.5', 'Temperature', 'Wind',
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


