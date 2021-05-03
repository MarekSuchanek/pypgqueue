import dataclasses
import datetime
import uuid


@dataclasses.dataclass
class DatabaseConfig:
    hostname: str
    port: int
    username: str
    password: str
    database: str

    @property
    def connection_string(self):
        return f'postgresql://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}'


@dataclasses.dataclass
class Job:
    id: str
    message: str
    number: int
    created_at: datetime.datetime


class Database:

    INSERT_JOB = 'INSERT INTO jobs (id, message, number, created_at) VALUES (%s, %s, %s, %s);'
    INSERT_RESULT = 'INSERT INTO results (id, message, result, created_at) VALUES (%s, %s, %s, %s);'
    SELECT_JOB = 'SELECT * FROM jobs LIMIT 1 FOR UPDATE SKIP LOCKED;'
    DELETE_JOB = 'DELETE FROM jobs WHERE id = %s;'
    NOTIFY = 'NOTIFY jobs, \'new job added\';'
    LISTEN = 'LISTEN jobs;'

    @classmethod
    def job_query_args(cls, message, number):
        return (
            str(uuid.uuid4()),
            message,
            number,
            datetime.datetime.now()
        )

    @classmethod
    def result_query_args(cls, message, result):
        return (
            str(uuid.uuid4()),
            message,
            result,
            datetime.datetime.now()
        )

    @classmethod
    def get_as_job(cls, result) -> Job:
        _id, message, number, created_at = result
        return Job(
            id=_id,
            message=message,
            number=number,
            created_at=created_at,
        )
