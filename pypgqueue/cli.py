import click
import configparser

from pypgqueue.consumer import Consumer
from pypgqueue.database import DatabaseConfig
from pypgqueue.producer import Producer


@click.group()
@click.option('-c', '--config-file', type=click.File('r'),
              help='Configuration file', required=False)
@click.pass_obj
def cli(obj, config_file):
    cfg = configparser.ConfigParser()
    if config_file is not None:
        cfg.read_file(config_file)
    obj['db_config'] = DatabaseConfig(
        hostname=cfg.get('database', 'hostname', fallback='localhost'),
        port=cfg.getint('database', 'port', fallback=15432),
        username=cfg.get('database', 'username', fallback='postgres'),
        password=cfg.get('database', 'password', fallback='postgres'),
        database=cfg.get('database', 'database', fallback='postgres'),
    )


@cli.command()
@click.argument('name')
@click.pass_obj
def consumer(obj, name):
    c = Consumer(db_config=obj['db_config'], name=name)
    c.run()


@cli.command()
@click.argument('name')
@click.option('-n', '--jobs-number', type=click.IntRange(0, 10000), required=True)
@click.option('-w', '--wait', type=click.IntRange(0, 360), default=0, show_default=True)
@click.pass_obj
def producer(obj, name, jobs_number, wait):
    p = Producer(db_config=obj['db_config'], name=name, jobs=jobs_number, wait=wait)
    p.run()


def main():
    cli(obj=dict())
