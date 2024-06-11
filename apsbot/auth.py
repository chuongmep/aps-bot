import click
from .tokenconfig import TokenConfig
from aps_toolkit import Auth, AuthGoogleColab
import requests
import os
import base64
import pyperclip
import subprocess


@click.command()
@click.option('--auth_type', prompt='Select authentication type (1: 2-legged, 2: 3-legged)',
              type=click.Choice(['1', '2'], case_sensitive=False))
def login(auth_type):
    """This command logs in to the Autodesk Platform Services."""
    auth = Auth(None)  # Assuming None for simplicity, replace with actual configuration if needed
    if auth_type == '1':
        token = auth.auth2leg()
        TokenConfig.save_config(token)
        click.echo("Token saved to token_config.json. Authentication type: 2-legged.")
    elif auth_type == '2':
        auth = AuthGoogleColab()
        token = auth.auth3leg()
        TokenConfig.save_config(token)
        click.echo("Token saved to token_config.json. Authentication type: 3-legged.")
    else:
        click.echo("Invalid authentication type.")
        return

    click.echo("Login successful!")


@click.command()
def refresh_token():
    """This command refreshes the access token."""
    token = TokenConfig.load_config()
    if not token:
        click.echo("No token found.")
        return
    url = "https://developer.api.autodesk.com/authentication/v2/revoke"
    client_id = os.getenv("APS_CLIENT_ID")
    client_secret = os.getenv("APS_CLIENT_SECRET")
    auth = f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth
    }
    data = {
        "token": token.refresh_token,
        "token_type_hint": "refresh_token"
    }
    result = requests.post(url, headers=headers, data=data)
    if result.status_code != 200:
        raise Exception(result.content)
    print("Refresh Token Success!")


@click.command()
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


@click.command()
@click.option('--callback', prompt='Callback URL', default='http://localhost:8000/api/auth/callback',
              help='The callback URL.')
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


@click.command()
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
