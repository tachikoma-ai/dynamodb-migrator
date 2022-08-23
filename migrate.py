import json
import os
import subprocess
from datetime import datetime


def export_db(db_name_export: str, path: str) -> str:
    """
    Export DynamoDB table content to a local JSON file.
    Output: the export file path
    """
    export_filename: str = (
        f"{db_name_export}_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    )
    if not os.path.exists(path):
        # Create the directory because it does not exist
        os.makedirs(os.path.join(os.getcwd(), path))
    export_file_path: str = os.path.join(os.getcwd(), path, export_filename)
    export_command: str = f"aws dynamodb scan --table-name {db_name_export} --no-paginate > {export_file_path}"
    subprocess.call(
        export_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print(f"\nTable '{db_name_export}' exported to '{export_file_path}'")

    return export_file_path


def import_db(file_path: str, db_name_import: str) -> None:
    """
    Load the data from a local JSON file, separate into batches file of 25 while reformatting items, and import them one by one to the DynamoDB table to import to.
    """

    # Load the data from the local file
    with open(file_path) as infile:
        data: dict = json.load(infile)
    if "Items" not in data:
        raise Exception(f"'{file_path}' seems to be invalid: no 'Items' key found")
    print(f"\nReading {len(data['Items'])} items")

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

    print(
        f"\nImported {count} items in {batch_number - 1} batches to '{db_name_import}'"
    )


def migrate() -> None:
    db_name_export: str = input("\nName of DynamoDB table to export from: ")
    EXPORT_PATH: str = "exports/"  # with no slash at the beginning
    # Export data from the export table
    export_file_path: str = export_db(db_name_export, EXPORT_PATH)
    # Import data into the import table
    db_name_import: str = input("\nName of DynamoDB table to import to: ")
    import_db(export_file_path, db_name_import)


migrate()
