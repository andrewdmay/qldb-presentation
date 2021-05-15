import boto3
import logging
import os
from pyqldb.driver.qldb_driver import QldbDriver
from .operations import upsert_event

logging.getLogger().setLevel(logging.INFO)
qldb_ledger = os.environ['QLDB_LEDGER']
topic_arn = os.environ['TOPIC_ARN']
session = boto3.session.Session()
sns_client = session.client('sns')
qldb_driver = QldbDriver(ledger_name=qldb_ledger, boto3_session=session)


def handler(event, context):
    """
    Lambda Handler
    :param dict event: API Gateway Event
    :param context: Lambda Context
    :return: HTTP Response
    """
    def sns_sender():
        sns_client.publish(TopicArn=topic_arn, Message=event['body'])

    qldb_driver.execute_lambda(lambda executor: upsert_event(executor, event['body'], sns_sender))

    return {
        'statusCode': 200,
        'body': 'OK'
    }
