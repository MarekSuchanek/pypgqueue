import psycopg2
import time

from pypgqueue.database import DatabaseConfig, Database
from pypgqueue.logging import logger


class Producer:

    def __init__(self, db_config: DatabaseConfig, name: str, jobs: int, wait: int):
        self.db_config = db_config
        self.name = name
        self.jobs = jobs
        self.wait = wait
        self.conn = psycopg2.connect(db_config.connection_string)

    def _submit_job(self, index: int):
        logger.info(f'Producer {self.name}: submitting job {index}')
        cursor = self.conn.cursor()
        message = f'Task #{index} from producer {self.name}'
        cursor.execute(
            query=Database.INSERT_JOB,
            vars=Database.job_query_args(message, index + 1),
        )
        cursor.execute(Database.NOTIFY)
        self.conn.commit()
        cursor.close()

    def run(self):
        logger.info(f'Producer {self.name}: starting')
        for i in range(self.jobs):
            self._submit_job(index=i)
            if self.wait > 0:
                logger.info(f'Producer {self.name}: sleep start')
                time.sleep(self.wait)
                logger.info(f'Producer {self.name}: sleep done')
        logger.info(f'Producer {self.name}: finishing')
