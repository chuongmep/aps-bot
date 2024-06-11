import click
from aps_toolkit import Bucket
from .tokenconfig import TokenConfig
from aps_toolkit.Bucket import PublicKey
from .config import Config
import json
from tabulate import tabulate


@click.command()
@click.option('--bucket_name', prompt='Bucket Name', default=lambda: Config.load_bucket_name(),
              help='The key of the bucket.')
@click.option('--bucket_key', prompt='Select Bucket Key (1: transient, 2: temporary, 3: persistent)',
              type=click.Choice(['1', '2', '3'], case_sensitive=False), help='The key of the bucket.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
def bucket_create(bucket_name, bucket_key, region):
    """This command creates a new bucket."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    switcher = {
        '1': PublicKey.transient,
        '2': PublicKey.temporary,
        '3': PublicKey.persistent
    }
    bucket_key = switcher.get(bucket_key)
    result = bucket.create_bucket(bucket_name, bucket_key)
    # save
    Config.save_bucket_name(bucket_name)
    if not result:
        click.echo("Bucket creation failed.")
        return
    click.echo("Bucket created successfully!")
    print(json.dumps(result, indent=4))


# get all buckets
@click.command()
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
def buckets(region):
    """This command lists all buckets."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    df = bucket.get_all_buckets()
    if df.empty:
        click.echo("No buckets found.")
        return
    print(tabulate(df, headers="keys", tablefmt="psql"))


# get objects
@click.command()
@click.option('--bucket_name', prompt='Bucket Name', default=lambda: Config.load_bucket_name(),
              help='The key of the bucket.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
def bucket_objects(bucket_name, region):
    """This command lists all objects in a bucket."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    df = bucket.get_objects(bucket_name)
    if df.empty:
        click.echo("No objects found.")
        return
    print(tabulate(df, headers="keys", tablefmt="psql"))


# upload object bucket
@click.command()
@click.option('--bucket_name', prompt='Bucket Name', default=lambda: Config.load_bucket_name(),
              help='The key of the bucket.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
@click.option('--object_name', prompt='Object Name', help='The name of the object.')
@click.option('--file_path', prompt='File Path', help='The path of the file.')
def bucket_upload_object(bucket_name, region, object_name, file_path):
    """This command uploads an object to a bucket."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    result = bucket.upload_object(bucket_name, file_path, object_name)
    if not result:
        click.echo("Object upload failed.")
        return
    click.echo("Object uploaded successfully!")
    print(json.dumps(result, indent=4))


# download
@click.command()
@click.option('--bucket_name', prompt='Bucket Name', default=lambda: Config.load_bucket_name(),
              help='The key of the bucket.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
@click.option('--object_name', prompt='Object Name', help='The name of the object.')
@click.option('--file_path', prompt='File Path', help='The path of the file.')
def bucket_download_object(bucket_name, region, object_name, file_path):
    """This command downloads an object from a bucket."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    result = bucket.download_object(bucket_name, object_name, file_path)
    if not result:
        click.echo("Object download failed.")
        return
    click.echo("Object downloaded successfully!")


# delete object
@click.command()
@click.option('--bucket_name', prompt='Bucket Name', default=lambda: Config.load_bucket_name(),
              help='The key of the bucket.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the bucket.')
@click.option('--object_name', prompt='Object Name', help='The name of the object.')
def bucket_delete_object(bucket_name, region, object_name):
    """This command deletes an object from a bucket."""
    token = TokenConfig.load_config()
    bucket = Bucket(token, region)
    result = bucket.delete_object(bucket_name, object_name)
    if not result:
        click.echo("Object deletion failed.")
        return
    click.echo("Object deleted successfully!")
