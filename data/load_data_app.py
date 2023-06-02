import pandas as pd
# import os
# import toml

# data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))


class LocalTransitRevenue(object):
    NAME = "Local Transit Revenue"

    def __init__(self, path: str):
        self._df = pd.read_csv(
            path,
            dtype={
                "Year": int,
                "Revenue Type": str,
                "Transit Agency": str,
                "Nominal": float,
                "Constant": float
            }
        )

    @property
    def data(self, data_name: str = NAME):
        """The Local Transit Revenue dataframe property."""
        print("get " + data_name + " dataframe")
        return self._df

    def datatable(self, revenue_types: list[str], agencies: list[str],
                  slider_year: list[int], dollar: str, value_unit: str = '') -> pd.DataFrame:
        """
        present dash datatable
        1. dollar type
        2. filtering revenue type and transit agency
        3. Millions/ Thousands
        4. sorting
        """
        YEAR_RANGE = range(slider_year[0],slider_year[1])

        # change value format to thousands or millions
        def format_value(df: pd.DataFrame, value_col: str, value_unit: str):

            df2 = df.copy()
            if value_unit in ['', 'K', 'M']:
                if value_unit == '':
                    df2[value_col] = df2[value_col].apply(lambda x: f"{round(x, 2)}")
                if value_unit == 'K':
                    df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000.0, 2)}{'K'}")
                if value_unit == 'M':
                    df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000000.0, 2)}{'M'}")
            else:
                print("Value units must be 'K' for thousands or 'M' for millions")

            return df2

        _datatable = self._df.copy()
        _datatable = format_value(_datatable, 'Value', value_unit)

        return _datatable. \
            query("`Dollar Type` in @dollar and `Revenue Type` in @revenue_types and `Transit Agency` in @agencies and "
                  "`Year` in @YEAR_RANGE"). \
            pivot(index=['Revenue Type', 'Transit Agency'],
                  columns='Year',
                  values='Value'). \
            reset_index()


class LocalTransitBoarding(object):
    NAME = "Local Transit Boarding"

    def __init__(self, path: str):
        self._df = pd.read_csv(
            path,
            dtype={
                "Transit Agency": str,
                "Year": int,
                "Boardings": float
            }
        )

    @property
    def data(self, data_name: str = NAME):
        """The Local Transit Revenue dataframe property."""
        print("get " + data_name + " dataframe")
        return self._df

    def datatable(self, agencies: list[str],
                  slider_year: list[int], value_unit: str = '') -> pd.DataFrame:
        """
        present dash datatable
        """
        YEAR_RANGE = range(slider_year[0],slider_year[1])

        # change value format to thousands or millions
        def format_value(df: pd.DataFrame, value_col: str, value_unit: str):

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

        _datatable = self._df.copy()
        _datatable = format_value(_datatable, 'Boardings', value_unit)

        return _datatable. \
            query("`Transit Agency` in @agencies and `Year` in @YEAR_RANGE"). \
            pivot(index=['Transit Agency'],
                  columns='Year',
                  values='Boardings'). \
            reset_index()

