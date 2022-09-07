import json
import os
import subprocess
from datetime import datetime
from math import ceil
from typing import Optional


def import_ddb_from_ddb_json(
    file_path: str, db_name_import: Optional[str] = None
) -> None:
    """
    Load the data from a DyanmoDB export JSON file and import it to the DynamoDB table to import to.
    """

    if not db_name_import:
        db_name_import: str = input("\nName of DynamoDB table to import to: ")

    # Load the data from the local file
    with open(file_path) as infile:
        data: dict = json.load(infile)
    if "Items" not in data:
        raise Exception(f"'{file_path}' seems to be invalid: no 'Items' key found")
    print(f"\nReading {len(data['Items'])} items")

    import_data_in_ddb(data=data["Items"], db_name_import=db_name_import, convert_data=False)


def import_ddb_from_dict_json(
    file_path: str, db_name_import: Optional[str] = None
) -> None:
    """
    Load the data from a local JSON file and import it to the DynamoDB table to import to.
    """

    if not db_name_import:
        db_name_import: str = input("\nName of DynamoDB table to import to: ")

    # Load the data from the local file
    with open(file_path) as infile:
        data: list = json.load(infile)
    if not isinstance(data, list):
        raise Exception(f"'{file_path}' seems to be invalid, not a JSON list inside")
    print(f"\nReading {len(data)} items")

    import_data_in_ddb(data=data["Items"], db_name_import=db_name_import, convert_data=True)


def import_data_in_ddb(data: dict, db_name_import: str, convert_data: False) -> None:
    """
    Separate the data into batches file of BATCH_SIZE (25) while reformatting items,
    and import them one by one to the DynamoDB table to import to.
    """
    BATCH_SIZE: int = 25
    batch_number: int = 1
    count: int = 0
    nb_batches: int = ceil(len(data) / BATCH_SIZE)

    for item in data:

        if convert_data:
            # Transform the data into a format that can be imported into DynamoDB
            item: dict = create_ddb_dict(item)

        if count % BATCH_SIZE == 0:
            import_data: dict = {db_name_import: []}
        import_data[db_name_import].append({"PutRequest": {"Item": item}})

        count += 1

        if (count % BATCH_SIZE == 0) or (count == len(data)):

            print(f"\nImporting batch {batch_number}/{nb_batches}")

            # Save the transformed data to a file
            import_filename: str = f"{db_name_import}_import_{batch_number}.json"
            with open(import_filename, "w") as outfile:
                json.dump(import_data, outfile, ensure_ascii=False)

            import_command: str = f"aws dynamodb batch-write-item --request-items file://{import_filename}"
            subprocess.call(
                import_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            batch_number += 1

            os.remove(import_filename)

    print(
        f"\nImported {count} items in {batch_number - 1} batches to '{db_name_import}'"
    )


def create_ddb_dict(item: dict) -> dict:
    ddb_dict: dict = {}
    for key, value in item.items():
        if value and (value not in ["null", "None", "none"]):
            if value == "TRUE":
                ddb_dict[key] = {"BOOL": True}
            elif value == "FALSE":
                ddb_dict[key] = {"BOOL": False}
            else:
                ddb_dict[key] = {"S": str(value)}
        if (key == "created") and (value == "none"):
            ddb_dict[key] = {
                "S": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            }
    return ddb_dict
