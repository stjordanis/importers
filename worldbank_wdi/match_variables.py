"""Creates a `variable_replacements.json` file of {old variable id} to
{new variable id} key-value pairs.

`variable_replacements.json` is used in `suggest_chart_revisions.py` for
determining which charts to update.

Usage:

    python -m worldbank_wdi.match_variables
"""

import os
import simplejson as json
import logging
from typing import List
import pandas as pd
from pymysql import Connection

from db import get_connection
from worldbank_wdi import OUTPATH

UPDATE_DB = False

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    with get_connection() as conn:
        # retrieves old and new datasets
        df_old_datasets = get_datasets(conn, new=False)
        df_new_datasets = get_datasets(conn, new=True)

        # retrieves old and new variables
        df_old_vars = get_variables(conn, dataset_ids=df_old_datasets["id"])
        df_new_vars = get_variables(conn, dataset_ids=df_new_datasets["id"])
        df_vars = pd.merge(
            df_old_vars,
            df_new_vars,
            on="name",
            how="inner",
            suffixes=["_old", "_new"],
            validate="m:1",
        )
        assert df_vars.id_old.notnull().all() and df_vars.id_new.notnull().all()
        old_var_id2new_var_id = (
            df_vars.dropna(subset=["id_old", "id_new"])
            .set_index("id_old")["id_new"]
            .squeeze()
            .to_dict()
        )
        if not os.path.exists(OUTPATH):
            os.makedirs(OUTPATH)
        with open(os.path.join(OUTPATH, "variable_replacements.json"), "w") as f:
            json.dump(old_var_id2new_var_id, f)


def get_datasets(conn: Connection, new: bool = True) -> pd.DataFrame:
    """retrieves new datasets if `new=True`, else retrieves old datasets.

    Arguments:

        new: bool = True. If True, retrieves new datasets. Else retrieves
            old datasets.

    Returns:

        pd.DataFrame: dataframe of old or new datasets.
    """
    columns = ["id", "name", "createdAt", "updatedAt"]
    try:
        datasets = pd.read_csv(os.path.join(OUTPATH, "datasets.csv"))
        new_dataset_names = datasets.name.unique().tolist()
    except FileNotFoundError:
        new_dataset_names = []
    if new:
        query = f"""
            SELECT {','.join(columns)}
            FROM datasets
            WHERE name IN ({','.join([f'"{n}"' for n in new_dataset_names])})
        """
    else:
        query = f"""
            SELECT {','.join(columns)}
            FROM datasets
            WHERE name COLLATE UTF8_GENERAL_CI LIKE '%world development indicators%'
        """
        if len(new_dataset_names):
            new_dataset_names_str = ",".join([f'"{n}"' for n in new_dataset_names])
            query += f" AND name NOT IN ({new_dataset_names_str})"
    df_datasets = pd.read_sql(query, conn)
    return df_datasets


def get_variables(conn: Connection, dataset_ids: List[int]) -> pd.DataFrame:
    """retrieves all variables in dataset(s).

    Also retrieves the min year and max year of available data for each variable.

    Arguments:

        dataset_ids: List[Union[int, str]]. List of dataset ids for which
            to retrieve variables.

    Returns:

        pd.DataFrame. Dataframe of variables.
    """
    # retrieves all variables in old dataset(s)
    dataset_ids_str = ",".join([str(_id) for _id in dataset_ids])
    columns = [
        "id",
        "name",
        "description",
        "unit",
        "display",
        "createdAt",
        "updatedAt",
        "datasetId",
        "sourceId",
    ]
    df_vars = pd.read_sql(
        f"""
        SELECT {','.join(columns)}
        FROM variables
        WHERE datasetId IN ({dataset_ids_str})
    """,
        conn,
    )
    return df_vars


if __name__ == "__main__":
    main()
