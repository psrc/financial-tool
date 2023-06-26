import pandas as pd
import numpy as np
import os
import toml
from scripts import forecasting_tool

data_config = toml.load(os.path.join(os.getcwd(), "../configuration.toml"))

# predict data
predict_subarea_population = False
predict_boardings_local_transit = False
predict_fare_per_boarding_local_transit = False
predict_revenue_local_transit = True
predict_tax_base = False

# Subarea Allocation Bases - Population
if predict_subarea_population:
    subarea_population = pd.read_csv(data_config['data_subarea_population'])

    result_subarea_population = pd.DataFrame()
    for i_county in data_config['all_counties']:
        for i_pop_area in subarea_population.PopulationArea.unique():

            df_pop = subarea_population[
                (subarea_population['County'] == i_county) & (
                        subarea_population['PopulationArea'] == i_pop_area)].copy()

            if df_pop.empty:
                pass

            else:
                start_year = int(df_pop['Year'].min())
                end_year = int(df_pop['Year'].max())
                # fill in missing years
                df_pop = forecasting_tool.fill_year(df_pop, ['County', 'PopulationArea'], start_year, end_year)
                # calculate interpolated population
                df_pop['Population'] = forecasting_tool.interpolate_population(df_pop, 'Population', start_year,
                                                                               end_year)
                df_pop = df_pop[['County', 'PopulationArea', 'Year', 'Population']]

                result_subarea_population = pd.concat([result_subarea_population, df_pop], ignore_index=True)
    result_subarea_population.to_csv(data_config['result_subarea_population'], index=False)

# Local Transit - Total Fixed-Route boardings
if predict_boardings_local_transit:
    transit_boardings = pd.read_csv(data_config['data_boardings_local_transit'])
    result_subarea_population = pd.read_csv(data_config['result_subarea_population'])

    result_boarding = pd.DataFrame()
    for agency in data_config['county_transit']:

        df_agency = transit_boardings[(transit_boardings['Transit Agency'] == agency)].copy()

        # fill in missing years
        start_year = df_agency['Year'].min()

        df_agency = forecasting_tool.fill_year(df_agency, 'Transit Agency', start_year, data_config['end_year'])

        # last and next year with population values
        # Everett transit using City Transit Population for boarding estimation, others using PTBA
        if agency == "Everett Transit":
            df_agency1 = pd.merge(df_agency, result_subarea_population[
                (result_subarea_population['County'] == data_config['county_transit'][agency]) &
                (result_subarea_population['PopulationArea'] == 'City Transit')],
                                  how="left", on="Year")
        else:
            df_agency1 = pd.merge(df_agency, result_subarea_population[
                (result_subarea_population['County'] == data_config['county_transit'][agency]) &
                (result_subarea_population['PopulationArea'] == 'PTBA')],
                                  how="left", on="Year")

        # calculation
        for year in range(start_year, data_config['end_year'] + 1):
            miss = df_agency1.loc[df_agency1['Year'] == year, 'Boardings'].item()

            if np.isnan(miss):
                boarding_prev_year = df_agency1.loc[df_agency1['Year'] == year - 1, 'Boardings'].item()
                pop = df_agency1.loc[df_agency1['Year'] == year, 'Population'].item()
                pop_prev_year = df_agency1.loc[df_agency1['Year'] == year - 1, 'Population'].item()

                df_agency1.loc[df_agency1['Year'] == year, 'Boardings'] = boarding_prev_year * pop / pop_prev_year

            else:
                pass

        result_boarding = pd.concat([result_boarding, df_agency1], ignore_index=True)

    result_boarding = result_boarding[['Transit Agency', 'Year', 'Boardings']]
    result_boarding.to_csv(data_config['result_boardings_local_transit'], index=False)

