import argparse

from src.label_studio_api import LabelStudioApi


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process input arguments")
    parser.add_argument(
        'connections_configuration_file',
        metavar='C',
        type=str,
        help="Configuration file for connections. See test/helpers/azure_storage_configuration.yaml for an example."
    )
    parsed_arguments = parser.parse_args()

    configuration_file = parsed_arguments.connections_configuration_file
    return configuration_file


def create_connections():
    configuration_file = parse_arguments()
    print(f"Creating connections from configuration file: {configuration_file}")
    LabelStudioApi.create_azure_storage_connections_from_configuration_file(configuration_file)
