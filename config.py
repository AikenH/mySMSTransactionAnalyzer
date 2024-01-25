import yaml


def read_config_file():
    """
    Reads the configuration settings from a YAML file.

    Returns:
        dict: A dictionary containing the configuration parameters.

    Raises:
        FileNotFoundError: If the 'config.yaml' file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    with open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
