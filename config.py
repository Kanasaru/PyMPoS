import json


class ConfigManager:
    """
    A class for managing configuration data stored in a JSON file.
    """

    def __init__(self, file_path):
        """
        Initialize a ConfigManager instance.

        Args:
            file_path (str): The path to the JSON configuration file.
        """
        self.file_path = file_path
        self.config = {}

    def load_config(self):
        """
        Load the configuration data from the JSON file.

        Returns:
            bool: True if the configuration was loaded successfully, False if the file was not found or there was an error in loading.
        """
        try:
            with open(self.file_path, 'r') as file:
                self.config = json.load(file)
            return True
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.file_path}' not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in configuration file '{self.file_path}'.")
            return False

    def save_config(self):
        """
        Save the current configuration data to the JSON file.

        Returns:
            bool: True if the configuration was saved successfully, False if there was an error in saving.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
            return True
        except Exception as e:
            print(f"Error: Failed to save configuration to '{self.file_path}'.")
            print(str(e))
            return False

    def get_config(self):
        """
        Get the current configuration data.

        Returns:
            dict: The configuration data as a dictionary.
        """
        return self.config

    def update_config(self, new_config):
        """
        Update the configuration data with the provided dictionary.

        Args:
            new_config (dict): A dictionary containing the updated configuration data.
        """
        self.config.update(new_config)

    def set_value(self, key, value, category=None):
        """
        Set a key-value pair in the configuration.

        Args:
            key (str): The key to set.
            value: The value to associate with the key.
            category (str, optional): The category under which to store the key-value pair.
        """
        if category:
            if category not in self.config:
                self.config[category] = {}
            self.config[category][key] = value
        else:
            self.config[key] = value

    def get_value(self, key, category=None):
        """
        Get the value associated with a key in the configuration.

        Args:
            key (str): The key to retrieve.
            category (str, optional): The category in which the key is stored.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        if category:
            if category in self.config:
                return self.config[category].get(key)
            else:
                return None
        else:
            return self.config.get(key)

    def remove_value(self, key, category=None):
        """
        Remove a key-value pair from the configuration.

        Args:
            key (str): The key to remove.
            category (str, optional): The category from which to remove the key-value pair.
        """
        if category:
            if category in self.config and key in self.config[category]:
                del self.config[category][key]
        else:
            if key in self.config:
                del self.config[key]

    def remove_category(self, category):
        """
        Remove an entire category from the configuration.

        Args:
            category (str): The category to remove.
        """
        if category in self.config:
            del self.config[category]

    def __repr__(self):
        """
        Return a string representation of the ConfigManager.
        """
        return f'ConfigManager(file_path={self.file_path}, config={self.config})'

    def __eq__(self, other):
        """
        Compare two ConfigManager instances for equality.
        """
        if isinstance(other, ConfigManager):
            return self.file_path == other.file_path and self.config == other.config
        return False
    