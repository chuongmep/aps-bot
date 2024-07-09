import click
from .tokenconfig import TokenConfig
from .config import Config
from aps_toolkit import Webhooks
import pandas as pd
import json
import os
from tabulate import tabulate
@click.command()
@click.option('--webhook_id', prompt='Webhook Id', help='The id of the webhook.')
def webhook_delete(webhook_id):
    """This command deletes a webhook."""
    token = TokenConfig.load_config()
    webhook = Webhooks(token)
    result = webhook.delete_hook_by_id(webhook_id)
    if not result:
        click.echo(result)
        return
    click.echo("Webhook deleted successfully!")

@click.command()
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def webhooks_get_all(save_data):
    """This command lists all webhooks."""
    token = TokenConfig.load_config()
    webhook = Webhooks(token)
    result = webhook.batch_report_all_hooks()
    if result.empty:
        click.echo("No webhooks found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'webhooks.csv')
        result.to_csv(file_path, index=False)
        click.echo(f"Webhooks data saved to {file_path}")
    # just show hookId, event, folder
    df = result[["hookId","folder","projectId","event"]]
    print(tabulate(df, headers="keys", tablefmt="psql"))

@click.command()
@click.option('--hook_id', prompt='Hook Id',default=Config.load_webhook_id(), help='The id of the webhook.')
@click.option('--event', prompt='Event', default='dm.version.added', help='The event.')
@click.option('--system', prompt='System', default='data', help='The system.')
def webhook_get_by_id(hook_id,event,system):
    "Get webhook by id from user input"
    token = TokenConfig.load_config()
    webhook = Webhooks(token)
    result = webhook.get_hook_by_id(hook_id,event,system)
    #save webhook_id to config
    Config.save_webhook_id(hook_id)
    # dump json 
    print(json.dumps(result, indent=4))


@click.command()
@click.option('--scope', prompt='Scope', default='data:read data:write', help='The scope.')
@click.option('--callback', prompt='Callback URL', default='http://localhost:8000/api/auth/callback', help='The callback URL.')
@click.option('--event', prompt='Event', default='dm.version.added', help='The event.')
@click.option('--system', prompt='System', default='data', help='The system.')
@click.option('--hookAttribute', prompt='Hook Attribute', default=None, help='The hook attribute.')
def webhook_create(scope, callback, event, system, hookAttribute):
    """This command lists all webhooks."""
    token = TokenConfig.load_config()
    webhook = Webhooks(token)
    result = webhook.create_system_event_hook(scope, callback, event, system, hookAttribute)
    if not result:
        click.echo("No webhooks found.")
        return
    print(json.dumps(result, indent=4))
