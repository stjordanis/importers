"""downloads WDI data and saves it to disk.
"""

import os
import shutil
import zipfile
from io import BytesIO
import requests
import pandas as pd

from worldbank_wdi import INPATH

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    delete_input()
    download_data()


def delete_input() -> None:
    """deletes all files and folders in `{INPATH}`.

    WARNING: this method deletes all input data and is only intended for use
    immediately prior to `download_data()`.
    """
    if os.path.exists(INPATH):
        shutil.rmtree(INPATH)
    logger.info(f"Deleted all existing input files in {INPATH}")


def download_data() -> None:
    """Downloads the raw World Development Indicators data and saves it
    in csv format to `{INPATH}`.
    """
    if not os.path.exists(INPATH):
        os.makedirs(INPATH)
    url = "http://databank.worldbank.org/data/download/WDI_csv.zip"
    logger.info(f'Downloading data from "{url}"...')
    res = requests.get(url)
    zf = zipfile.ZipFile(BytesIO(res.content))
    fnames = zf.namelist()
    zf.extractall(path=INPATH)
    for fname in fnames:
        fname_zip = f'{fname}.zip'
        pd.read_csv(os.path.join(INPATH, fname)) \
          .to_csv(os.path.join(INPATH, fname_zip), index=False, compression='gzip')
        os.remove(os.path.join(INPATH, fname))
    logger.info(f"Data succcessfully downloaded to {INPATH}")


if __name__ == '__main__':
    main()
