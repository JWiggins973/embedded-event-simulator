import click
import database 

@click.group()
def cli():
    pass

@cli.command()
def events():
    results = database.get_events()
    for result in results:
        click.echo(result)

@cli.command()
def summary():
    results = database.get_summary()
    for result in results:
        click.echo(result)

@cli.command()
@click.argument('event_type')
def search(event_type):
    results = database.get_events_by_type(event_type)
    for result in results:
        click.echo(result)

@cli.command()
def system_failure():
    results = database.get_events_by_type('SYSTEM_FAILURE_CHECK_ALL')
    for result in results:
        click.echo(result)


if __name__ == '__main__':
    cli()