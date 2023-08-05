import pandas as pd
from components import common_functions


class PopulationData(object):
    NAME = "population data"

    def __init__(self, path: str):
        self._df = pd.read_csv(
            path,
            dtype={
                "County": str,
                "PopulationArea": str,
                "Year": int,
                "Population": float
            }
        )

    @property
    def data(self, data_name: str = NAME):
        """The Local Transit Revenue dataframe property."""
        print("get " + data_name + " dataframe")
        return self._df

    def datatable(self, counties: list[str],
                  slider_year: list[int], value_unit: str = '') -> pd.DataFrame:

        YEAR_RANGE = range(slider_year[0], slider_year[1]+1)

        _datatable = self._df.copy()
        _datatable2 = common_functions.format_value(_datatable, 'Population', value_unit)

        return _datatable2. \
            query("`County` in @counties and `Year` in @YEAR_RANGE"). \
            pivot(index=['County', 'PopulationArea'],
                  columns='Year',
                  values='Population'). \
            reset_index()
