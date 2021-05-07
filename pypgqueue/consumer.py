import select
import psycopg2
import psycopg2.extensions
import time

from pypgqueue.consts import LISTEN_TIMEOUT
from pypgqueue.database import DatabaseConfig, Database
from pypgqueue.logging import logger


class Consumer:

    def __init__(self, db_config: DatabaseConfig, name: str):
        self.db_config = db_config
        self.name = name
        self.conn_queue = psycopg2.connect(db_config.connection_string)
        self.conn_query = psycopg2.connect(db_config.connection_string)
        self.numbers = list()
        self.conn_queue.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def _work(self):
        logger.info(f'Consumer {self.name}: working')
        cursor = self.conn_query.cursor()
        cursor.execute(Database.SELECT_JOB)
        result = cursor.fetchall()
        if len(result) != 1:
            logger.info(f'Consumer {self.name}: fetched {len(result)} jobs')
            return False
        job = Database.get_as_job(result[0])
        logger.info(f'Consumer {self.name}: fetched job {job.id}')
        logger.info(f'Consumer {self.name}: message - {job.message}')
        logger.info(f'Consumer {self.name}: computing result')
        self.numbers.append(job.number)
        result = job.number ** 2
        time.sleep(1)
        logger.info(f'Consumer {self.name}: result computed')
        logger.info(f'Consumer {self.name}: storing result')
        message = f'Result for number {job.number} (computed by {self.name})'
        cursor.execute(
            query=Database.INSERT_RESULT,
            vars=Database.result_query_args(message, result),
        )
        logger.info(f'Consumer {self.name}: deleting job')
        cursor.execute(
            query=Database.DELETE_JOB,
            vars=(job.id,)
        )
        logger.info(f'Consumer {self.name}: committing')
        self.conn_query.commit()
        cursor.close()
        return True

    def run(self):
        logger.info(f'Consumer {self.name}: starting')
        cursor = self.conn_queue.cursor()
        cursor.execute(Database.LISTEN)

        while True:
            logger.info(f'Consumer {self.name}: trying to do some work')
            should_work = True
            while should_work:
                should_work = self._work()

            logger.info(f'Consumer {self.name} processed: {self.numbers}')
            logger.info(f'Consumer {self.name}: waiting for notifications')
            if select.select([self.conn_queue], [], [], LISTEN_TIMEOUT) == ([], [], []):
                logger.info(f'Consumer {self.name}: nothing received in this cycle...')
            else:
                self.conn_queue.poll()
                notifications = []
                while self.conn_queue.notifies:
                    notifications.append(self.conn_queue.notifies.pop())
                logger.info(f'Consumer {self.name}: {len(notifications)} notifications received')
