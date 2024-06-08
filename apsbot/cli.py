import click
from aps_toolkit import Auth,BIM360, AuthGoogleColab
from aps_toolkit import Token
import pyperclip
from tabulate import tabulate
import subprocess
import os
from .config import TokenConfig
import json
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
    token = auth.auth2leg()
    click.echo("Auth 2 legged success!")
    TokenConfig.save_config(token)
    print("Token Saved to Environment Variables")
    print("Access Token: ", token.access_token)
    print("Expires in: ", token.expires_in)
    # copy to clipboard
    pyperclip.copy(token.access_token)
    print("Note: Token copied to clipboard.")

    
@apsbot.command()
@click.option('--callback', prompt='Callback URL', default='http://localhost:5000/api/auth/callback', help='The callback URL.')
@click.option('--scope', prompt='Scope', default='data:read data:write', help='The scope.')
def auth3leg(callback, scope):
    """This command authenticates with 3-legged OAuth and copies the token to the clipboard."""
    auth = AuthGoogleColab()
    result = auth.auth3leg(callback, scope)
    if not result:
        click.echo("Auth 3 legged failed.")
        return
    TokenConfig.save_config(result)
    click.echo("Auth 3 legged success! Saving token to token_config.json.")
    print("Access Token: ", result.access_token)
    print("Refresh Token: ", result.refresh_token)
    print("Expires in: ", result.expires_in)
    # copy to clipboard
    pyperclip.copy(result.access_token)
    print("Note: Token copied to clipboard.")
    
@apsbot.command()
def hubs():
    """This command lists all hubs."""
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    result = bim360.get_hubs()
    if not result:
        click.echo("No hubs found.")
        return
    print(json.dumps(result, indent=4))



@apsbot.command()
@click.option('--hub_id', prompt='Hub Id', help='The projects information from hub id.')
def get_projects(hub_id):
    """This command gets the details of a projects inside hub."""
    if not hub_id:
        click.echo("Please provide a Hub Id.")
        return
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
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

@apsbot.command()
@click.option('--hub_id', prompt='Hub Id', help='The projects information from hub id.')
@click.option('--project_id', prompt='Project Id', help='The projects information from project id.')
def get_items(project_id, folder_id,extension,is_sub_folder):
    """This command gets the top folder of a project."""
    if not hub_id or not project_id:
        click.echo("Please provide a Hub Id and Project Id.")
        return
    bim360 = BIM360()
    df = bim360.batch_report_items(project_id, folder_id,extension,is_sub_folder)
    if df.empty:
        click.echo("No top folder found.")
        return
    print(tabulate(df, headers="keys", tablefmt="psql"))