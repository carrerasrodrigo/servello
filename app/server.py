from .error import InvalidFileException
from .parser import parse_file
import click


@click.command()
@click.option('--config', help='json file with the app configuration')
@click.option('--debug', is_flag=True, help='enabled flask debug mode')
@click.option('--port', default=5000, help='port where servello will run')
@click.option('--host', default='localhost',
    help='host where servello will run')
def start_app(config, debug, host, port):
    try:
        server = parse_file(config)
    except InvalidFileException:
        click.echo(f'error loading server file {config}... exiting', err=True)
        exit(1)
    server.start(debug, host, port)


if __name__ == '__main__':
    start_app()
