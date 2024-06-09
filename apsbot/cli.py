import click
from aps_toolkit import Auth, BIM360, AuthGoogleColab
from aps_toolkit import Token
from aps_toolkit import PropDbReaderRevit
import pyperclip
from tabulate import tabulate
import subprocess
import os
from .tokenconfig import TokenConfig
from .config import Config
import pandas as pd
import json
import requests
import base64


@click.group()
def apsbot():
    """Welcome to CLI apsbot! This CLI tool is used to interact with the Autodesk Platform Services(Former Autodesk Forge) API."""
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
@click.option('--folder_path', prompt='Folder Path', default=lambda: Config.load_folder_path(),
              help='The folder path to save data.')
def set_folder(folder_path):
    """This command sets the default folder for saving data."""
    # check if user input is valid
    if not os.path.exists(folder_path):
        click.echo("Invalid folder path.")
        return
    # check if input filepath 
    if os.path.isfile(folder_path):
        # get folder path
        folder = os.path.dirname(folder_path)
        Config.save_folder_path(folder)
    else:
        Config.save_folder_path(folder_path)
    click.echo(f"Default folder has been set to {folder_path}")


@apsbot.command()
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


@apsbot.command()
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
@click.option('--hub_id', prompt='Hub Id', default=lambda: Config.load_hub_id(),
              help='The projects information from hub id.')
@click.option('--save_data', prompt='Save Data(y/n)',default='n', help='Save data to file.')
def projects(hub_id, save_data):
    """Get batch all projects with general information by hub_id"""
    if not hub_id:
        click.echo("Please provide a Hub Id.")
        return
    # save hub_id to config
    Config.save_hub_id(hub_id)
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    df = bim360.batch_report_projects(hub_id)
    if df.empty:
        click.echo("No projects found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'projects.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Projects data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


@apsbot.command()
@click.option('--hub_id', prompt='Hub Id', default=lambda: Config.load_hub_id(),
              help='The projects information from hub id.')
@click.option('--project_id', prompt='Project Id', default=lambda: Config.load_project_id(),
              help='The projects information from project id.')
@click.option('--save_data', prompt='Save Data(y/n)',default='n', help='Save data to file.')
def top_folders(hub_id, project_id, save_data):
    """Get batch all top folders with general information by hub_id and project_id"""
    if not hub_id or not project_id:
        click.echo("Please provide a Hub Id and Project Id.")
        return
    Config.save_hub_id(hub_id)
    Config.save_project_id(project_id)
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    df = bim360.batch_report_top_folders(hub_id, project_id)
    if df.empty:
        click.echo("No top folder found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'top_folders.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Top folders data saved to {file_path}")
    # just show df id,name
    df = df[['id', 'name']]
    print(tabulate(df, headers="keys", tablefmt="psql", ))


@apsbot.command()
@click.option('--project_id', prompt='Project Id', default=lambda: Config.load_project_id(),
              help='The projects information from project id.')
@click.option('--folder_id', prompt='Folder Id', default=lambda: Config.load_folder_id(),
              help='The projects information from folder id.')
@click.option('--extension', prompt='Extension', default=".rvt", help='The projects information from extension.')
@click.option('--is_sub_folder', prompt='Is Sub Folder(y/n)', default="n",
              help='The projects information from is sub folder.')
@click.option('--save_data', prompt='Save Data(y/n)', default="n", help='Save data to file.')
def items(project_id, folder_id, extension, is_sub_folder, save_data):
    """Get batch all items with general information by project_id and folder_id"""
    if not project_id or not folder_id:
        click.echo("Please provide a Hub Id and Project Id.")
        return
    Config.save_folder_id(folder_id)
    Config.save_project_id(project_id)
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    if str.lower(is_sub_folder) == 'y':
        is_sub_folder = True
    else:
        is_sub_folder = False
    df = bim360.batch_report_items(project_id, folder_id, extension, is_sub_folder)
    if df.empty:
        click.echo("No items found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'items.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Items data saved to {file_path}")
    # just show item_id, item_name, derivative_urn
    df = df[['item_id', 'item_name', 'derivative_urn']]
    print(tabulate(df, headers="keys", tablefmt="psql"))


@apsbot.command()
@click.option('--project_id', prompt='Project Id', default=lambda: Config.load_project_id(),
              help='The projects information from project id.')
@click.option('--item_id', prompt='Item Id', default=lambda: Config.load_item_id(), help='The urn of the item.')
@click.option('--save_data', prompt='Save Data(y/n)',default="n", help='Save data to file.')
def item_versions(project_id, item_id, save_data):
    """Get batch all item versions with general information by project_id and item_id"""

    if not project_id or not item_id:
        click.echo("Please provide a Hub Id and Project Id.")
        return
    Config.save_item_id(item_id)
    Config.save_project_id(project_id)
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    df = bim360.batch_report_item_versions(project_id, item_id)
    if df.empty:
        click.echo("No top folder found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'item_versions.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Item Versions data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


@apsbot.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default="n", help='Save data to file.')
def data_revit_parameters(urn, region, save_data):
    """Read all parameters by urn."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    Config.save_derivative_urn(urn)
    list = propdb.get_all_parameters()
    series = pd.Series(list)
    df = pd.DataFrame(series, columns=['Parameter'])
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'parameters.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## all categories
@apsbot.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def data_revit_categories(urn, region, save_data):
    """Read all categories by urn."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    Config.save_derivative_urn(urn)
    dict_categories = propdb.get_all_categories()
    df = pd.DataFrame.from_dict(dict_categories, orient='index', columns=['Category'])
    # rename columns index to DbId
    df.index.name = 'DbId'
    # add new column at left is index 
    df.reset_index(inplace=True)
    df.index.name = 'Index'
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'categories.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## by categories
@apsbot.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--categories', prompt='Categories', default=lambda: Config.load_revit_categories(),
              help='The categories of the elements.')
