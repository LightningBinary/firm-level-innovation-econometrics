"""
Data Loading and Preprocessing Module
======================================
For the Cincera (1997) panel dataset on patents, R&D, and technological spillovers.

This module provides functions to load, reshape, and prepare the raw ASCII data
for econometric analysis in Python.

Data Source:
    Cincera, M. (1997): "Patents, R&D and Technological Spillovers at the Firm Level"
    Journal of Applied Econometrics, Vol. 12, No. 3, pp. 265-280.
    https://doi.org/10.15456/jae.2022313.1256653867
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ──────────────────────────────────────────────
# Sector and region mapping
# ──────────────────────────────────────────────

SECTOR_MAP = {
    1: "Aerospace",
    2: "Chemistry",
    3: "Computers",
    4: "Drugs",
    5: "Electricity",
    6: "Food",
    7: "Fuel and Mining",
    8: "Glass",
    9: "Instruments",
    10: "Machinery",
    11: "Metals",
    12: "Other",
    13: "Paper",
    14: "Software",
    15: "Motor Vehicles",
}

REGION_MAP = {
    1: "European Union",
    2: "Japan",
    3: "U.S.",
    4: "Rest of the World",
}


def load_data(data_path="data/data.mc"):
    """
    Load the raw ASCII panel dataset.

    The dataset has 181 firms and 30 columns:
        - col 1: firm_id
        - col 2: sector (1-15)
        - col 3: region (1-4)
        - cols 4-12: patents_1983 through patents_1991 (9 years)
        - cols 13-21: log_RD_1983 through log_RD_1991
        - cols 22-30: log_spillover_1983 through log_spillover_1991

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame with one row per firm.
    """
    df = pd.read_table(data_path, header=None, sep=r"\s+")

    col_names = (
        ["firm_id", "sector", "region"]
        + [f"patents_{year}" for year in range(1983, 1992)]
        + [f"log_RD_{year}" for year in range(1983, 1992)]
        + [f"log_spillover_{year}" for year in range(1983, 1992)]
    )
    df.columns = col_names

    # Categorical mapping
    df["sector_name"] = df["sector"].map(SECTOR_MAP)
    df["region_name"] = df["region"].map(REGION_MAP)

    return df


def reshape_to_long(df):
    """
    Reshape the wide-format dataset into long/panel format.

    Parameters
    ----------
    df : pd.DataFrame
        Wide-format data from load_data().

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns:
        [firm_id, sector, region, sector_name, region_name, year,
         patents, log_RD, log_spillover]
    """
    id_vars = ["firm_id", "sector", "region", "sector_name", "region_name"]

    long_df = pd.wide_to_long(
        df,
        stubnames=["patents", "log_RD", "log_spillover"],
        i=["firm_id", "sector", "region", "sector_name", "region_name"],
        j="year",
        sep="_",
    ).reset_index()

    long_df = long_df.sort_values(["firm_id", "year"]).reset_index(drop=True)

    # Ensure proper dtypes
    long_df["year"] = long_df["year"].astype(int)
    long_df["firm_id"] = long_df["firm_id"].astype(int)

    return long_df


def create_lagged_variables(long_df):
    """
    Create lagged variables (t-1) for 2SLS instrumental variable regression.

    For each firm, computes:
        - lag_log_RD: log_RD from the previous year
        - lag_log_spillover: log_spillover from the previous year

    Parameters
    ----------
    long_df : pd.DataFrame
        Long-format panel data.

    Returns
    -------
    pd.DataFrame
        Data with additional 'lag_log_RD' and 'lag_log_spillover' columns.
    """
    df = long_df.copy()
    df["lag_log_RD"] = df.groupby("firm_id")["log_RD"].shift(1)
    df["lag_log_spillover"] = df.groupby("firm_id")["log_spillover"].shift(1)
    return df


def prepare_panel_data(long_df):
    """
    Prepare panel data by setting a MultiIndex [(firm_id, year)] and
    optionally dropping missing lagged observations.

    Parameters
    ----------
    long_df : pd.DataFrame
        Long-format panel data (ideally with lagged variables).

    Returns
    -------
    pd.DataFrame
        PanelData with MultiIndex [(firm_id, year)].
    """
    panel_df = long_df.set_index(["firm_id", "year"])
    return panel_df
