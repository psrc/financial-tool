# Initial Data Processing
# - Read in raw data from Excel spreadsheets (from excel_data_2018 folder)
# - Reformat raw data to input for financial tool (saved to input_data_2018 folder)

import pandas as pd
import toml
import os


data_config = toml.load(os.path.join(os.getcwd(), "../configuration.toml"))

#  Local Transit Tab
# Replace datasets
replace_parameter = False
replace_subarea_population = False
replace_boardings_local_transit = False
replace_fare_per_boarding_local_transit = False
replace_revenue_local_transit = False
replace_tax_base = False
replace_state_highway_revenue = False
replace_county_roads_revenue = True

# actual data from 2018 excel spreadsheet

#  Local Transit Tab
## Transit revenues (Nominal $millions)
Excel_data_revenue_local_transit = "script_data/excel_data_2018/local_transit_actual_revenue.csv"
## Total Fixed-Route boardings
Excel_data_boardings_local_transit = "script_data/excel_data_2018/local_transit_actual_boardings.csv"         # FIXME: consider RTP forecast data
## Fixed-Route fare per boarding
Excel_data_fare_per_boarding_local_transit = "script_data/excel_data_2018/local_transit_fare_per_boarding.csv"

# Tax Base Tab
Excel_data_tax_base = "script_data/excel_data_2018/tax_base_actual.csv"
Excel_data_parameter = "script_data/excel_data_2018/parameters_tax.csv"

# Subarea Allocation Bases Tab
Excel_data_subarea_population = "script_data/excel_data_2018/subarea_allocation_bases_population_actual.csv"

# State Highway
Excel_data_state_highway_revenue = "script_data/excel_data_2018/state_highway_revenue_generated_2014.csv"

# County Roads
Excel_data_revenue_county_roads = "script_data/excel_data_2018/county_roads_revenue.csv"


if replace_parameter:
    parameter = pd.read_csv(Excel_data_parameter).astype({'Year': 'int64'})

    # add Calculate inflation using CPI (current year vs. previous year)
    for year in range(min(parameter['Year'])+1, max(parameter['Year'])+1):
        cpi_prev_year = parameter.loc[parameter['Year'] == year - 1, 'CPI'].item()
        parameter.loc[parameter['Year'] == year, 'indecies'] = parameter.loc[parameter['Year'] == year, 'CPI'] / cpi_prev_year

    parameter.to_csv(data_config['input_parameter'], index=False)


# Subarea Allocation Bases - Population
if replace_subarea_population:
    df = pd.read_csv(Excel_data_subarea_population)

    subarea_population = pd.melt(df,
                                 id_vars=['County', 'PopulationArea'],
                                 value_vars=df.columns[2:],
                                 var_name='Year',
                                 value_name='Population').dropna().astype(
        {'Year': 'int64', 'County': str, 'PopulationArea': str, 'Population': 'int64'})

    subarea_population.to_csv(data_config['input_subarea_population'], index=False)


# Local Transit - Total Fixed-Route boardings
if replace_boardings_local_transit:
    df = pd.read_csv(Excel_data_boardings_local_transit)

    transit_boardings = pd.melt(df,
                                id_vars='Transit Agency',
                                value_vars=df.columns[1:],
                                var_name='Year',
                                value_name='Boardings (000s)').dropna().astype({'Year': 'int64'})

    transit_boardings['Boardings'] = transit_boardings['Boardings (000s)'].apply(
        lambda x: x.strip().replace(',', '')).astype({'Boardings (000s)': float}) * 1e3
    transit_boardings['Boardings'] = transit_boardings['Boardings'].astype({'Boardings': int})
    transit_boardings = transit_boardings[['Transit Agency', 'Year', 'Boardings']]

    transit_boardings.to_csv(data_config['input_local_transit_boardings'], index=False)


# Average Fixed-Route fare per boarding with periodic increases
if replace_fare_per_boarding_local_transit:
    df = pd.read_csv(Excel_data_fare_per_boarding_local_transit)

    fare_per_boarding = pd.melt(df, id_vars='Transit Agency', value_vars=df.columns[1:],
                                var_name='Year', value_name='Average Fare per Boarding ($)').dropna().\
        astype({'Year': 'int64',
                'Average Fare per Boarding ($)': 'float'})

    fare_per_boarding.to_csv(data_config['input_local_transit_fare_per_boarding'], index=False)


# Local Transit Revenue
if replace_revenue_local_transit:
    df = pd.read_csv(Excel_data_revenue_local_transit)

    # wide to long
    transit_revenue = pd.melt(df, id_vars=['Revenue Type', 'Transit Agency'], value_vars=df.columns[2:],
                              var_name='Year', value_name='Nominal $millions').dropna().astype({'Year': 'int64'})
    # calculate normal value
    transit_revenue['Nominal'] = transit_revenue['Nominal $millions']*1e6
    transit_revenue = transit_revenue[['Revenue Type', 'Transit Agency', 'Year', 'Nominal']]

    transit_revenue.to_csv(data_config['input_local_transit_revenue'], index=False)


if replace_tax_base:
    df = pd.read_csv(Excel_data_tax_base)

    tax_base = pd.melt(df, id_vars=['County', 'Tax Base Category'], value_vars=df.columns[2:],
                       var_name='Year', value_name='Values').dropna()

    tax_base["Multiplier"] = 1e6
    tax_base.loc[tax_base["Tax Base Category"].str.contains("000s"), "Multiplier"] = 1e3
    tax_base.loc[tax_base["Tax Base Category"].str.contains("Diesel"), "Multiplier"] = 1
    tax_base["Value"] = tax_base["Multiplier"] * tax_base["Values"]

    new_values = {
        'Personal Income (nominal $mil) ': 'Personal Income (nominal)',
        'Population (000s) ': 'Population',
        'Employment (000s) ': 'Employment',
        'Retail Sales (nominal $mil) ': 'Retail Sales (nominal)',
        'Motor Fuel (gal. Mil.) ': 'Motor Fuel (gal.)',
        'Cars and Gas Trucks (000s)': 'Cars and Gas Trucks',
        'Diesel': 'Diesel',
        'Total Registrations (000s)': 'Total Registrations'
    }
    tax_base["Tax Base Category"] = tax_base["Tax Base Category"].map(new_values)
    tax_base = tax_base[['County', 'Tax Base Category', 'Year', 'Value']]

    tax_base.to_csv(data_config['input_tax_base'], index=False)


if replace_state_highway_revenue:
    df = pd.read_csv(Excel_data_state_highway_revenue)

    state_highway = pd.melt(df,
                            id_vars='Base Program Revenue Type',
                            value_vars=df.columns[1:],
                            var_name='Year',
                            value_name='Nominal').dropna().astype({'Year': 'int64'})

    state_highway.to_csv(data_config['input_state_highway_revenue'], index=False)

if replace_county_roads_revenue:
    df = pd.read_csv(Excel_data_revenue_county_roads)

    county_roads = pd.melt(df, id_vars=['County', 'Revenue Category', 'Revenue Type'], value_vars=df.columns[3:],
                    var_name='Year', value_name='Value').dropna()

    county_roads.to_csv(data_config['input_county_roads_revenue'], index=False)