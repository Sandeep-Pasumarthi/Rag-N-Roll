import yaml
import os


def load_config(config_file_path: str = os.path.join("config", "config.yaml")) -> dict:
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    return config
