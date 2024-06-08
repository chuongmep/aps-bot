import click
from aps_toolkit import Auth,BIM360
import pyperclip
from tabulate import tabulate

@click.group()
def apsbot():
    """Welcome to CLI apsbot! This CLI tool is used to interact with the Autodesk Forge API."""
    pass

@apsbot.command()
def helloworld():
    """This command prints 'Hello, World!'"""
    click.echo("Hello, World!")

@apsbot.command()
def auth2leg():
    """This command authenticates with 2-legged OAuth and copies the token to the clipboard."""
    auth = Auth()
    result = auth.auth2leg()
    click.echo("Auth 2 legged success!")
    token = result.access_token
    click.echo(token)
    # copy to clipboard
    pyperclip.copy(token)
    
@apsbot.command()
def auth3leg():
    """This command authenticates with 3-legged OAuth and copies the token to the clipboard."""
    auth = Auth()
    result = auth.auth3leg()
    click.echo("Auth 3 legged success!")
    token = result.access_token
    click.echo(token)
    
@apsbot.command()
def hubs():
    """This command lists all hubs."""
    bim360 = BIM360()
    json = bim360.get_hubs()
    if not json:
        click.echo("No hubs found.")
        return
    print(json)

@apsbot.command()
@click.option('--hub_id', prompt='Hub Id', help='The projects information from hub id.')
def get_projects(hub_id):
    """This command gets the details of a projects inside hub."""
    if not hub_id:
        click.echo("Please provide a Hub Id.")
        return
    bim360 = BIM360()
    df = bim360.batch_report_projects(hub_id)
    print(tabulate(df, headers="keys", tablefmt="psql"))
    