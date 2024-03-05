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

# parameters needed in script
motor_fuel = pd.read_csv(data_config['input_tax_base'])
motor_fuel = motor_fuel[motor_fuel['Tax Base Category'] == 'Motor Fuel (gal.)'].set_index("Year")
# (Y regional fuel forecasts/Y-1 regional fuel forecasts)
motor_fuel['ratio'] = motor_fuel['Value']/motor_fuel['Value'].shift(1)

# annual incorporated area population in each county
subarea_pop = pd.read_csv(data_config['input_subarea_population_forecast'])
subarea_pop = subarea_pop[(subarea_pop['PopulationArea'] == 'Unincorp.')].set_index("Year")
subarea_pop['ratio'] = subarea_pop['Population']/subarea_pop['Population'].shift(1)

parameter = pd.read_csv(data_config['input_parameter']).set_index("Year")
# (Y regional fuel forecasts/Y-1 regional fuel forecasts)
parameter['CPI ratio'] = parameter['CPI']/parameter['CPI'].shift(1)

# single value
df_mul = pd.DataFrame({'multiply value 1.01': np.repeat(1.01, data_config['end_year']+1-county_roads['Year'].min()),
                       'multiply value 1.025': np.repeat(1.025, data_config['end_year']+1-county_roads['Year'].min())} , 
                       index=range(county_roads['Year'].min(), data_config['end_year']+1))

# forecasting
# County Road Levy: revenue = Prior year revenue × 1.01
df_forecast = county_roads.loc[county_roads['Revenue Type']=="County Road Levy"].copy()

counties = df_forecast['County'].unique().tolist()
for county in counties:
    df = df_forecast.loc[county_roads['County']==county].copy()

    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',df_mul['multiply value 1.01'])

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
    # first forecast year
    df.loc[last_actual_year+1,'Value'] = df.loc[range(last_actual_year-4,last_actual_year+1),'Value'].mean()*1.025
    # other forecast year
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',df_mul['multiply value 1.025'])

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)

# Other Federal Grants
# Estimate 2021 Revenue = (average 2016-2020 revenue) × 1.025
# Prior year estimate × 1.025
    
# different calculation in spreadsheet
# Estimate 2021 Revenue = (Y CPI/Y-1 CPI) * (average 2016-2020 revenue)
# Prior year estimate × (Y CPI/Y-1 CPI) 
df_forecast = county_roads.loc[county_roads['Revenue Type']=="Other Federal Grants"].copy()

counties = df_forecast['County'].unique().tolist()
for county in counties:
    df = df_forecast.loc[county_roads['County']==county].copy()

    last_actual_year = max(df['Year'])
    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])
    # first forecast year
    df.loc[last_actual_year+1,'Value'] = df.loc[range(last_actual_year-4,last_actual_year+1),'Value'].mean()*parameter['CPI ratio'][last_actual_year+1]
    # other forecast year
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',parameter['CPI ratio'])

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)


# County Gas Tax Distribution
# Estimate 2021 Revenue = (Y regional fuel forecasts/Y-1 regional fuel forecasts) × (average 2016-2020 revenue)
# year Y revenue= (Y regional fuel forecasts/Y-1 regional fuel forecasts) × Y-1 revenue

df_forecast = county_roads.loc[county_roads['Revenue Type']=="County Gas Tax Distribution"].copy()

counties = df_forecast['County'].unique().tolist()
for county in counties:
    df = df_forecast.loc[county_roads['County']==county].copy()

    last_actual_year = max(df['Year'])
    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])

    # motor fuel ratio * average previous 5 years for the first forecast year
    # first forecast year
    df.loc[last_actual_year+1,'Value'] = motor_fuel.loc[last_actual_year+1,'ratio']*df.loc[range(last_actual_year-4,last_actual_year+1),'Value'].mean()
    # other forecast year
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',motor_fuel['ratio'])

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)


# Real Estate Excise Tax
# data only found in Pierce county
df_forecast = county_roads.loc[county_roads['Revenue Type']=="Real Estate Excise Tax"].copy()

for county in df_forecast['County'].unique():
    df = df_forecast.loc[county_roads['County']==county].copy()

    county_pop = subarea_pop.loc[subarea_pop['County']=="Pierce County"]
    multiply_value = parameter['CPI ratio']+county_pop['ratio']-1

    last_actual_year = max(df['Year'])
    df = forecasting_tool.add_years(df,['County', 'Revenue Category', 'Revenue Type'],data_config['end_year'])

    # motor fuel ratio * average previous 5 years for the first forecast year
    df.loc[last_actual_year+1,'Value'] = multiply_value[last_actual_year+1]*df.loc[range(last_actual_year-4,last_actual_year+1),'Value'].mean()
    # other forecast year
    test = forecasting_tool.forecast_prev_year_multiply(df,'Value',multiply_value)

    county_roads_result = pd.concat([county_roads_result, test], ignore_index=True)
