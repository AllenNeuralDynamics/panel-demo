"""Utility code to pull the QC status data"""
from aind_data_access_api.document_db import MetadataDbClient
import os
import pandas as pd
import panel as pn

API_GATEWAY_HOST = os.getenv("API_GATEWAY_HOST", "api.allenneuraldynamics-test.org")
DATABASE = os.getenv("DATABASE", "metadata_index")
COLLECTION = os.getenv("COLLECTION", "data_assets")

docdb_api_client = MetadataDbClient(
    host=API_GATEWAY_HOST,
    database=DATABASE,
    collection=COLLECTION,
)

CACHE_RESET_DAY = 24 * 60 * 60
CACHE_RESET_HOUR = 60 * 60


@pn.cache(ttl=CACHE_RESET_DAY)
def _get_metadata(test_mode=False) -> pd.DataFrame:
    """Get metadata about records in DocDB

    Parameters
    ----------
    test_mode : bool, optional
        _description_, by default False
    """
    record_list = docdb_api_client.retrieve_docdb_records(
        filter_query={},
        projection={
            "data_description.modality": 1,
            "name": 1,
            "_id": 1,
            "location": 1,
            "created": 1,
        },
        limit=0 if not test_mode else 10,
        paginate_batch_size=500,
    )

    records = []
    # Now add some information about the records, i.e. modality, derived state, etc.
    for i, record in enumerate(record_list):
        if (
            "data_description" in record
            and record["data_description"]
            and "modality" in record["data_description"]
        ):
            if isinstance(record["data_description"]["modality"], list):
                modalities = [
                    mod["abbreviation"]
                    for mod in record["data_description"]["modality"]
                ]
        else:
            modalities = []
        derived = True if record["name"].count("_") <= 3 else False

        info_data = {
            "modalities": ",".join(modalities),
            "derived": derived,
            "name": record["name"],
            "_id": record["_id"],
            "location": record["location"],
            "created": record["created"],
        }

        records.append(info_data)

    return pd.DataFrame(
        records,
        columns=["modalities", "derived", "name", "_id", "location", "created"],
    )