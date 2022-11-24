import json
import os
import subprocess
from datetime import datetime
from typing import Optional


def export_ddb(
    path: str, timestamp: bool = True, db_name_export: Optional[str] = None
) -> str:
    """
    Export DynamoDB table content to a local JSON file.
    Output: the export file path
    """

    if not db_name_export:
        db_name_export = input("\nName of DynamoDB table to export from: ")

    export_filename: str = f"{db_name_export}_export.json"
    if timestamp:
        export_filename: str = f"{db_name_export}_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    if not os.path.exists(path):
        # Create the directory because it does not exist
        os.makedirs(os.path.join(os.getcwd(), path))
    export_file_path: str = os.path.join(os.getcwd(), path, export_filename)
    export_command: str = f"aws dynamodb scan --table-name {db_name_export} --no-paginate > {export_file_path}"
    subprocess.check_output(export_command, shell=True)

    file = open(export_file_path, "r")
    print(
        "\nTable '{}' exported to '{}' with {} items.".format(
            db_name_export, export_file_path, len(json.load(file)["Items"])
        )
    )

    return export_file_path