import json
import os
import subprocess
from datetime import datetime
from typing import Optional


def export_ddb(path: str, timestamp: bool = True, db_name: Optional[str] = None) -> str:
    """Export DynamoDB table content to a local JSON file.

    Args:
        path (str): the path to the directory where the export file will be saved
        timestamp (bool): whether to add a timestamp to the export file name
        db_name (str, optional): the name of the DynamoDB table to export from.
            If not provided, will ask for it.

    Returns:
        str:the export file path
    """

    if not db_name:
        db_name = input("\nName of DynamoDB table to export from: ")

    export_filename: str = f"{db_name}_export.json"
    if timestamp:
        export_filename: str = (
            f"{db_name}_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )
    if not os.path.exists(path):
        # Create the directory because it does not exist
        os.makedirs(os.path.join(os.getcwd(), path))
    export_file_path: str = os.path.join(os.getcwd(), path, export_filename)
    export_command: str = (
        f"aws dynamodb scan --table-name {db_name} --no-paginate > {export_file_path}"
    )
    subprocess.check_output(export_command, shell=True)

    file = open(export_file_path, "r")
    print(
        "\nTable '{}' exported to '{}' with {} items.".format(
            db_name, export_file_path, len(json.load(file)["Items"])
        )
    )

    return export_file_path
