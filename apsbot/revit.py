import click
from .tokenconfig import TokenConfig
from aps_toolkit import PropDbReaderRevit
from .config import Config
import pandas as pd
from tabulate import tabulate
import os
import warnings


@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default="n", help='Save data to file.')
def revit_parameters(urn, region, save_data):
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
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def revit_categories(urn, region, save_data):
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


# families
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def revit_families(urn, region, save_data):
    """Read all families by urn."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    Config.save_derivative_urn(urn)
    dict_families = propdb.get_all_families()
    df = pd.DataFrame.from_dict(dict_families, orient='index', columns=['Family'])
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
        file_path = os.path.join(folder, 'families.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


# family types
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def revit_family_types(urn, region, save_data):
    """Read all family types by urn."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    Config.save_derivative_urn(urn)
    dict_families = propdb.get_all_families_types()
    df = pd.DataFrame.from_dict(dict_families, orient='index', columns=['Family Type'])
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
        file_path = os.path.join(folder, 'family_types.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


# revit categories and family and types
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def revit_categories_families_types(urn, region, save_data):
    """Read all categories, families, and family types by urn."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    Config.save_derivative_urn(urn)
    df = propdb.get_categories_families_types()
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'categories_families_types.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## by categories
@click.command()
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
        file_path = os.path.join(folder, 'data_revit_categories.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## data_revit_by_family
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--families', prompt='Families', default=lambda: Config.load_revit_families(),
              help='The list family names of the elements.')
@click.option('--is_sub_family', prompt='Is Sub Family(y/n)', default="n", help='The is sub family of the elements.')
@click.option('--display_unit', prompt='Display Unit(y/n)', default="n", help='The display unit of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def data_revit_by_family(urn, region, families, is_sub_family, display_unit, save_data):
    """Read Revit data by family."""

    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    if not families:
        click.echo("Please provide family.")
        return
    Config.save_derivative_urn(urn)
    Config.save_revit_families(families)
    list_families = families.split(',')
    if str.lower(is_sub_family) == 'y':
        is_sub_family = True
    else:
        is_sub_family = False
    if str.lower(display_unit) == 'y':
        display_unit = True
    else:
        display_unit = False
    # main function
    print("Families: ", list_families)
    df = propdb.get_data_by_families(families, is_sub_family, display_unit=display_unit)
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'data_revit_families.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## data_revit_by_family_types
@click.command()
@click.option('--urn', prompt='URN', default=lambda: Config.load_derivative_urn(),
              help='The derivative urn of the item version.')
@click.option('--region', prompt='Region', default=lambda: Config.load_region(), help='The region of the item.')
@click.option('--family_types', prompt='Family Types', default=lambda: Config.load_revit_family_types(),
              help='The list family types name of the elements.')
@click.option('--display_unit', prompt='Display Unit(y/n)', default="n", help='The display unit of the item.')
@click.option('--save_data', prompt='Save Data(y/n)', default='n', help='Save data to file.')
def data_revit_by_family_types(urn, region, family_types, display_unit, save_data):
    """Read Revit data by family types."""
    token = TokenConfig.load_config()
    propdb = PropDbReaderRevit(urn, token, region)
    if not urn:
        click.echo("Please provide a urn.")
        return
    if not family_types:
        click.echo("Please provide list name if family types.\b e.g. <Wall,Door>")
        return
    Config.save_derivative_urn(urn)
    Config.save_revit_family_types(family_types)
    list_family_types = family_types.split(',')
    if str.lower(display_unit) == 'y':
        display_unit = True
    else:
        display_unit = False
    # main function
    print("Family Types: ", list_family_types)
    df = propdb.get_data_by_family_types(list_family_types, display_unit=display_unit)
    if df.empty:
        click.echo("No data found.")
        return
    if str.lower(save_data) == 'y':
        folder = Config.load_folder_path()
        file_path = os.path.join(folder, 'data_revit_family_types.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))


## by categories and parameteres
@click.command()
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
        file_path = os.path.join(folder, 'data_revit_categories_params.csv')
        df.to_csv(file_path, index=False)
        click.echo(f"Revit data saved to {file_path}")
    print(tabulate(df, headers="keys", tablefmt="psql"))
