from import_funcs import import_ddb_from_ddb_json
from export_funcs import export_ddb


EXPORT_PATH: str = "exports/"  # with no slash at the beginning

# Export data from the export table
export_file_path: str = export_ddb(
    path=EXPORT_PATH, timestamp=True, db_name_export=None
)

# Import data into the import table
import_ddb_from_ddb_json(file_path=export_file_path, db_name_import=None, fake=True)
