import pandas as pd
import os
import toml

data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))


class DataSchema:
    YEAR = "Year"
    REVENUE_TYPE = "Revenue Type"
    TRANSIT_AGENCY = "Transit Agency"
    NOMINAL = "Nominal"
    CONSTANT = "Constant"


def load_local_transit_revenue_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(
        data_config[path],
        dtype={
            DataSchema.YEAR: int,
            DataSchema.REVENUE_TYPE: str,
            DataSchema.TRANSIT_AGENCY: str,
            DataSchema.NOMINAL: float,
            DataSchema.CONSTANT: float
        }
    )
    return data
