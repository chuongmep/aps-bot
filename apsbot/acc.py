import click
from .config import Config
from aps_toolkit import BIM360
import json
from .tokenconfig import TokenConfig
from tabulate import tabulate
import os


@click.command()
def hubs():
    """This command lists all hubs."""
    token = TokenConfig.load_config()
    bim360 = BIM360(token)
    result = bim360.get_hubs()
    if not result:
        click.echo("No hubs found.")
        return
    print(json.dumps(result, indent=4))


@click.command()
@click.option('--hub_id', prompt='Hub Id', default=lambda: Config.load_hub_id(),
              help='The projects information from hub id.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
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


@click.command()
@click.option('--hub_id', prompt='Hub Id', default=lambda: Config.load_hub_id(),
              help='The projects information from hub id.')
@click.option('--project_id', prompt='Project Id', default=lambda: Config.load_project_id(),
              help='The projects information from project id.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
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


@click.command()
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


@click.command()
@click.option('--project_id', prompt='Project Id', default=lambda: Config.load_project_id(),
              help='The projects information from project id.')
@click.option('--item_id', prompt='Item Id', default=lambda: Config.load_item_id(), help='The urn of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default="n", help='Save data to file.')
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
