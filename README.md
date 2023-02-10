# DynamoDB migrator

Python package to export an AWS DynamoDB table content to a JSON file, import an AWS DynamoDB table content from a JSON file, or migrate the content of an AWS DynamoDB table to another through JSON files, using AWS CLI commands.\
DynamoDB migrator needs to be run inside a CLI script, as it uses CLI commands and prompts.

It consists of two main functions that can be used independently:
- `export_ddb` to export data from a DynamoDB database
- `import_ddb` to import data to a DynamoDB database

Using them together by binding the file path output of `export_ddb` to the `file_path` argument of `import_ddb` function will allow to perfom a migration from one DynamoDB table to another.

The import functions use the AWS CLI command `aws dynamodb batch-write-item`, so it will NOT overwrite the existing data in the import table.

## Requirements

- Python >= 3.9
- AWS CLI >= 2.7

It doesn't need any Python virtual environement to be run in as it doesn't require any external Python module.

## How to

- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) if necessary

- Install the package in your project with:\
`pip install git+https://github.com/tachikoma-ai/dynamodb-migrator@main`\
`poetry add git+https://github.com/tachikoma-ai/dynamodb-migrator@main` if you use [Poetry](https://python-poetry.org/)

- Configure your AWS CLI to use the AWS account where your DynamoDB tables are located (note: you can export from one AWS account and then import to anotehr AWS account by editing your script and changing the `AWS_PROFILE` environement variable between the two)

- Import the necessary functions in your script(s), e.g.:
```python
from ddb_migrator import export_ddb, import_ddb
```

- Use the functions in your script(s) as explained in the docstrings, or following the `example.py` example script.
