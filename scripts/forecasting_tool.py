import pandas as pd
import numpy as np
import math


def fix_path(base_path: str) -> str:
    return "../"+base_path


def fill_year(df, group_cols, start_year, end_year):
    """fill in missing years with nan values between start and end year (2050 for 2018 RTP)"""
    df3 = df.copy()

    # fill in missing years
    df3 = df3.set_index("Year")
    df3 = df3.reindex(list(range(start_year, end_year + 1)))
    df3.reset_index(inplace=True)
    df3[group_cols] = df3[group_cols].ffill()

    return df3


def add_constant_dollar(df: pd.DataFrame, parameter: pd.DataFrame) -> pd.DataFrame:
    """append another version of same dataframe with calculated constant dollar"""
    # prep dataframe with nominal revenue
    df_nominal = df.copy().rename(columns={"Nominal": "Value"})
    df_nominal["Dollar Type"] = "Nominal"
    # calculate constant dollar
    df_constant = pd.merge(df, parameter[['Year', 'PV factor']], how="left", on="Year")
    df_constant["Value"] = df_constant['Nominal'] * df_constant['PV factor']
    df_constant["Dollar Type"] = "Constant"
    df_constant = df_constant[df_nominal.columns]

    return pd.concat([df_nominal, df_constant], ignore_index=True)


def interpolate_population(df, pop_col, start_year, end_year):
    df3 = df.copy()

    # last and next year with population values
    df3['low'] = df3[pop_col].ffill()
    df3['up'] = df3[pop_col].bfill()
    # nth root
    df3['n'] = df3.groupby(['up'])['up'].transform('count')

    # calculation
    for year in range(start_year, end_year + 1):
        miss = df3.loc[df3['Year'] == year, pop_col].item()
        up = df3.loc[df3['Year'] == year, 'up'].item()
        low = df3.loc[df3['Year'] == year, 'low'].item()
        n = df3.loc[df3['Year'] == year, 'n'].item()
        # if the year is missing population value
        if np.isnan(miss):
            if low == 0:
                val = 0
            else:
                val = ((up / low) ** (1 / n)) * last_val
        else:
            val = miss
        df3.loc[df3['Year'] == year, pop_col] = math.ceil(val)
        last_val = val

    return df3[pop_col]
