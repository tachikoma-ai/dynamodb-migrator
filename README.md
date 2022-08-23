# DynamoDB migration script

Simple Python script to migrate the content of an AWS DynamoDB table to another.

## Requirements

- Python >= 3.9
- AWS CLI >= 2.7

It doesn't need any Python virtual environement to be run in as it doesn't require any external Python module.

## How to

- Set up your AWS credentials and region

- Set the DynamoDB table name to export as `DB_NAME_EXPORT` and the DynamoDB table name to import as `DB_NAME_IMPORT` in `__main__.py`.

- Run with:
```bash
python __main__.py
```
