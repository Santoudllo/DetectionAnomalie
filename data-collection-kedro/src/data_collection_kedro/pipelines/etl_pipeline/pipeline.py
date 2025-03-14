"""
pipeline 'etl_pipeline'
"""
from kedro.pipeline import Pipeline, node

from .nodes import etl_api_data, etl_csv_data

def create_pipeline(**kwargs) -> Pipeline:
    """
    Create a Kedro pipeline for the ETL process with multiple API sources.
    Returns::
          Pipeline: The constructed Kedro pipeline.
    """
    return Pipeline(
        [
            node(
                func=etl_api_data,
                inputs=["params:api_urls", "params:db_name", "params:collection_names"],
                outputs=None,
                name="process_api_data_node",
            ),
            node(
                func=etl_csv_data,
                inputs=[
                    "params:csv_file_paths",
                    "params:db_name",
                    "params:collection_names",
                ],
                outputs=None,
                name="process_csv_data_node",
            ),
        ]
    )
