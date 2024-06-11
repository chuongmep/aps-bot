from .acc import *
from .auth import *
from .bucket import *
from .chat import *
from .revit import *
from .settings import *


@click.group()
def apsbot():
    """Welcome to CLI apsbot! This CLI tool is used to interact with the Autodesk Platform Services(Former Autodesk Forge) API."""
    pass


# settings
apsbot.add_command(set_folder)

# auth
apsbot.add_command(auth2leg)
apsbot.add_command(auth3leg)
apsbot.add_command(login)
apsbot.add_command(show_ports)
# bucket
apsbot.add_command(buckets)
apsbot.add_command(bucket_create)
apsbot.add_command(bucket_objects)
apsbot.add_command(bucket_delete_object)
apsbot.add_command(bucket_upload_object)
apsbot.add_command(bucket_download_object)

# acc
apsbot.add_command(hubs)
apsbot.add_command(projects)
apsbot.add_command(top_folders)
apsbot.add_command(items)
apsbot.add_command(item_versions)

# revit
apsbot.add_command(revit_categories)
apsbot.add_command(revit_parameters)
apsbot.add_command(revit_families)
apsbot.add_command(revit_family_types)
apsbot.add_command(revit_categories_families_types)
apsbot.add_command(data_revit_by_categories)
apsbot.add_command(data_revit_by_cats_params)
apsbot.add_command(data_revit_by_family)
apsbot.add_command(data_revit_by_family_types)
# chat
apsbot.add_command(chat)
apsbot.add_command(chat_data)
