import pandas as pd
import numpy as np
import os
import math
import toml
import forecasting_tool

data_config = toml.load(os.path.join(os.getcwd(), "../configuration.toml"))

# TODO: expand to full "Subarea Allocation Bases" tab
subarea_population = pd.read_csv(data_config['input_subarea_population_actual'])

result_subarea_population = pd.DataFrame()
for i_county in subarea_population['County'].unique():
    for i_pop_area in subarea_population['PopulationArea'][subarea_population['County'] == i_county].unique():

        df_pop = subarea_population[(subarea_population['County'] == i_county) & (subarea_population['PopulationArea'] == i_pop_area)].copy()

        end_year = int(df_pop['Year'].max())
        # fill in missing years
        df_pop = forecasting_tool.add_years(df_pop,['County', 'PopulationArea'],end_year,'Population')
        # calculate interpolated population
        df_pop = forecasting_tool.interpolate_sub_alloc_base(df_pop, 'Population')

        result_subarea_population = pd.concat([result_subarea_population, df_pop[['County', 'PopulationArea', 'Year', 'Population']]], ignore_index=True)
        
result_subarea_population.to_csv(data_config['input_subarea_population_forecast'], index=False)