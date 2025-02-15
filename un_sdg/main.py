"""executes bulk dataset import + chart updates for the UN_SDGs dataset.
Usage:
    python -m un_sdg.main

To run the code without downloading the data again: 
    python -m un_sdg.main --skip_download

To run the code without downloading or cleaning the data again: 
    python -m un_sdg.main --skip_download --skip_clean
"""
import click

from un_sdg import DATASET_DIR, DATASET_NAMESPACE

from un_sdg import download, clean, match_variables

from standard_importer import import_dataset
from standard_importer.chart_revision_suggester import ChartRevisionSuggester


@click.command()
@click.option(
    "--download_data/--skip_download",
    default=True,
    help="Whether or not to download the data from the source as it often takes quite some time.",
)
@click.option(
    "--clean_data/--skip_clean",
    default=True,
    help="Whether or not to clean the data, useful for just upserting previously cleaned data",
)
def main(download_data, clean_data):
    if download_data:
        download.main()
    if clean_data:
        clean.main()
    import_dataset.main(DATASET_DIR, DATASET_NAMESPACE)
    match_variables.main()

    suggester = ChartRevisionSuggester(DATASET_DIR)
    suggester.suggest()


if __name__ == "__main__":
    main()
