import pandas as pd
from components import ids, common_functions


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

        YEAR_RANGE = range(slider_year[0], slider_year[1]+1)

        _datatable = self._df.copy()

        _filtered_datatable = _datatable. \
            query("`Dollar Type` in @dollar and `Revenue Type` in @revenue_types and `Transit Agency` in @agencies and "
                  "`Year` in @YEAR_RANGE").drop(columns=['Dollar Type'])

        # calculate total revenue of each agency
        test = _filtered_datatable.groupby(['Transit Agency', 'Year'], as_index=False)['Value'].agg("sum")
        test['Revenue Type'] = "Total"
        _filtered_datatable2 = pd.concat([_filtered_datatable, test[_filtered_datatable.columns]]).\
            reset_index(drop=True)

        _filtered_datatable2 = common_functions.format_value(_filtered_datatable2, 'Value', value_unit)

        return _filtered_datatable2. \
            pivot(index=['Transit Agency', 'Revenue Type'], columns='Year', values='Value'). \
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

    def datatable(self, agencies: list[str], slider_year: list[int], value_unit: str = '') -> pd.DataFrame:
        """
        present dash datatable
        """

        YEAR_RANGE = range(slider_year[0], slider_year[1]+1)

        _datatable = self._df.copy()

        # calculate total boarding
        _filtered_datatable = _datatable. \
            query("`Transit Agency` in @agencies and `Year` in @YEAR_RANGE")
        test = _filtered_datatable.groupby(['Year'], as_index=False)['Boardings'].agg("sum")
        test['Transit Agency'] = 'Total Transit Boardings'
        agencies.extend(['Total Transit Boardings'])

        _datatable2 = pd.concat([_filtered_datatable, test[_filtered_datatable.columns]]). \
            reset_index(drop=True)

        _datatable2 = common_functions.format_value(_datatable2, 'Boardings', value_unit)

        return _datatable2. \
            query("`Transit Agency` in @agencies and `Year` in @YEAR_RANGE"). \
            pivot(index=['Transit Agency'], columns='Year', values='Boardings'). \
            reset_index()

