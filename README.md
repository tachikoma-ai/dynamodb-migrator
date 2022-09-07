# DynamoDB migration script

Simple Python script to migrate the content of an AWS DynamoDB table to another.

## Requirements

- Python >= 3.9
- AWS CLI >= 2.7

It doesn't need any Python virtual environement to be run in as it doesn't require any external Python module.

## How to

- Set up your AWS credentials and region

- Run with:
```bash
python main.py
```

- Input the DynamoDB table name to export as and the DynamoDB table name to import as, as prompted.
