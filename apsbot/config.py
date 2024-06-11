import json
import os
import uuid as guid


class Config:
    config_path = 'config.json'

    @classmethod
    def save_folder_path(cls, path):
        """Save the folder data to a JSON file."""
        # check if the folder_data exists
        if not os.path.exists(path):
            os.makedirs(path)
        cls._save_to_config('FOLDER_PATH', path)

    @classmethod
    def load_folder_path(cls):
        """Load the folder data from a JSON file."""
        current_folder = cls._load_from_config('FOLDER_PATH')
        if current_folder is None:
            return os.getcwd()
        return current_folder

    @classmethod
    def save_bucket_name(cls, bucket_name):
        """Save the bucket name to a JSON file."""
        cls._save_to_config('BUCKET_NAME', bucket_name)

    @classmethod
    def load_bucket_name(cls):
        """Load the bucket name from a JSON file."""
        name = cls._load_from_config('BUCKET_NAME')
        if name is None:
            return 'apsbot' + str(guid.uuid4())
        return name

    @classmethod
    def save_project_id(cls, project_id):
        """Save the default project ID to a JSON file."""
        cls._save_to_config('DEFAULT_PROJECT_ID', project_id)

    @classmethod
    def load_project_id(cls):
        """Load the default project ID from a JSON file."""
        return cls._load_from_config('DEFAULT_PROJECT_ID')

    @classmethod
    def save_hub_id(cls, hub_id):
        """Save the default hub ID to a JSON file."""
        cls._save_to_config('DEFAULT_HUB_ID', hub_id)

    @classmethod
    def load_hub_id(cls):
        """Load the default hub ID from a JSON file."""
        return cls._load_from_config('DEFAULT_HUB_ID')

    @classmethod
    def save_folder_id(cls, folder_id):
        """Save the default folder ID to a JSON file."""
        cls._save_to_config('DEFAULT_FOLDER_ID', folder_id)

    @classmethod
    def load_folder_id(cls):
        """Load the default folder ID from a JSON file."""
        return cls._load_from_config('DEFAULT_FOLDER_ID')

    @classmethod
    def save_item_id(cls, item_id):
        """Save the default item ID to a JSON file."""
        cls._save_to_config('DEFAULT_ITEM_ID', item_id)

    @classmethod
    def load_item_id(cls):
        """Load the default item ID from a JSON file."""
        return cls._load_from_config('DEFAULT_ITEM_ID')

    @classmethod
    def save_derivative_urn(cls, derivative_urn):
        """Save the default derivative URN to a JSON file."""
        cls._save_to_config('DEFAULT_DERIVATIVE_URN', derivative_urn)

    @classmethod
    def load_derivative_urn(cls):
        """Load the default derivative URN from a JSON file."""
        return cls._load_from_config('DEFAULT_DERIVATIVE_URN')

    @classmethod
    def save_revit_category(cls, revit_category):
        """Save the default Revit category to a JSON file."""
        cls._save_to_config('DEFAULT_REVIT_CATEGORY', revit_category)

    @classmethod
    def load_revit_category(cls):
        """Load the default Revit category from a JSON file."""
        return cls._load_from_config('DEFAULT_REVIT_CATEGORY')

    @classmethod
    def save_revit_categories(cls, revit_categories):
        """Save the list of Revit categories to a JSON file."""
        cls._save_to_config('REVIT_CATEGORIES', revit_categories)

    @classmethod
    def load_revit_categories(cls):
        """Load the list of Revit categories from a JSON file."""
        return cls._load_from_config('REVIT_CATEGORIES')

    @classmethod
    def load_revit_families(cls):
        """Load the list of Revit families from a JSON file."""
        return cls._load_from_config('REVIT_FAMILIES')

    @classmethod
    def save_revit_families(cls, revit_families):
        """Save the list of Revit families to a JSON file."""
        cls._save_to_config('REVIT_FAMILIES', revit_families)

    @classmethod
    def load_revit_family_types(cls):
        """Load the list of Revit family types from a JSON file."""
        return cls._load_from_config('REVIT_FAMILY_TYPES')

    @classmethod
    def save_revit_family_types(cls, revit_family_types):
        """Save the list of Revit family types to a JSON file."""
        cls._save_to_config('REVIT_FAMILY_TYPES', revit_family_types)

    @classmethod
    def save_revit_parameters(cls, revit_parameters):
        """Save the list of Revit parameters to a JSON file."""
        cls._save_to_config('REVIT_PARAMETERS', revit_parameters)

    @classmethod
    def load_revit_parameters(cls):
        """Load the list of Revit parameters from a JSON file."""
        return cls._load_from_config('REVIT_PARAMETERS')

    @classmethod
    def save_region(cls, region):
        """Save the default region to a JSON file."""
        cls._save_to_config('DEFAULT_REGION', region)

    @classmethod
    def load_region(cls):
        """Load the default region from a JSON file."""
        region = cls._load_from_config('DEFAULT_REGION')
        if region is None or region == '':
            return 'US'
        return region

    @classmethod
    def _save_to_config(cls, key, value):
        """Generic save method for any configuration setting."""
        if not os.path.exists(cls.config_path):
            config_data = {}
        else:
            with open(cls.config_path, 'r') as file:
                config_data = json.load(file)

        config_data[key] = value

        with open(cls.config_path, 'w') as file:
            # save indent for easy read
            json.dump(config_data, file, indent=4)

    @classmethod
    def _load_from_config(cls, key):
        """Generic load method for any configuration setting."""
        if not os.path.exists(cls.config_path):
            return None

        with open(cls.config_path, 'r') as file:
            config_data = json.load(file)
            return config_data.get(key)
