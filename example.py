import os

from ddb_migrator import export_ddb, import_ddb


EXPORT_PATH: str = "exports/"  # with no slash at the beginning

os.environ["AWS_PROFILE"] = "aws_account_1"
# Export data from the export table
export_file_path: str = export_ddb(
    path=EXPORT_PATH, timestamp=True, db_name="my-ddb-table-name-to-export-from"
)

# Import data into the import table
os.environ["AWS_PROFILE"] = "aws_account_2"
import_ddb(
    file_path=export_file_path,
    from_dynamo=True,
    db_name="my-ddb-table-name-to-import-to",
    fake=True,
)
