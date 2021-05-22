import logging
from aws_kinesis_agg.deaggregator import deaggregate_records
from .helpers import filtered_records_generator

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def handler(event, context):
    """
    Triggered for a batch of kinesis records.
    Parses QLDB Journal streams.
    """
    raw_kinesis_records = event['Records']

    # Deaggregate all records in one call
    records = deaggregate_records(raw_kinesis_records)

    # Iterate through deaggregated records of ApiEvent Table
    for record in filtered_records_generator(records, table_names=['ApiEvent']):
        table_name = record["table_info"]["tableName"]
        revision_data = record["revision_data"]
        revision_metadata = record["revision_metadata"]
        document_id = revision_metadata["id"]
        version = revision_metadata["version"]

        logger.info(f'Table: {table_name}, Id: {document_id}, Version: {version}, Data: {revision_metadata}')