# Average Fixed-Route fare per boarding with periodic increases
if predict_fare_per_boarding_local_transit:
    fare_per_boarding = pd.read_csv(data_config["data_fare_per_boarding_local_transit"])

    result_fare_per_boarding = pd.DataFrame()
    for agency in data_config['county_transit']:
        fare_per_boarding1 = fare_per_boarding.copy()
        # get the last year with actual value for creating periodic increases
        last_value_year = max(fare_per_boarding1['Year'])
        # base list of fare change period
        list_grp = sorted(
            list(range(1, data_config['end_year'] - last_value_year)) * data_config['transit_fare_change_period'][
                agency])

        fare_per_boarding1 = forecasting_tool.fill_year(
            fare_per_boarding1[fare_per_boarding1['Transit Agency'] == agency], 'Transit Agency', 1989,
            data_config['end_year'])

        # Average Fixed-Route fare per boarding by Annual Growth Rate: This has the fare grown by the average annual growth rate for each transit agency based on previous 20 year history
        for year in range(1989, data_config['end_year'] + 1):
            miss = fare_per_boarding1.loc[fare_per_boarding1['Year'] == year, 'Average Fare per Boarding ($)'].item()

            if np.isnan(miss):
                fare_prev_year = fare_per_boarding1.loc[
                    fare_per_boarding1['Year'] == year - 1, 'Average Fare per Boarding ($)'].item()
                fare_per_boarding1.loc[
                    fare_per_boarding1['Year'] == year, 'Average Fare per Boarding ($)'] = fare_prev_year + (
                        fare_prev_year * data_config['transit_annual_fare_increase'][agency])

            else:
                pass

        # add grouping column (trim base list to needed length)
        fare_per_boarding1['list_grp'] = list([0] * (last_value_year - 1989)) + list_grp[0:data_config[
                                                                                               'end_year'] - last_value_year + 1]
        # Average Fixed-Route fare per boarding with periodic increases
        fare_per_boarding1.loc[fare_per_boarding1['list_grp'] > 0, 'Average Fare per Boarding ($)'] = \
            fare_per_boarding1.loc[
                fare_per_boarding1['list_grp'] > 0, ['list_grp', 'Average Fare per Boarding ($)']].groupby(
                ['list_grp'])[
                'Average Fare per Boarding ($)'].transform(min)
        result_fare_per_boarding = pd.concat(
            [result_fare_per_boarding, fare_per_boarding1[['Year', 'Transit Agency', 'Average Fare per Boarding ($)']]],
            ignore_index=True)
    result_fare_per_boarding.to_csv(data_config['result_fare_per_boarding_local_transit'], index=False)

