import pandas as pd
import numpy as np
import os
import toml
import forecasting_tool

data_config = toml.load(os.path.join(os.getcwd(), "../configuration.toml"))



# input
county_roads = pd.read_csv(data_config['input_county_roads_revenue'])
# forecast result
county_roads_result = pd.DataFrame()

# County Road Levy: revenue = Prior year revenue × 1.01
df_forecast = county_roads.loc[county_roads['Revenue Type']=="County Road Levy"].copy()

counties = df_forecast['County'].unique().tolist()
for county in counties:
    df = df_forecast.loc[county_roads['County']==county].copy()

    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',1.01)

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)

# Other Federal Funds (highways):
# Estimate 2021 Revenue = (average 2016-2020 revenue) × 1.025
# Prior year estimate × 1.025
df_forecast = county_roads.loc[county_roads['Revenue Type']=="Other Federal Funds (highways)"].copy()

counties = df_forecast['County'].unique().tolist()
for county in counties:
    df = df_forecast.loc[county_roads['County']==county].copy()

    last_actual_year = max(df['Year'])
    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])

    # average previous 5 years * 1.025 for the first forecast year
    df.loc[last_actual_year+1,'Value'] = df.loc[range(last_actual_year-4,last_actual_year+1),'Value'].mean()*1.025
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',1.025)

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)


1+1