import json
import os
import subprocess
from datetime import datetime

DB_NAME_EXPORT: str = "my-dynamodb-table-name-to-export-from"
DB_NAME_IMPORT: str = "my-dynamodb-table-name-to-import-into"


def export_db(db_name_export: str) -> str:
    """
    Export data to a local JSON file
    """
    export_filename: str = (
        f"{db_name_export}_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    )
    export_command: str = f"aws dynamodb scan --table-name {db_name_export} --no-paginate > {export_filename}"
    subprocess.call(export_command, shell=True)

    print(f"Exported '{db_name_export}' to '{export_filename}'")

    return export_filename


def import_db(filename: str, db_name_import: str) -> None:
    """
    Load the data from a local JSON file, separate into batches file of 25 reformatted items and import them one by one to the import table
    """

    # Load the data from the local file
    with open(filename) as infile:
        data: dict = json.load(infile)
    print(f"Reading {len(data['Items'])} items")

    BATCH_SIZE: str = 25
    batch_number: int = 1
    count: int = 0

    for item in data["Items"]:

        # Transform the data into a format that can be imported into DynamoDB
        if count % BATCH_SIZE == 0:
            import_data: dict = {db_name_import: []}
        import_data[db_name_import].append({"PutRequest": {"Item": item}})

        count += 1

        if (count % BATCH_SIZE == 0) or (count == len(data["Items"])):
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

    print(f"Imported {count} items in {batch_number - 1} batches to '{db_name_import}'")


if __name__ == "__main__":
    # Export data from the export table
    export_filename: str = export_db(DB_NAME_EXPORT)
    # Import data into the import table
    import_db(export_filename, DB_NAME_IMPORT)
