import json
import os
import subprocess
from datetime import datetime
from math import ceil
from typing import Optional


def import_ddb(
    file_path: str,
    from_dynamo: Optional[bool] = True,
    db_name_import: Optional[str] = None,
    fake: Optional[bool] = True,
) -> None:
    """Load the data from a local JSON file and import it to the DynamoDB table to import to.

    Args:
        file_path (str): Path to the JSON file to import from.
        from_dynamo (bool, optional): If True, will import from a DynamoDB JSON format.
            Defaults to True.
        db_name_import (str, optional): Name of the DynamoDB table to import to.
            If not provided, will ask for it.
        fake (bool, optional): If True, will not import the data,
            but will print the command that would have been used. Defaults to True.
    """

    if not db_name_import:
        db_name_import: str = input("\nName of DynamoDB table to import to: ")

    # Load the data from the local file
    if from_dynamo:
        with open(file_path) as infile:
            data: dict = json.load(infile)
        if "Items" not in data:
            raise Exception(
                f"'{file_path}' seems to be an invalid DynamoDB: no 'Items' key found"
            )
        items: list = data["Items"]

    else:
        with open(file_path) as infile:
            data: list = json.load(infile)
        if not isinstance(data, list):
            raise Exception(f"'{file_path}' seems to be invalid, not a JSON list")
        items: list = data
    
    print(f"\nReading {len(items)} items")

    BATCH_SIZE: int = 25
    batch_number: int = 1
    count: int = 0
    nb_batches: int = ceil(len(items) / BATCH_SIZE)

    for item in items:
        if not from_dynamo:
            # Transform the data into a format that can be imported into DynamoDB
            item: dict = create_ddb_dict(item)

        if count % BATCH_SIZE == 0:
            import_data: dict = {db_name_import: []}
        import_data[db_name_import].append({"PutRequest": {"Item": item}})

        count += 1

        if (count % BATCH_SIZE == 0) or (count == len(items)):
            print(f"\nImporting batch {batch_number}/{nb_batches}")

            # Save the transformed data to a file
            import_filename: str = f"{db_name_import}_import_{batch_number}.json"
            with open(import_filename, "w") as outfile:
                json.dump(import_data, outfile, ensure_ascii=False)

            import_command: str = f"aws dynamodb batch-write-item --request-items file://{import_filename}"
            if not fake:
                subprocess.call(
                    import_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            batch_number += 1

            os.remove(import_filename)
    if fake:
        print(
            f"\nFake imported {count} items in {batch_number - 1} batches to '{db_name_import}'"
        )
    else:
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
            elif isinstance(value, int):
                ddb_dict[key] = {"N": value}
            else:
                ddb_dict[key] = {"S": str(value)}
        if (key in ["created", "createdAt"]) and (value == "none"):
            ddb_dict[key] = {
                "S": str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            }
    return ddb_dict