@click.option('--is_sub_family', prompt='Is Sub Family(y/n)', default="n", help='The is sub family of the elements.')
@click.option('--display_unit', prompt='Display Unit(y/n)', default="n", help='The display unit of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def data_revit_by_categories(urn, region, categories, is_sub_family, display_unit, save_data):
    """Read Revit data by categories."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    if not categories:
        click.echo("Please provide categories.")
        return
    Config.save_derivative_urn(urn)
    Config.save_revit_categories(categories)
    list_categories = categories.split(',')
    if str.lower(is_sub_family) == 'y':
        is_sub_family = True
    else:
        is_sub_family = False
    if str.lower(display_unit) == 'y':
        display_unit = True
    else:
        display_unit = False
    # main function
    print("Categories: ", list_categories)
    df = propdb.get_data_by_categories(list_categories, is_sub_family, display_unit=display_unit)
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'data_categories.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## by categories and parameteres
@apsbot.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--categories', prompt='Categories', default=lambda: Config.load_revit_categories(),
              help='The categories of the elements.')
@click.option('--parameters', prompt='Parameters', default=lambda: Config.load_revit_parameters(),
              help='The parameters of the elements.')
@click.option('--is_sub_family', prompt='Is Sub Family(y/n)', default="n", help='The is sub family of the elements.')
@click.option('--display_unit', prompt='Display Unit(y/n)', default="n", help='The display unit of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def data_revit_by_cats_params(urn, region, categories, parameters, is_sub_family, display_unit, save_data):
    """Read Revit data by categories and parameters."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    if not categories:
        click.echo("Please provide categories.")
        return
    if not parameters:
        click.echo("Please provide parameters.")
        return
    Config.save_derivative_urn(urn)
    Config.save_revit_categories(categories)
    Config.save_revit_parameters(parameters)
    list_categories = categories.split(',')
    list_parameters = parameters.split(',')
    if str.lower(is_sub_family) == 'y':
        is_sub_family = True
    else:
        is_sub_family = False
    if str.lower(display_unit) == 'y':
        display_unit = True
    else:
        display_unit = False
    # main function
    print("Categories: ", list_categories)
    print("Parameters: ", list_parameters)
    df = propdb.get_data_by_categories_and_params(list_categories, list_parameters, is_sub_family,
                                                  display_unit=display_unit)
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'data_categories_params.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))
