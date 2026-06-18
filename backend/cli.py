import click
import database


@click.group()
def cli():
    pass


# python backend/cli.py events
@cli.command()
def events():
    results = database.get_events()
    for row in results:
        click.echo(
            f"ID: {row[0]} | EVENT: {row[1]} | TIME: {row[2]} | SEVERITY: {row[3]}"
        )


# python backend/cli.py summary
@cli.command()
def summary():
    results = database.get_summary()
    if not results:
        click.echo("No events found")
        return
    for row in results:
        click.echo(f"EVENT: {row[0]} | COUNT: {row[1]}")


# python backend/cli.py search QUERY
@cli.command()
@click.argument("event_type")
def search(event_type):
    results = database.get_events_by_type(event_type)
    if not results:
        click.echo(f"No events found for type: {event_type}")
    for rows in results:
        click.echo(f"EVENT: {rows[1]} | TIME: {rows[2]} | SEVERITY: {rows[3]}")


# python backend/cli.py system-failure
@cli.command()
def system_failure():
    results = database.get_events_by_type("SYSTEM_FAILURE_CHECK_ALL")
    if not results:
        click.echo("No system failures found")
        return
    for row in results:
        click.echo(
            f"ID: {row[0]} | EVENT: {row[1]} | TIME: {row[2]} | SEVERITY: {row[3]}"
        )


if __name__ == "__main__":
    cli()
