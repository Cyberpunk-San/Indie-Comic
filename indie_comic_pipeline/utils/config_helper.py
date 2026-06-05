"""
CONFIG HELPER
Resolves absolute paths and loads settings from YAML config
"""

import os

import yaml

                                                            

                                                                  

                                            

                                      

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

def get_project_root():

    """Get the absolute path to the project root directory"""

    return PROJECT_ROOT

def load_settings():

    """Load configuration from config/settings.yaml"""

    settings_path = os.path.join(PROJECT_ROOT, "config", "settings.yaml")

    with open(settings_path, "r", encoding="utf-8") as f:

        return yaml.safe_load(f)

def get_output_path(*path_parts):

    """
    Get absolute path for an output file or directory.
    Automatically creates the parent directory structure if it doesn't exist.
    """

                                                                                             

    if path_parts and os.path.isabs(path_parts[0]):

        full_path = os.path.join(*path_parts)

    else:

        full_path = os.path.join(PROJECT_ROOT, *path_parts)

        

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path

