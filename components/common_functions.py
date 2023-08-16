import pandas as pd


# change value format to thousands or millions
def format_value(df: pd.DataFrame, value_col: str, value_unit: str) -> pd.DataFrame:

    df2 = df.copy()
    if value_unit in ['', 'K', 'M']:
        if value_unit == '':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x, 0)}")
        if value_unit == 'K':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000.0, 2)}{'K'}")
        if value_unit == 'M':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000000.0, 2)}{'M'}")
    else:
        print("Value units must be 'K' for thousands or 'M' for millions")

    return df2