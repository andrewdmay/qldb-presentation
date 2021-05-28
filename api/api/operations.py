import amazon.ion.simpleion as simpleion
import logging

logger = logging.getLogger(__name__)


def upsert_event(executor, event, sns_sender):
    """
    Insert or Update event into QLDB ledger using the id attribute as a unique value
    :param executor: QLDB Executor
    :param str event: JSON event
    :param function sns_sender: SNS Sender
    :return bool: true if inserted, false if updated
    """
    ion_event = simpleion.loads(event)

    if 'id' not in ion_event:
        raise ValueError('Event does not contain id attribute')
    id = ion_event['id']

    cursor = executor.execute_statement('SELECT * FROM ApiEvent WHERE id = ?', id)
    record = next(cursor, None)

    if record:
        # Event already exists, update it
        executor.execute_statement('UPDATE ApiEvent AS e SET e = ? WHERE id = ?', ion_event, id)
        logger.info(f'Updated ApiEvent {id}')
    else:
        # Insert Event
        executor.execute_statement('INSERT INTO ApiEvent ?', ion_event)
        logger.info(f'Inserted ApiEvent {id}')
        sns_sender()
        logger.info('Sent new Api Event to SNS Topic')
