import click
from aps_toolkit import Auth,BIM360, AuthGoogleColab
import pyperclip
from tabulate import tabulate
import subprocess
import os
@click.group()
def apsbot():
    """Welcome to CLI apsbot! This CLI tool is used to interact with the Autodesk Forge API."""
    pass


@apsbot.command()
def show_ports():
    """This command displays all network ports currently in use on the system."""
    try:
        # Use 'lsof' to list all open files by network connections (-i) without hostname resolution (-n)
        # and showing numerical port numbers (-P)
        result = subprocess.run(['lsof', '-i', '-P', '-n'], capture_output=True, text=True)
        if result.returncode == 0:
            ports = set()
            for line in result.stdout.split('\n'):
                if line.strip() and (line.lower().startswith('tcp') or line.lower().startswith('udp')):
                    parts = line.split()
                    # Extract the port part from address which is usually the last part after ':'
                    port = parts[-2].split(':')[-1]
                    ports.add(port)
            if ports:
                click.echo("Ports currently in use:")
                for port in sorted(ports, key=int):
                    click.echo(port)
            else:
                click.echo("No ports are currently in use.")
        else:
            click.echo("Failed to retrieve port information.")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

@apsbot.command()
def auth2leg():
    """This command authenticates with 2-legged OAuth and copies the token to the clipboard."""
    auth = Auth()
    result = auth.auth2leg()
    click.echo("Auth 2 legged success!")
    token = result.access_token
    os.environ['APS_ACCESS_TOKEN'] = token
    print("Token Saved to Environment Variables")
    print("Access Token: ", token)
    print("Expires in: ", result.expires_in)
    # copy to clipboard
    pyperclip.copy(token)
    print("Note: Token copied to clipboard.")

    
@apsbot.command()
@click.option('--callback', prompt='Callback URL', default='http://localhost:5000/api/auth/callback', help='The callback URL.')
@click.option('--scope', prompt='Scope', default='data:read data:write', help='The scope.')
def auth3leg(callback, scope):
    """This command authenticates with 3-legged OAuth and copies the token to the clipboard."""
    auth = AuthGoogleColab()
    result = auth.auth3leg(callback, scope)
    click.echo("Auth 3 legged success!")
    os.environ['APS_ACCESS_TOKEN'] = result.access_token
    os.environ['APS_REFRESH_TOKEN'] = result.refresh_token
    print("Token Saved to Environment Variables")
    print("Access Token: ", result.access_token)
    print("Refresh Token: ", result.refresh_token)
    print("Expires in: ", result.expires_in)
    # copy to clipboard
    pyperclip.copy(result.access_token)
    print("Note: Token copied to clipboard.")
    
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
    
@apsbot.command()
@click.option('--hub_id', prompt='Hub Id', help='The projects information from hub id.')
@click.option('--project_id', prompt='Project Id', help='The projects information from project id.')
def get_top_folder(hub_id, project_id):
    """This command gets the top folder of a project."""
    if not hub_id or not project_id:
        click.echo("Please provide a Hub Id and Project Id.")
        return
    bim360 = BIM360()
    df = bim360.batch_report_top_folders(hub_id, project_id)
    if df.empty:
        click.echo("No top folder found.")
        return
    print(tabulate(df, headers="keys", tablefmt="psql"))