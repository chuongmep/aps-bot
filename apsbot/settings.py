import os
import click
from apsbot.config import Config


@click.command()
@click.option('--folder_path', prompt='Folder Path', default=lambda: Config.load_folder_path(),
              help='The folder path to save data.')
def set_folder(folder_path):
    """This command sets the default folder for saving data."""
    if not os.path.exists(folder_path):
        click.echo("Invalid folder path.")
        return
    if os.path.isfile(folder_path):
        folder = os.path.dirname(folder_path)
        Config.save_folder_path(folder)
    else:
        Config.save_folder_path(folder_path)
    click.echo(f"Default folder has been set to {folder_path}")