if predict_revenue_local_transit:
    """
    Local Transit Revenue calculation:
    Part 1 - Sales and Use Tax
    Part 2 - Fare revenue
    Part 3 - PSRC FHWA and PSRC FTA funding
    Part 4 - Non-PSRC FHWA, Non-PSRC FTA, State and Other Federal funding
    Old revenue: MVET not available anymore
    """

    # Local Transit Revenue
    parameter = pd.read_csv(data_config['parameter']).astype({'Year': 'int64'})
    transit_revenue = pd.read_csv(data_config['data_revenue_local_transit'])

    # Part 2 - Local transit fare revenue
    result_fare_per_boarding = pd.read_csv(forecasting_tool.fix_path(data_config['result_fare_per_boarding_local_transit']))
    result_boarding = pd.read_csv(forecasting_tool.fix_path(data_config['result_boardings_local_transit']))
    revenue_transit_fare = pd.merge(result_boarding[['Year', 'Transit Agency', 'Boardings']],
                                    result_fare_per_boarding[
                                        ['Year', 'Transit Agency', 'Average Fare per Boarding ($)']],
                                    on=['Year', 'Transit Agency'])
    revenue_transit_fare['Nominal'] = revenue_transit_fare['Boardings'] * revenue_transit_fare[
        'Average Fare per Boarding ($)']
    revenue_transit_fare['Revenue Type'] = "Fares"
    result_transit_revenue_fare = revenue_transit_fare[['Year', 'Revenue Type', 'Transit Agency', 'Nominal']].copy()

    # Part 3 - PSRC FHWA and PSRC FTA funding
    # previous year times 1.025

    process_list = ['PSRC FHWA', 'PSRC FTA']
    predict_list_other = ['Non-PSRC FTA', 'State', 'Other Federal']

    result_transit_funding = pd.DataFrame()
    for agency in data_config['county_transit'].keys():
        # forecasting ['PSRC FHWA', 'PSRC FTA'] fundings
        for predict in process_list:
            # first predicting year uses the average of the last five years with known revenue
            df = transit_revenue[
                (transit_revenue['Transit Agency'] == agency) & (transit_revenue['Revenue Type'] == predict)].copy()
            max_year = max(df['Year'])
            df = forecasting_tool.fill_year(df, ['Revenue Type', 'Transit Agency'],
                                            min(df['Year']), data_config['end_year'])
            df.loc[df['Year'] == max_year + 1, 'Nominal'] = df[df['Year'].isin(range(max_year - 5, max_year + 1))][
                                                                'Nominal'].mean() * \
                                                            data_config['psrc_transit_funding_annual_increase']
            # other years: previous year funding * 1.025
            for year in range(max_year + 2, data_config['end_year'] + 1):
                funding_prev_year = df.loc[df['Year'] == year - 1, 'Nominal'].item()
                df.loc[df['Year'] == year, 'Nominal'] = funding_prev_year * data_config[
                    'psrc_transit_funding_annual_increase']
            result_transit_funding = pd.concat([result_transit_funding, df], ignore_index=True)

        # forecasting ['Non-PSRC FTA','State','Other Federal'] fundings
        for predict in predict_list_other:
            # first predicting year uses the average of the last five years with known revenue
            df = transit_revenue[
                (transit_revenue['Transit Agency'] == agency) & (transit_revenue['Revenue Type'] == predict)].copy()
            max_year = max(df['Year'])
            df = forecasting_tool.fill_year(df, ['Revenue Type', 'Transit Agency'],
                                            min(df['Year']), data_config['end_year'])
            df.loc[df['Year'] == max_year + 1, 'Nominal'] = df[df['Year'].isin(range(max_year - 5, max_year + 1))][
                                                                'Nominal'].mean() * \
                                                            parameter.loc[
                                                                parameter['Year'] == max_year + 1, 'indecies'].item()
            # other years: previous year funding * 1.025
            for year in range(max_year + 2, data_config['end_year'] + 1):
                funding_prev_year = df.loc[df['Year'] == year - 1, 'Nominal'].item()
                df.loc[df['Year'] == year, 'Nominal'] = funding_prev_year * parameter.loc[
                    parameter['Year'] == year, 'indecies'].item()
            result_transit_funding = pd.concat([result_transit_funding, df], ignore_index=True)

    # PART 4: Sales & Use Tax
    transit_sales_tax_rate = pd.read_csv(data_config['data_transit_sales_tax_rate']).astype({'Year': 'int64'})

    retail_sales = pd.read_csv(data_config['data_tax_base'])
    retail_sales = retail_sales[retail_sales['Tax Base Category'] == 'Retail Sales (nominal)']

    result_transit_sales_tax = pd.DataFrame()

    for agency in data_config['county_transit'].keys():
        df = transit_revenue[(transit_revenue['Transit Agency'] == agency) & (
                    transit_revenue['Revenue Type'] == 'Sales & Use Tax')].copy()

        max_year = max(df['Year'])

        df = forecasting_tool.fill_year(df, ['Revenue Type', 'Transit Agency'],
                                        min(df['Year']), data_config['end_year'])

        sales = pd.merge(retail_sales[retail_sales['County'] == data_config['county_transit'][agency]],
                         transit_sales_tax_rate[['Year', agency]],
                         on=['Year'])
        sales['Sales & Use Tax'] = sales[agency] * sales['Value'] * data_config['transit_boundary_cal'][agency]

        df = pd.merge(df, sales[['Year', 'Sales & Use Tax']],
                      how='left', on=['Year'])
        df.loc[np.isnan(df['Nominal']), 'Nominal'] = df['Sales & Use Tax']
        df = df[['Year', 'Revenue Type', 'Transit Agency', 'Nominal']]
        result_transit_sales_tax = pd.concat([result_transit_sales_tax, df], ignore_index=True)

    # aggregate all revenue types
    df = transit_revenue[transit_revenue['Revenue Type'] == 'MVET'].copy()
    revenue_nominal = pd.concat([result_transit_revenue_fare, result_transit_funding,
                                result_transit_sales_tax, df], ignore_index=True)
    revenue_nominal = revenue_nominal[revenue_nominal['Nominal'] != 0.0]

    # calculate constant revenue with PV factor
    result_revenue = forecasting_tool.add_constant_dollar(revenue_nominal, parameter[['Year', 'PV factor']])

    # save to output
    result_revenue.to_csv(forecasting_tool.fix_path(data_config['tab_revenue_local_transit']), index=False)
    print("saved Local Transit Revenue to " + forecasting_tool.fix_path(data_config['tab_revenue_local_transit']))

