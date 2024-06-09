import json
import os

class Config:
    config_path = 'config.json'

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
        return cls._load_from_config('DEFAULT_REGION')

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
            json.dump(config_data, file)

    @classmethod
    def _load_from_config(cls, key):
        """Generic load method for any configuration setting."""
        if not os.path.exists(cls.config_path):
            return None
        
        with open(cls.config_path, 'r') as file:
            config_data = json.load(file)
            return config_data.get(key)
