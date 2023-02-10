from ddb_migrator import export_ddb, import_ddb


EXPORT_PATH: str = "exports/"  # with no slash at the beginning

# Export data from the export table
export_file_path: str = export_ddb(
    path=EXPORT_PATH, timestamp=True, db_name_export="my-ddb-table-name-to-export-from"
)

# Import data into the import table
import_ddb(
    file_path=export_file_path,
    from_dynamo=True,
    db_name_import="my-ddb-table-name-to-import-to",
    fake=True,
)
